

Projet d'apprentissage : nettoyer un jeu de ventes avec Python et pandas,
valider la qualité, charger dans SQLite, puis automatiser le pipeline.

> 🚧 Projet en cours

## Contenu
- `generer_donnees.py`, `generer_clients.py` : génèrent les données brutes fictives
- `explorer.py` : exploration des données
- `netoyer.py` : nettoyage pas à pas, avec validation
- `pipeline.py` : pipeline complet (charger → nettoyer → valider → sauvegarder, avec logs)
- `pipeline_elt.py` : version ELT, avec transformation en SQL
- `modeliser.py` : modèle faits/dimensions (`faits_ventes`, `dim_clients`)
- `joindre.py`, `requetes.py` : jointures et requêtes SQL

## Lancer
pip install pandas
python generer_donnees.py
python generer_clients.py
python pipeline.py