"""
Configuration globale pour pytest
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cooldeal.settings')
django.setup()

from django.conf import settings

# Ajouter testserver à ALLOWED_HOSTS après l'initialisation de Django
if 'testserver' not in settings.ALLOWED_HOSTS:
    settings.ALLOWED_HOSTS.append('testserver')
if 'localhost' not in settings.ALLOWED_HOSTS:
    settings.ALLOWED_HOSTS.append('localhost')
if '127.0.0.1' not in settings.ALLOWED_HOSTS:
    settings.ALLOWED_HOSTS.append('127.0.0.1')

import pytest
from django.contrib.auth.models import User
from customer.models import Customer, Panier, CodePromotionnel
from shop.models import Produit, Etablissement, CategorieEtablissement, CategorieProduit
from cities_light.models import City
import uuid


@pytest.fixture
def user_data():
    """Fixture fournissant des données utilisateur de test avec username unique"""
    unique_id = str(uuid.uuid4())[:8]
    return {
        'username': f'testuser_{unique_id}',
        'email': f'testuser_{unique_id}@example.com',
        'password': 'testpass123',
        'first_name': 'Test',
        'last_name': 'User'
    }


@pytest.fixture
def customer_user(db, user_data):
    """Fixture créant un utilisateur et son profil client avec données uniques"""
    # Nettoyer d'abord les utilisateurs existants avec le même email
    User.objects.filter(email=user_data['email']).delete()
    
    user = User.objects.create_user(
        username=user_data['username'],
        email=user_data['email'],
        password=user_data['password'],
        first_name=user_data['first_name'],
        last_name=user_data['last_name']
    )
    customer = Customer.objects.create(
        user=user,
        adresse='123 Rue de Test',
        contact_1='+1234567890'
    )
    return user, customer


@pytest.fixture
def product_data():
    """Fixture fournissant des données produit de test"""
    return {
        'nom': 'Produit Test',
        'description': 'Description du produit test',
        'description_deal': 'Deal description',
        'prix': 10000.0,
        'prix_promotionnel': 8000.0,
        'quantite': 50
    }


@pytest.fixture
def categorie_etablissement(db):
    """Fixture créant une catégorie d'établissement"""
    return CategorieEtablissement.objects.create(
        nom='Catégorie Test',
        description='Description de la catégorie de test'
    )


@pytest.fixture
def categorie_produit(db, categorie_etablissement):
    """Fixture créant une catégorie de produit"""
    return CategorieProduit.objects.create(
        nom='Catégorie Produit Test',
        description='Description de la catégorie produit',
        categorie=categorie_etablissement
    )


@pytest.fixture
def promo_code(db):
    """Fixture créant un code promotionnel"""
    from datetime import datetime, timedelta
    from django.utils.timezone import now
    return CodePromotionnel.objects.create(
        libelle='Code10',
        code_promo='PROMO10',
        etat=True,
        reduction=0.10,
        date_fin=now().date() + timedelta(days=30),
        nombre_u=100
    )


@pytest.fixture
def panier(db, customer_user):
    """Fixture créant un panier pour un client"""
    user, customer = customer_user
    return Panier.objects.create(
        customer=customer,
        status=True
    )


@pytest.fixture
def client(db):
    """Fixture fournissant un client HTTP de test avec ALLOWED_HOSTS configuré"""
    from django.test import Client
    return Client()
