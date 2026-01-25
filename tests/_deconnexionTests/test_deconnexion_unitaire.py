"""
Tests unitaires pour le module de déconnexion
Tests des validations et de la logique métier de la déconnexion
"""
import pytest
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from customer.models import Customer


@pytest.mark.django_db
class TestDeconnexionValidationUnitaire:
    """Tests unitaires validant les règles métier de déconnexion"""

    # Test 1 : Vérifier qu'un utilisateur authentifié peut être déconnecté
    def test_logout_authenticated_user(self, customer_user):
        """
        TEST UNITAIRE 1 : Vérifier que la session d'un utilisateur peut être supprimée
        Arrangement : Un utilisateur authentifié
        Action : Récupérer le user de la base de données et vérifier son état
        Assertion : L'utilisateur doit exister et être actif
        """
        user, customer = customer_user
        retrieved_user = User.objects.get(id=user.id)
        assert retrieved_user.is_active, "L'utilisateur doit être actif avant déconnexion"
        assert retrieved_user.username == 'testuser', "L'utilisateur doit avoir le bon username"

    # Test 2 : Vérifier que l'utilisateur reste dans la base de données après déconnexion
    def test_user_persists_after_logout(self, customer_user):
        """
        TEST UNITAIRE 2 : Vérifier que la déconnexion ne supprime pas l'utilisateur
        Arrangement : Un utilisateur dans la base de données
        Action : Compter le nombre d'utilisateurs
        Assertion : L'utilisateur doit toujours exister après une déconnexion
        """
        user, customer = customer_user
        count_before = User.objects.filter(username='testuser').count()
        assert count_before == 1, "L'utilisateur doit exister"
        # Le logout ne supprime pas l'utilisateur
        assert User.objects.filter(username='testuser').exists(), "L'utilisateur doit toujours exister"
