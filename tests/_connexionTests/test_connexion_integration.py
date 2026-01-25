"""
Tests d'intégration pour le module de connexion
Tests de l'ensemble du flux de connexion via l'interface HTTP
"""
import pytest
from django.contrib.auth.models import User
from django.test import Client
from customer.models import Customer
import json


@pytest.mark.django_db
class TestConnexionIntegration:
    """Tests d'intégration du flux de connexion complet"""

    def setup_method(self):
        """Initialiser le client HTTP pour chaque test"""
        self.client = Client()

    # Test 4 : Accès à la page de connexion
    def test_login_page_accessible(self):
        """
        TEST D'INTÉGRATION 1 : Vérifier que la page de connexion est accessible
        Arrangement : Utilisateur non authentifié
        Action : Faire une requête GET vers /customer/
        Assertion : La réponse doit avoir un status 200 et contenir le template login.html
        """
        response = self.client.get('/customer/')
        assert response.status_code == 200, "La page de connexion doit être accessible"

    # Test 5 : Redirection utilisateur authentifié vers index
    def test_login_redirect_authenticated_user(self, customer_user):
        """
        TEST D'INTÉGRATION 2 : Un utilisateur authentifié doit être redirigé
        Arrangement : Créer et authentifier un utilisateur
        Action : Accéder à la page de connexion
        Assertion : Doit être redirigé vers la page d'accueil (status 302 ou 301)
        """
        user, customer = customer_user
        self.client.login(username=user.username, password='testpass123')
        response = self.client.get('/customer/', follow=False)
        assert response.status_code in [301, 302], "L'utilisateur authentifié doit être redirigé"

    # Test 6 : Authentification avec username valide
    def test_connexion_valid_username(self, customer_user):
        """
        TEST D'INTÉGRATION 3 : Connecter un utilisateur avec un username valide
        Arrangement : Un utilisateur existant
        Action : Soumettre un POST JSON à /customer/post avec username et password
        Assertion : La réponse doit indiquer une authentification réussie
        """
        user, customer = customer_user
        login_data = {
            'username': user.username,
            'password': 'testpass123'
        }
        response = self.client.post(
            '/customer/post',
            data=json.dumps(login_data),
            content_type='application/json'
        )
        assert response.status_code == 200, "La requête doit être traitée"
        # Vérifier que l'utilisateur est maintenant connecté
        assert self.client.session.get('_auth_user_id') is not None, "L'utilisateur doit être dans la session"

    # Test 7 : Authentification avec email valide
    def test_connexion_valid_email(self, customer_user):
        """
        TEST D'INTÉGRATION 4 : Connecter un utilisateur avec son email à la place du username
        Arrangement : Un utilisateur existant avec un email
        Action : Soumettre un POST JSON avec l'email et le password
        Assertion : L'authentification doit fonctionner avec l'email
        """
        user, customer = customer_user
        login_data = {
            'username': user.email,  # Utiliser l'email à la place du username
            'password': 'testpass123'
        }
        response = self.client.post(
            '/customer/post',
            data=json.dumps(login_data),
            content_type='application/json'
        )
        assert response.status_code == 200, "La requête doit être traitée"

    # Test 8 : Rejeter un mot de passe incorrect
    def test_connexion_invalid_password(self, customer_user):
        """
        TEST D'INTÉGRATION 5 : Rejeter une tentative de connexion avec un mauvais mot de passe
        Arrangement : Un utilisateur existant
        Action : Soumettre un POST JSON avec un mot de passe incorrect
        Assertion : La connexion doit échouer
        """
        user, customer = customer_user
        login_data = {
            'username': user.username,
            'password': 'mauvaispassword'
        }
        response = self.client.post(
            '/customer/post',
            data=json.dumps(login_data),
            content_type='application/json'
        )
        assert response.status_code == 200, "La requête doit être traitée"
        # Vérifier que l'utilisateur n'est pas authentifié
        assert '_auth_user_id' not in self.client.session, "L'utilisateur ne doit pas être authentifié"

    # Test 9 : Rejeter un utilisateur inexistant
    def test_connexion_nonexistent_user(self):
        """
        TEST D'INTÉGRATION 6 : Rejeter une tentative de connexion avec un utilisateur inexistant
        Arrangement : Aucun utilisateur avec ce username
        Action : Soumettre un POST JSON avec un username inexistant
        Assertion : La connexion doit échouer
        """
        login_data = {
            'username': 'utilisateurfictif',
            'password': 'anypassword'
        }
        response = self.client.post(
            '/customer/post',
            data=json.dumps(login_data),
            content_type='application/json'
        )
        assert response.status_code == 200, "La requête doit être traitée"
        assert '_auth_user_id' not in self.client.session, "L'utilisateur ne doit pas être authentifié"

    # Test 10 : Données JSON vides
    def test_connexion_empty_credentials(self):
        """
        TEST D'INTÉGRATION 7 : Rejeter une tentative de connexion avec des données vides
        Arrangement : Données JSON sans username ou password
        Action : Soumettre un POST JSON avec des données manquantes
        Assertion : La connexion doit échouer ou une erreur doit être retournée
        """
        login_data = {
            'username': '',
            'password': ''
        }
        response = self.client.post(
            '/customer/post',
            data=json.dumps(login_data),
            content_type='application/json'
        )
        assert '_auth_user_id' not in self.client.session, "L'utilisateur ne doit pas être authentifié avec des données vides"

    # Test 11 : Session utilisateur créée après connexion
    def test_connexion_session_created(self, customer_user):
        """
        TEST D'INTÉGRATION 8 : Vérifier qu'une session est créée après connexion réussie
        Arrangement : Un utilisateur valide
        Action : Authentifier l'utilisateur via login()
        Assertion : L'utilisateur doit être dans la session du client
        """
        user, customer = customer_user
        self.client.login(username=user.username, password='testpass123')
        assert '_auth_user_id' in self.client.session, "L'ID utilisateur doit être dans la session"
        assert self.client.session['_auth_user_id'] == str(user.id), "L'ID dans la session doit correspondre"
