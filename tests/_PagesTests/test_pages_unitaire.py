"""
Tests unitaires pour les pages et routes
Tests de la disponibilité des pages et du rendu des templates
"""
import pytest
from django.test import Client
from django.contrib.auth.models import User
from customer.models import Customer


@pytest.mark.django_db
class TestPagesValidationUnitaire:
    """Tests unitaires validant l'accès aux pages"""

    def setup_method(self):
        """Initialiser le client HTTP pour chaque test"""
        self.client = Client()

    # Test 1 : Vérifier que l'URL reverse fonctionne pour la page d'accueil
    def test_home_page_url_reverse(self):
        """
        TEST UNITAIRE 1 : Vérifier que l'URL reverse pour la page d'accueil fonctionne
        Arrangement : Appel de reverse() pour le nom de la route 'index'
        Action : Vérifier que la fonction retourne une URL valide
        Assertion : L'URL doit être '/index' ou équivalent
        """
        from django.urls import reverse
        url = reverse('index')
        assert url is not None, "L'URL reverse doit retourner une URL"
        assert isinstance(url, str), "L'URL doit être une chaîne de caractères"

    # Test 2 : Vérifier que les URL reverse fonctionnent pour les autres pages
    def test_about_page_url_reverse(self):
        """
        TEST UNITAIRE 2 : Vérifier que l'URL reverse pour la page à propos fonctionne
        Arrangement : Appel de reverse() pour le nom de la route 'about'
        Action : Vérifier que la fonction retourne une URL valide
        Assertion : L'URL doit être '/a-propos' ou équivalent
        """
        from django.urls import reverse
        url = reverse('about')
        assert url is not None, "L'URL reverse doit retourner une URL"
        assert '/a-propos' in url or 'about' in url, "L'URL doit contenir 'a-propos' ou 'about'"
