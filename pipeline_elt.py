import sqlite3
import pandas as pd

# E + L : extraire et charger les données BRUTES, sans rien corriger
df = pd.read_csv("ventes_brut.csv", dtype=str)
conn = sqlite3.connect("ventes_elt.db")
df.to_sql("ventes_brut", conn, if_exists="replace", index=False)

# T : la transformation se fait en SQL, dans la base
conn.execute("DROP TABLE IF EXISTS ventes_propre")
conn.execute("""
CREATE TABLE ventes_propre AS
SELECT
    CAST(id_vente AS INTEGER) AS id_vente,
    UPPER(SUBSTR(TRIM(ville), 1, 1)) || LOWER(SUBSTR(TRIM(ville), 2)) AS ville,
    UPPER(SUBSTR(TRIM(produit), 1, 1)) || LOWER(SUBSTR(TRIM(produit), 2)) AS produit,
    CASE WHEN CAST(quantite AS INTEGER) BETWEEN 1 AND 50
         THEN CAST(quantite AS INTEGER) END AS quantite,
    CASE WHEN CAST(prix_unitaire AS REAL) > 0
         THEN CAST(prix_unitaire AS REAL) END AS prix_unitaire
FROM (SELECT DISTINCT * FROM ventes_brut)
""")
conn.commit()

print(pd.read_sql("SELECT ville, COUNT(*) AS nb FROM ventes_propre GROUP BY ville", conn))
print(pd.read_sql("SELECT COUNT(*) AS lignes, COUNT(prix_unitaire) AS prix_ok FROM ventes_propre", conn))
conn.close()