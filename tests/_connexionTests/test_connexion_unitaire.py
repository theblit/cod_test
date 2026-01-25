"""
Tests unitaires pour le module de connexion
Tests des validations et de la logique métier de l'authentification
"""
import pytest
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


@pytest.mark.django_db
class TestConnexionValidationUnitaire:
    """Tests unitaires validant les règles métier de connexion"""

    # Test 1 : Authentifier un utilisateur avec identifiants corrects
    def test_authentication_valid_credentials(self, customer_user):
        """
        TEST UNITAIRE 1 : Vérifier qu'un utilisateur peut s'authentifier avec les bons identifiants
        Arrangement : Un utilisateur existant avec username et password valides
        Action : Appeler authenticate() avec les bons identifiants
        Assertion : La fonction authenticate() doit retourner l'objet User
        """
        user, customer = customer_user
        authenticated_user = authenticate(username=user.username, password='testpass123')
        assert authenticated_user is not None, "L'utilisateur doit être authentifié"
        assert authenticated_user.id == user.id, "L'utilisateur authentifié doit correspondre"

    # Test 2 : Rejeter les identifiants incorrects
    def test_authentication_invalid_password(self, customer_user):
        """
        TEST UNITAIRE 2 : Vérifier qu'un mauvais mot de passe est rejeté
        Arrangement : Un utilisateur existant
        Action : Appeler authenticate() avec un mauvais mot de passe
        Assertion : La fonction authenticate() doit retourner None
        """
        user, customer = customer_user
        authenticated_user = authenticate(username=user.username, password='wrongpassword')
        assert authenticated_user is None, "Une mauvaise authentification doit retourner None"

    # Test 3 : Rejeter un utilisateur inexistant
    def test_authentication_nonexistent_user(self):
        """
        TEST UNITAIRE 3 : Vérifier qu'un utilisateur inexistant ne peut pas s'authentifier
        Arrangement : Aucun utilisateur avec ce username
        Action : Appeler authenticate() avec un username inexistant
        Assertion : La fonction authenticate() doit retourner None
        """
        authenticated_user = authenticate(username='usernonexistant', password='anypassword')
        assert authenticated_user is None, "Un utilisateur inexistant ne doit pas être authentifié"
