import pandas as pd

ventes = pd.read_csv("ventes_propre.csv")
clients = pd.read_csv("clients.csv")

resultat = ventes.merge(clients, on="client", how="left", indicator=True)

print(resultat.shape)
print(resultat["_merge"].value_counts())
print(resultat[resultat["_merge"] == "left_only"]["client"].value_counts())