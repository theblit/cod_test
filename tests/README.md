# Documentation des Tests Pytest

## Structure des Tests

La suite de tests est organisée par fonctionnalités métier:

```
tests/
├── __init__.py
├── conftest.py                    # Configuration globale et fixtures
├── pytest.ini                      # Configuration pytest
│
├── _inscriptionTests/             # Tests d'inscription (10 tests)
│   ├── __init__.py
│   ├── test_inscription_unitaire.py      # 2 tests unitaires
│   └── test_inscription_integration.py   # 8 tests d'intégration
│
├── _connexionTests/               # Tests de connexion (10 tests)
│   ├── __init__.py
│   ├── test_connexion_unitaire.py        # 2 tests unitaires
│   └── test_connexion_integration.py     # 8 tests d'intégration
│
├── _deconnexionTests/             # Tests de déconnexion (10 tests)
│   ├── __init__.py
│   ├── test_deconnexion_unitaire.py      # 2 tests unitaires
│   └── test_deconnexion_integration.py   # 8 tests d'intégration
│
├── _paniersTests/                 # Tests du panier (10 tests)
│   ├── __init__.py
│   ├── test_panier_unitaire.py           # 2 tests unitaires
│   └── test_panier_integration.py        # 8 tests d'intégration
│
├── _paiementTests/                # Tests de paiement (10 tests)
│   ├── __init__.py
│   ├── test_paiement_unitaire.py         # 2 tests unitaires
│   └── test_paiement_integration.py      # 8 tests d'intégration
│
├── _PagesTests/                   # Tests des pages/routes (10 tests)
│   ├── __init__.py
│   ├── test_pages_unitaire.py            # 2 tests unitaires
│   └── test_pages_integration.py         # 8 tests d'intégration
│
└── _couponTests/                  # Tests des codes promotionnels (10 tests)
    ├── __init__.py
    ├── test_coupon_unitaire.py           # 2 tests unitaires
    └── test_coupon_integration.py        # 8 tests d'intégration
```

## Total des Tests

- **Fixtures**: 8 fixtures partagées dans `conftest.py`
- **Dossiers de tests**: 8 suites de tests
- **Tests par suite**: 10 tests (2 unitaires + 8 intégration)
- **Total**: 80 tests

## Fixtures Disponibles

Disponibles dans `conftest.py`:

### 1. `user_data`
Données utilisateur standard pour les tests
```python
{
    'username': 'testuser',
    'email': 'testuser@example.com',
    'password': 'testpass123',
    'first_name': 'Test',
    'last_name': 'User'
}
```

### 2. `customer_user`
Crée un utilisateur et son profil Customer
```python
user, customer = customer_user
```

### 3. `product_data`
Données produit de test

### 4. `categorie_etablissement`
Catégorie d'établissement créée

### 5. `categorie_produit`
Catégorie de produit créée

### 6. `promo_code`
Code promotionnel valide créé avec réduction 10%

### 7. `panier`
Panier d'un client créé

### 8. `client`
Client HTTP Django pour les tests

## Comment Exécuter les Tests

### Exécuter tous les tests
```bash
python -m pytest tests -v
```

### Exécuter une suite spécifique
```bash
python -m pytest tests/_inscriptionTests -v
python -m pytest tests/_connexionTests -v
python -m pytest tests/_paniersTests -v
```

### Exécuter un test spécifique
```bash
python -m pytest tests/_inscriptionTests/test_inscription_unitaire.py::TestInscriptionValidationUnitaire::test_email_validation_valid_email -v
```

### Exécuter avec options utiles
```bash
# Affichage des print statements
python -m pytest tests -v -s

# Rapport d'erreur court
python -m pytest tests -v --tb=short

# Exécuter les tests qui ont échoué
python -m pytest tests --lf

# Exécuter les tests contenant "inscription"
python -m pytest tests -k "inscription" -v

# Générer un rapport HTML
python -m pytest tests -v --html=report.html
```

## Structure des Tests

### Tests Unitaires
- Testent une fonction ou méthode isolée
- Aucune dépendance HTTP
- Rapidement exécutables
- Focalisés sur la logique métier

### Tests d'Intégration
- Testent le flux complet HTTP
- Utilisent le client test Django
- Testent les redirections et réponses
- Valident la logique end-to-end

## Conventions de Nommage

### Fichiers
- `test_*.py` : Fichiers de test
- `conftest.py` : Configuration et fixtures

### Classes
- `Test*Unitaire` : Tests unitaires
- `Test*Integration` : Tests d'intégration

### Méthodes
- `test_*` : Méthodes de test
- Pattern: `test_feature_description`

## Commentaires dans les Tests

Chaque test contient 3 sections commentées:

1. **Arrangement** : Préparation des données
2. **Action** : Exécution du code à tester
3. **Assertion** : Vérification des résultats

Exemple:
```python
def test_inscription_valid_user(self):
    """
    TEST D'INTÉGRATION 3 : Description du test
    Arrangement : Préparation...
    Action : Exécution...
    Assertion : Vérification...
    """
```

## Configuration Django

- `DJANGO_SETTINGS_MODULE` : `cooldeal.settings`
- Base de données : SQLite pour les tests
- Marker `@pytest.mark.django_db` : Accès à la base de données

## Dépendances

- Django 4.2.9
- pytest
- pytest-django

Pour installer pytest-django:
```bash
pip install pytest-django
```

## Notes Importantes

1. **Base de données** : Les tests utilisent une base de données de test séparée
2. **Transactions** : Chaque test est isolé dans une transaction
3. **Fixtures** : Sont créées et détruites automatiquement
4. **Client HTTP** : Simulé par Django TestClient

## Développement Futur

Envisager l'ajout de:
- Tests de performance
- Tests de sécurité (CSRF, SQL injection, etc.)
- Tests de permissions et authentification avancée
- Tests de cache
- Tests des middlewares personnalisés
