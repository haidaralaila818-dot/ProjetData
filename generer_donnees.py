import random
import csv

random.seed(42)

clients = ["Awa Traoré", "awa traoré", "Moussa Keita", "MOUSSA KEITA", "Fatoumata Diallo",
           "Ibrahim Coulibaly", "Aminata Sow", "  Seydou Camara ", "Mariam Konaté", None]
produits = ["Riz", "riz", "Huile", "Sucre", "Savon", "Lait", "Thé", "Farine"]
villes = ["Bamako", "bamako", "Sikasso", "Ségou", "Mopti", "Kayes", "BAMAKO"]
formats_date = ["%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y"]

from datetime import date, timedelta

lignes = []
for i in range(1, 201):
    d = date(2026, 1, 1) + timedelta(days=random.randint(0, 300))
    fmt = random.choice(formats_date)
    prix = random.choice([500, 750, 1000, 1500, 2000, None, "abc", -300])
    qte = random.choice([1, 2, 3, 5, 10, None, 999])
    lignes.append([i, random.choice(clients), random.choice(produits),
                   qte, prix, d.strftime(fmt), random.choice(villes)])

# on ajoute quelques doublons exacts
lignes += random.sample(lignes, 10)
random.shuffle(lignes)

with open("ventes_brut.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["id_vente", "client", "produit", "quantite", "prix_unitaire", "date_vente", "ville"])
    w.writerows(lignes)

print("ventes_brut.csv créé :", len(lignes), "lignes")