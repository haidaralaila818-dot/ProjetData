import sqlite3
import pandas as pd

ventes = pd.read_csv("ventes_propre.csv")
clients = pd.read_csv("clients.csv")

# 1. Ajouter la ligne "Inconnu" dans la dimension
inconnu = pd.DataFrame({"id_client": [0], "client": ["Inconnu"], "telephone": [None]})
clients = pd.concat([inconnu, clients], ignore_index=True)

# 2. Remplacer le nom par l'identifiant dans la table de faits
faits = ventes.merge(clients[["id_client", "client"]], on="client", how="left")
assert faits["id_client"].notna().all(), "Des ventes n'ont pas de client"
faits["id_client"] = faits["id_client"].astype(int)
faits = faits.drop(columns=["client"])

# 3. Charger les deux tables dans la base
conn = sqlite3.connect("ventes_modele.db")
faits.to_sql("faits_ventes", conn, if_exists="replace", index=False)
clients.to_sql("dim_clients", conn, if_exists="replace", index=False)

# 4. Interroger avec une jointure SQL
requete = """
SELECT c.client,
       COUNT(*) AS nb_ventes,
       SUM(f.quantite * f.prix_unitaire) AS chiffre_affaires
FROM faits_ventes f
JOIN dim_clients c ON c.id_client = f.id_client
GROUP BY c.client
ORDER BY chiffre_affaires DESC
"""
print(pd.read_sql(requete, conn))
conn.close()