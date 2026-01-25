"""
Tests unitaires pour le module d'inscription
Tests des validations de données et de la logique métier sans l'interface HTTP
"""
import pytest
from django.contrib.auth.models import User
from customer.models import Customer
from django.core.exceptions import ValidationError
from django.core.validators import validate_email


@pytest.mark.django_db
class TestInscriptionValidationUnitaire:
    """Tests unitaires validant les règles métier d'inscription"""

    # Test 1 : Validation d'un email valide
    def test_email_validation_valid_email(self):
        """
        TEST UNITAIRE 1 : Valider qu'un email au format correct est accepté
        Arrangement : Email au format standard
        Action : Appeler validate_email()
        Assertion : Ne doit pas lever d'exception
        """
        email_valide = 'utilisateur@exemple.com'
        try:
            validate_email(email_valide)
            assert True, "Email valide devrait être accepté"
        except ValidationError:
            pytest.fail("Email valide levé une exception")

    # Test 2 : Rejet d'un email invalide
    def test_email_validation_invalid_email(self):
        """
        TEST UNITAIRE 2 : Vérifier qu'un email au format incorrect est rejeté
        Arrangement : Email sans le caractère '@'
        Action : Appeler validate_email()
        Assertion : Doit lever une exception ValidationError
        """
        email_invalide = 'utilisateur_sans_arobase.com'
        with pytest.raises(ValidationError):
            validate_email(email_invalide)
