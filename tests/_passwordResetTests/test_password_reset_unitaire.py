"""
Tests unitaires pour la réinitialisation de mot de passe
Tests de validation et logique métier pour la récupération de compte
"""
import pytest
from django.contrib.auth.models import User


@pytest.mark.django_db
class TestPasswordResetValidationUnitaire:
    """Tests unitaires pour la réinitialisation de mot de passe"""

    def test_password_reset_email_valid_user(self):
        """
        TEST UNITAIRE 1 : Vérifier qu'un email valide peut demander réinitialisation
        Arrangement : Un utilisateur existant avec email valide
        Action : Vérifier si l'email est associé à un utilisateur
        Assertion : L'utilisateur doit être trouvé par son email
        """
        # Créer un utilisateur de test
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='oldpass123'
        )
        
        # Chercher l'utilisateur par email
        found_user = User.objects.filter(email='test@example.com').first()
        
        assert found_user is not None, "L'utilisateur doit être trouvé par son email"
        assert found_user.email == user.email, "L'email doit correspondre"

    def test_password_reset_email_invalid_user(self):
        """
        TEST UNITAIRE 2 : Vérifier qu'un email invalide ne trouve pas d'utilisateur
        Arrangement : Un email qui n'existe pas
        Action : Chercher un utilisateur avec cet email
        Assertion : Aucun utilisateur ne doit être trouvé
        """
        # Chercher un utilisateur avec un email inexistant
        found_user = User.objects.filter(email='nonexistent@example.com').first()
        
        assert found_user is None, "Aucun utilisateur ne doit être trouvé pour un email inexistant"

