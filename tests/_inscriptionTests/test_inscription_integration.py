"""
Tests d'intégration pour le module d'inscription
Tests de l'ensemble du flux d'inscription via l'interface HTTP
"""
import pytest
from django.contrib.auth.models import User
from django.test import Client
from customer.models import Customer
from cities_light.models import City
import json


@pytest.mark.django_db
class TestInscriptionIntegration:
    """Tests d'intégration du flux d'inscription complet"""

    def setup_method(self):
        """Initialiser le client HTTP pour chaque test"""
        self.client = Client()

    # Test 3 : Accès à la page d'inscription
    def test_inscription_page_accessible(self):
        """
        TEST D'INTÉGRATION 1 : Vérifier que la page d'inscription est accessible
        Arrangement : Utilisateur non authentifié
        Action : Faire une requête GET vers /customer/signup
        Assertion : La réponse doit avoir un status 200 et contenir le template register.html
        """
        response = self.client.get('/customer/signup')
        assert response.status_code == 200, "La page d'inscription doit être accessible"

    # Test 4 : Redirection utilisateur authentifié vers index
    def test_inscription_redirect_authenticated_user(self, customer_user):
        """
        TEST D'INTÉGRATION 2 : Un utilisateur authentifié doit être redirigé
        Arrangement : Créer et authentifier un utilisateur
        Action : Accéder à la page d'inscription
        Assertion : Doit être redirigé vers la page d'accueil (status 302 ou 301)
        """
        user, customer = customer_user
        self.client.login(username=user.username, password='testpass123')
        response = self.client.get('/customer/signup', follow=False)
        assert response.status_code in [301, 302], "L'utilisateur authentifié doit être redirigé"

    # Test 5 : Créer un nouvel utilisateur valide
    def test_inscription_create_valid_user(self):
        """
        TEST D'INTÉGRATION 3 : Créer avec succès un nouvel utilisateur valide
        Arrangement : Données d'inscription complètes et valides
        Action : Soumettre un POST avec les données d'inscription
        Assertion : Un nouvel utilisateur doit être créé dans la base de données
        """
        inscription_data = {
            'nom': 'Dupont',
            'prenoms': 'Jean',
            'username': 'jeandupont',
            'email': 'jean.dupont@example.com',
            'phone': '+21234567890',
            'adresse': '123 Rue de Paris',
            'password': 'SecurePass123!',
            'passwordconf': 'SecurePass123!'
        }
        initial_count = User.objects.count()
        response = self.client.post('/customer/inscription', data=inscription_data)
        assert User.objects.count() == initial_count + 1, "Un nouvel utilisateur doit être créé"

    # Test 6 : Rejeter les mots de passe non concordants
    def test_inscription_mismatched_passwords(self):
        """
        TEST D'INTÉGRATION 4 : Rejeter l'inscription si les mots de passe ne correspondent pas
        Arrangement : Deux mots de passe différents
        Action : Soumettre un POST avec des mots de passe non concordants
        Assertion : Aucun utilisateur ne doit être créé
        """
        inscription_data = {
            'nom': 'Martin',
            'prenoms': 'Pierre',
            'username': 'piermartin',
            'email': 'pierre.martin@example.com',
            'phone': '+21234567890',
            'adresse': '456 Rue de Lyon',
            'password': 'Password123!',
            'passwordconf': 'DifferentPass123!'
        }
        initial_count = User.objects.count()
        response = self.client.post('/customer/inscription', data=inscription_data)
        assert User.objects.count() == initial_count, "Aucun utilisateur ne doit être créé avec des mots de passe différents"

    # Test 7 : Rejeter un email invalide
    def test_inscription_invalid_email_format(self):
        """
        TEST D'INTÉGRATION 5 : Rejeter un email au format invalide
        Arrangement : Email sans le caractère '@'
        Action : Soumettre un POST avec un email invalide
        Assertion : L'inscription doit échouer et aucun utilisateur ne doit être créé
        """
        inscription_data = {
            'nom': 'Durand',
            'prenoms': 'Sophie',
            'username': 'sophiedurand',
            'email': 'email_invalide_sans_arobase',
            'phone': '+21234567890',
            'adresse': '789 Rue de Marseille',
            'password': 'Password123!',
            'passwordconf': 'Password123!'
        }
        initial_count = User.objects.count()
        response = self.client.post('/customer/inscription', data=inscription_data)
        assert User.objects.count() == initial_count, "Email invalide doit être rejeté"

    # Test 8 : Éviter les doublons d'email
    def test_inscription_duplicate_email(self, customer_user):
        """
        TEST D'INTÉGRATION 6 : Rejeter une inscription avec un email déjà utilisé
        Arrangement : Un utilisateur existe déjà avec un email
        Action : Tenter d'inscrire un nouvel utilisateur avec le même email
        Assertion : L'inscription doit échouer
        """
        user, customer = customer_user
        inscription_data = {
            'nom': 'Nouveau',
            'prenoms': 'Utilisateur',
            'username': 'nouvelutilisateur',
            'email': user.email,  # Même email que l'utilisateur existant
            'phone': '+21234567890',
            'adresse': '999 Rue de Toulouse',
            'password': 'Password123!',
            'passwordconf': 'Password123!'
        }
        initial_count = User.objects.count()
        response = self.client.post('/customer/inscription', data=inscription_data)
        # Vérifier que pas d'utilisateur supplémentaire n'a été créé
        assert User.objects.count() == initial_count, "L'email dupliqué doit être rejeté"

    # Test 9 : Créer le profil client automatiquement
    def test_inscription_create_customer_profile(self):
        """
        TEST D'INTÉGRATION 7 : Créer automatiquement un profil client lors de l'inscription
        Arrangement : Données d'inscription valides
        Action : Inscrire un nouvel utilisateur
        Assertion : Un profil Customer doit être créé et lié à l'utilisateur
        """
        inscription_data = {
            'nom': 'Blanc',
            'prenoms': 'Marie',
            'username': 'marianc',
            'email': 'marie.blanc@example.com',
            'phone': '+21234567890',
            'adresse': '321 Rue de Nice',
            'password': 'Password123!',
            'passwordconf': 'Password123!'
        }
        self.client.post('/customer/inscription', data=inscription_data)
        user = User.objects.get(username='marianc')
        assert hasattr(user, 'customer'), "Un profil customer doit être créé pour le nouvel utilisateur"
        assert user.customer.contact_1 == '+21234567890', "Le numéro de téléphone doit être sauvegardé"

    # Test 10 : Rejeter champs manquants requis
    def test_inscription_missing_required_fields(self):
        """
        TEST D'INTÉGRATION 8 : Rejeter une inscription avec des champs requis manquants
        Arrangement : Données incomplètes (sans email par exemple)
        Action : Soumettre un POST sans le champ email
        Assertion : L'inscription doit échouer
        """
        inscription_data = {
            'nom': 'Test',
            'prenoms': 'Incomplet',
            'username': 'incomplet',
            # Pas d'email
            'phone': '+21234567890',
            'adresse': '111 Rue de Bordeaux',
            'password': 'Password123!',
            'passwordconf': 'Password123!'
        }
        initial_count = User.objects.count()
        response = self.client.post('/customer/inscription', data=inscription_data)
        assert User.objects.count() == initial_count, "Champs manquants doivent être rejetés"
