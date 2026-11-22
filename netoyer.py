import pandas as pd

df = pd.read_csv("ventes_brut.csv")
print("Avant :", df.shape)

# 1. Supprimer les doublons exacts
df = df.drop_duplicates()

# 2. Nettoyer le texte : enlever les espaces autour, uniformiser la casse
df["ville"] = df["ville"].str.strip().str.title()
df["produit"] = df["produit"].str.strip().str.title()
df["client"] = df["client"].str.strip().str.title()


# 3. Remplacer les clients manquants
print(df["client"].isna().sum())
df["client"] = df["client"].fillna("Inconnu")
print("Après :", df.shape)
print(df["ville"].value_counts())
print(df["produit"].value_counts())
print(df["client"].value_counts(dropna=False))
  # doit afficher 0
# 4. Convertir le prix en nombre
df["prix_unitaire"] = pd.to_numeric(df["prix_unitaire"], errors="coerce")

print(df["prix_unitaire"].describe())
print(df["prix_unitaire"].isna().sum())
# 5. Les prix négatifs sont des erreurs : on les traite comme des valeurs manquantes
df.loc[df["prix_unitaire"] < 0, "prix_unitaire"] = None

# 6. Remplacer les prix manquants par la médiane du même produit
df["prix_unitaire"] = df["prix_unitaire"].fillna(
    df.groupby("produit")["prix_unitaire"].transform("median")
)

print(df["prix_unitaire"].describe())
print(df["prix_unitaire"].isna().sum())
# 7. Quantité : 999 est une valeur aberrante, on la traite comme manquante
df.loc[df["quantite"] > 100, "quantite"] = None

# 8. Remplacer les manquantes par la médiane du même produit
df["quantite"] = df["quantite"].fillna(
    df.groupby("produit")["quantite"].transform("median")
)

# 9. Une quantité est un nombre entier
df["quantite"] = df["quantite"].round().astype(int)

print(df["quantite"].describe())
print(df["quantite"].isna().sum())
# 10. Dates : on essaie chaque format, puis on combine
d1 = pd.to_datetime(df["date_vente"], format="%Y-%m-%d", errors="coerce")
d2 = pd.to_datetime(df["date_vente"], format="%d/%m/%Y", errors="coerce")
d3 = pd.to_datetime(df["date_vente"], format="%d-%m-%Y", errors="coerce")

df["date_vente"] = d1.fillna(d2).fillna(d3)

print(df["date_vente"].isna().sum())   # doit afficher 0
print(df["date_vente"].min(), df["date_vente"].max())
print(df.dtypes)
# 11. Validation : le script s'arrête si une règle est violée
assert df.duplicated().sum() == 0, "Il reste des doublons"
assert df["id_vente"].is_unique, "id_vente n'est pas unique"
assert df.isna().sum().sum() == 0, "Il reste des valeurs manquantes"
assert (df["prix_unitaire"] > 0).all(), "Prix négatif ou nul"
assert df["quantite"].between(1, 100).all(), "Quantité hors limites"

print("Validation OK")

# 12. Chargement : fichier propre + base SQLite
import sqlite3

df.to_csv("ventes_propre.csv", index=False)

conn = sqlite3.connect("ventes.db")
df.to_sql("ventes", conn, if_exists="replace", index=False)
conn.close()

print("Fichiers créés : ventes_propre.csv et ventes.db")