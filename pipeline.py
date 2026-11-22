import sqlite3
import pandas as pd
import logging
import sys

logging.basicConfig(
    filename="pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8",
)

def charger(chemin):
    """Étape 1 : lire les données brutes."""
    return pd.read_csv(chemin)


def nettoyer(df):
    """Étape 2 : corriger tous les problèmes."""
    df = df.drop_duplicates()

    for col in ["ville", "produit", "client"]:
        df[col] = df[col].str.strip().str.title()
    df["client"] = df["client"].fillna("Inconnu")

    df["prix_unitaire"] = pd.to_numeric(df["prix_unitaire"], errors="coerce")
    df.loc[df["prix_unitaire"] < 0, "prix_unitaire"] = None
    df["prix_unitaire"] = df["prix_unitaire"].fillna(
        df.groupby("produit")["prix_unitaire"].transform("median")
    )

    df.loc[df["quantite"] > 100, "quantite"] = None
    df["quantite"] = df["quantite"].fillna(
        df.groupby("produit")["quantite"].transform("median")
    )
    df["quantite"] = df["quantite"].round().astype(int)

    d1 = pd.to_datetime(df["date_vente"], format="%Y-%m-%d", errors="coerce")
    d2 = pd.to_datetime(df["date_vente"], format="%d/%m/%Y", errors="coerce")
    d3 = pd.to_datetime(df["date_vente"], format="%d-%m-%Y", errors="coerce")
    df["date_vente"] = d1.fillna(d2).fillna(d3)

    return df


def valider(df):
    """Étape 3 : contrôles qualité."""
    assert df.duplicated().sum() == 0, "Il reste des doublons"
    assert df["id_vente"].is_unique, "id_vente n'est pas unique"
    assert df.isna().sum().sum() == 0, "Il reste des valeurs manquantes"
    assert (df["prix_unitaire"] > 0).all(), "Prix négatif ou nul"
    assert df["quantite"].between(1, 100).all(), "Quantité hors limites"


def sauvegarder(df, csv_sortie, base_sortie):
    """Étape 4 : écrire le résultat propre."""
    df.to_csv(csv_sortie, index=False)
    conn = sqlite3.connect(base_sortie)
    df.to_sql("ventes", conn, if_exists="replace", index=False)
    conn.close()






def main():
    try:
        logging.info("Début du pipeline")

        df = charger("ventes_brut.csv")
        logging.info(f"Lignes brutes : {len(df)}")

        df = nettoyer(df)
        valider(df)
        logging.info(f"Lignes propres : {len(df)} - validation OK")

        sauvegarder(df, "ventes_propre.csv", "ventes.db")
        logging.info("Sauvegarde terminée")

    except AssertionError as e:
        logging.error(f"Validation échouée : {e}")
        sys.exit(1)
    except Exception as e:
        logging.exception(f"Erreur inattendue : {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()