import sqlite3
import pandas as pd

conn = sqlite3.connect("ventes.db")

requete = """
SELECT ville,
       COUNT(*) AS nb_ventes,
       SUM(quantite * prix_unitaire) AS chiffre_affaires
FROM ventes
GROUP BY ville
ORDER BY chiffre_affaires DESC
"""

print(pd.read_sql(requete, conn))
conn.close()