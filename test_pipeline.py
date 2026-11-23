import pandas as pd
import pytest

from pipeline import nettoyer, valider


def donnees_brutes():
    """Petit jeu de données avec un exemplaire de chaque problème."""
    return pd.DataFrame({
        "id_vente": [1, 2, 3, 3, 4],
        "client": ["awa traoré", "  MOUSSA KEITA ", None, None, "Awa Traoré"],
        "produit": ["riz", "Riz", "Savon", "Savon", "Savon"],
        "quantite": [2, 999, 3, 3, None],
        "prix_unitaire": ["1000", "abc", "-300", "-300", "500"],
        "date_vente": ["2026-01-05", "06/02/2026", "07-03-2026", "07-03-2026", "2026-04-08"],
        "ville": ["BAMAKO", "bamako", " Ségou", " Ségou", "Kayes"],
    })


@pytest.fixture
def propre():
    return nettoyer(donnees_brutes())


def test_doublons_supprimes(propre):
    assert len(propre) == 4


def test_texte_standardise(propre):
    assert set(propre["ville"]) == {"Bamako", "Ségou", "Kayes"}
    assert set(propre["produit"]) == {"Riz", "Savon"}


def test_client_manquant_devient_inconnu(propre):
    assert "Inconnu" in set(propre["client"])
    assert propre["client"].isna().sum() == 0


def test_prix_aberrants_remplaces(propre):
    assert (propre["prix_unitaire"] > 0).all()
    # le prix "abc" de la vente 2 (Riz) prend la médiane du Riz : 1000
    assert propre.set_index("id_vente").loc[2, "prix_unitaire"] == 1000


def test_quantite_aberrante_remplacee(propre):
    # la quantité 999 de la vente 2 (Riz) prend la médiane du Riz : 2
    assert propre.set_index("id_vente").loc[2, "quantite"] == 2
    assert propre["quantite"].between(1, 100).all()


def test_dates_converties(propre):
    assert pd.api.types.is_datetime64_any_dtype(propre["date_vente"])
    assert propre["date_vente"].isna().sum() == 0


def test_valider_accepte_donnees_propres(propre):
    valider(propre)  # ne doit rien lever


def test_valider_refuse_id_duplique(propre):
    propre.loc[0, "id_vente"] = propre.loc[1, "id_vente"]
    with pytest.raises(AssertionError):
        valider(propre)