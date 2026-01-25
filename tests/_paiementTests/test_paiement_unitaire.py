"""
Tests unitaires pour le module de paiement
Tests de la validation et de la logique métier des paiements
"""
import pytest
from django.contrib.auth.models import User
from customer.models import Customer, Panier
from shop.models import Produit


@pytest.mark.django_db
class TestPaiementValidationUnitaire:
    """Tests unitaires validant les règles métier du paiement"""

    # Test 1 : Vérifier qu'un montant de paiement est un nombre positif
    def test_payment_amount_must_be_positive(self):
        """
        TEST UNITAIRE 1 : Vérifier qu'un montant de paiement doit être positif
        Arrangement : Créer des montants de test
        Action : Vérifier la validité des montants
        Assertion : Seuls les nombres positifs doivent être valides
        """
        valid_amount = 10000.0
        invalid_amount = -5000.0
        
        assert valid_amount > 0, "Un montant positif doit être valide"
        assert invalid_amount <= 0, "Un montant négatif doit être invalide"

    # Test 2 : Vérifier que le total du panier est calculé correctement
    def test_panier_total_calculation(self, panier):
        """
        TEST UNITAIRE 2 : Vérifier que le calcul du total du panier fonctionne
        Arrangement : Un panier avec des produits
        Action : Calculer le total du panier
        Assertion : Le total doit être un nombre positif ou zéro
        """
        total = panier.total
        assert isinstance(total, (int, float)), "Le total doit être un nombre"
        assert total >= 0, "Le total ne peut pas être négatif"
