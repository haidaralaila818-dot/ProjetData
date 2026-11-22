import pandas as pd

clients = pd.DataFrame({
    "id_client": [1, 2, 3, 4, 5, 6, 7],
    "client": ["Awa Traoré", "Moussa Keita", "Fatoumata Diallo", "Ibrahim Coulibaly",
               "Aminata Sow", "Seydou Camara", "Mariam Konaté"],
    "telephone": ["70 00 00 01", "70 00 00 02", "70 00 00 03", "70 00 00 04",
                  "70 00 00 05", "70 00 00 06", "70 00 00 07"],
})
clients.to_csv("clients.csv", index=False)
print("clients.csv créé")