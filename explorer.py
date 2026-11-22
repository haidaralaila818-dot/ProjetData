import pandas as pd

df = pd.read_csv("ventes_brut.csv")

print(df.head(10))        # les 10 premières lignes
print(df.shape)           # (nombre de lignes, nombre de colonnes)
print(df.info())          # types des colonnes + valeurs non nulles
print(df.isna().sum())    # valeurs manquantes par colonne
print(df.duplicated().sum())  # nombre de doublons exacts
print(df["ville"].value_counts())  # les variantes d'écriture