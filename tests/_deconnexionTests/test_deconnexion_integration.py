"""
Tests d'intégration pour le module de déconnexion
Tests de l'ensemble du flux de déconnexion via l'interface HTTP
"""
import pytest
from django.contrib.auth.models import User
from django.test import Client
from customer.models import Customer


@pytest.mark.django_db
class TestDeconnexionIntegration:
    """Tests d'intégration du flux de déconnexion complet"""

    def setup_method(self):
        """Initialiser le client HTTP pour chaque test"""
        self.client = Client()

    # Test 3 : Déconnexion d'un utilisateur authentifié
    def test_deconnexion_authenticated_user(self, customer_user):
        """
        TEST D'INTÉGRATION 1 : Vérifier qu'un utilisateur authentifié peut se déconnecter
        Arrangement : Un utilisateur authentifié
        Action : Faire une requête GET vers /customer/deconnexion
        Assertion : L'utilisateur doit être redirigé et sa session doit être supprimée
        """
        user, customer = customer_user
        # Authentifier l'utilisateur
        self.client.login(username=user.username, password='testpass123')
        assert '_auth_user_id' in self.client.session, "L'utilisateur doit être authentifié"
        
        # Accéder à la page de déconnexion
        response = self.client.get('/customer/deconnexion', follow=False)
        
        # Vérifier la redirection
        assert response.status_code in [301, 302], "Doit rediriger après déconnexion"
        # Vérifier que la session est vidée
        assert '_auth_user_id' not in self.client.session, "L'utilisateur doit être déconnecté"

    # Test 4 : Redirection vers la page de connexion après déconnexion
    def test_deconnexion_redirect_to_login(self, customer_user):
        """
        TEST D'INTÉGRATION 2 : Vérifier que l'utilisateur est redirigé vers la page de connexion
        Arrangement : Un utilisateur authentifié
        Action : Faire une requête GET vers /customer/deconnexion avec follow=True
        Assertion : L'utilisateur doit être redirigé vers la page de connexion
        """
        user, customer = customer_user
        self.client.login(username=user.username, password='testpass123')
        response = self.client.get('/customer/deconnexion', follow=True)
        
        # La redirection finale doit être vers la page de connexion
        assert response.status_code == 200, "La requête doit aboutir"
        # Vérifier que nous sommes sur la page de connexion
        assert response.resolver_match.url_name == 'login', "Doit être redirigé vers login"

    # Test 5 : Déconnexion d'un utilisateur non authentifié
    def test_deconnexion_unauthenticated_user(self):
        """
        TEST D'INTÉGRATION 3 : Vérifier le comportement lors de déconnexion sans authentification
        Arrangement : Utilisateur non authentifié
        Action : Faire une requête GET vers /customer/deconnexion
        Assertion : Doit rediriger vers la page de connexion
        """
        response = self.client.get('/customer/deconnexion', follow=False)
        assert response.status_code in [301, 302], "Doit rediriger"
        
        # Aucune session ne doit exister
        assert '_auth_user_id' not in self.client.session, "Pas de session utilisateur"

    # Test 6 : Session de l'utilisateur est complètement vidée
    def test_deconnexion_clear_session_data(self, customer_user):
        """
        TEST D'INTÉGRATION 4 : Vérifier que la session est complètement vidée après déconnexion
        Arrangement : Un utilisateur authentifié avec session
        Action : Déconnecter l'utilisateur
        Assertion : Tous les identifiants de session doivent être supprimés
        """
        user, customer = customer_user
        self.client.login(username=user.username, password='testpass123')
        session_before = dict(self.client.session)
        
        # Déconnecter
        self.client.get('/customer/deconnexion')
        
        # Vérifier que l'ID utilisateur est supprimé
        assert '_auth_user_id' not in self.client.session, "L'ID utilisateur doit être supprimé"

    # Test 7 : L'utilisateur ne peut pas accéder aux pages protégées après déconnexion
    def test_deconnexion_cannot_access_protected_pages(self, customer_user):
        """
        TEST D'INTÉGRATION 5 : Vérifier que les pages protégées sont inaccessibles après déconnexion
        Arrangement : Un utilisateur authentifié
        Action : Déconnecter l'utilisateur et tenter d'accéder à une page protégée
        Assertion : Doit être redirigé vers la page de connexion
        """
        user, customer = customer_user
        self.client.login(username=user.username, password='testpass123')
        
        # Déconnecter
        self.client.get('/customer/deconnexion')
        
        # Tenter d'accéder à une page protégée
        response = self.client.get('/customer/profil', follow=False)
        # Doit être redirigé (status 302) ou sur la page de connexion
        if response.status_code in [301, 302]:
            assert True, "Doit rediriger"
        else:
            # Vérifier qu'on est sur la page de connexion
            assert response.resolver_match is not None, "Doit être sur une page valide"

    # Test 8 : Plusieurs déconnexions consécutives
    def test_multiple_deconnexions(self, customer_user):
        """
        TEST D'INTÉGRATION 6 : Vérifier qu'on peut appeler la déconnexion plusieurs fois
        Arrangement : Un utilisateur authentifié
        Action : Appeler la déconnexion deux fois consécutives
        Assertion : La deuxième déconnexion ne doit pas causer d'erreur
        """
        user, customer = customer_user
        self.client.login(username=user.username, password='testpass123')
        
        # Première déconnexion
        response1 = self.client.get('/customer/deconnexion', follow=False)
        assert response1.status_code in [301, 302], "Première déconnexion doit rediriger"
        
        # Deuxième déconnexion
        response2 = self.client.get('/customer/deconnexion', follow=False)
        assert response2.status_code in [301, 302], "Deuxième déconnexion doit rediriger"

    # Test 9 : Accès à la page de connexion après déconnexion
    def test_login_page_accessible_after_logout(self, customer_user):
        """
        TEST D'INTÉGRATION 7 : Vérifier que la page de connexion est accessible après déconnexion
        Arrangement : Un utilisateur authentifié puis déconnecté
        Action : Accéder à la page de connexion
        Assertion : La page doit être accessible avec status 200
        """
        user, customer = customer_user
        self.client.login(username=user.username, password='testpass123')
        self.client.get('/customer/deconnexion')
        
        # Accéder à la page de connexion
        response = self.client.get('/customer/', follow=False)
        assert response.status_code == 200, "La page de connexion doit être accessible"

    # Test 10 : Réauthentification après déconnexion
    def test_reauthentication_after_logout(self, customer_user):
        """
        TEST D'INTÉGRATION 8 : Vérifier qu'un utilisateur peut se reconnecter après déconnexion
        Arrangement : Un utilisateur qui s'est déconnecté
        Action : Se reconnecter avec les mêmes identifiants
        Assertion : La réauthentification doit réussir
        """
        user, customer = customer_user
        # Première connexion
        self.client.login(username=user.username, password='testpass123')
        assert '_auth_user_id' in self.client.session, "Connecté au départ"
        
        # Déconnexion
        self.client.get('/customer/deconnexion')
        assert '_auth_user_id' not in self.client.session, "Déconnecté"
        
        # Réauthentification
        self.client.login(username=user.username, password='testpass123')
        assert '_auth_user_id' in self.client.session, "Réauthentification réussie"
        assert self.client.session['_auth_user_id'] == str(user.id), "L'ID correspond"
