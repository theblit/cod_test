"""
Tests unitaires pour le module de panier
Tests des validations et de la logique métier du panier
"""
import pytest
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from customer.models import Customer, Panier, CodePromotionnel
from shop.models import Produit, Etablissement, CategorieEtablissement, CategorieProduit
from datetime import datetime, timedelta


@pytest.mark.django_db
class TestPanierValidationUnitaire:
    """Tests unitaires validant les règles métier du panier"""

    # Test 1 : Créer un panier pour un client
    def test_create_panier_for_customer(self, customer_user):
        """
        TEST UNITAIRE 1 : Vérifier qu'un panier peut être créé pour un client
        Arrangement : Un client existant
        Action : Créer un nouveau Panier lié au client
        Assertion : Le panier doit être créé et lié au bon client
        """
        user, customer = customer_user
        panier = Panier.objects.create(customer=customer, status=True)
        
        assert panier.id is not None, "Le panier doit avoir un ID"
        assert panier.customer.id == customer.id, "Le panier doit être lié au bon client"
        assert panier.status is True, "Le panier doit être actif"

    # Test 2 : Calculer le total du panier
    def test_panier_total_property(self, panier):
        """
        TEST UNITAIRE 2 : Vérifier que la propriété total du panier fonctionne
        Arrangement : Un panier existant
        Action : Accéder à la propriété total
        Assertion : Le total doit être un nombre entier
        """
        total = panier.total
        assert isinstance(total, int), "Le total doit être un entier"
        assert total >= 0, "Le total ne peut pas être négatif"
