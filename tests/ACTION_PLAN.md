# ✅ Plan d'Action - Amélioration de la Suite de Tests

**Date:** 25 janvier 2026  
**Statut:** 60.6% de réussite (43/71 tests)  
**Objectif:** Atteindre 85%+ de réussite

---

## 🔥 PRIORITÉ 1 - BLOCKER (4-6 heures)

### 1.1 Corriger Déconnexion Unitaires
**Impact:** +2 tests passants (5→7)  
**Effort:** 1h  
**Fichier:** `_deconnexionTests/test_deconnexion_unitaire.py`

```python
# ❌ ACTUELLEMENT ÉCHOUE
def test_logout_authenticated_user(self, customer_user):
    # Logique apparemment correcte mais échoue
    
# ❌ ACTUELLEMENT ÉCHOUE  
def test_user_persists_after_logout(self, customer_user):
    # Vérification que l'utilisateur n'est pas supprimé après logout
```

**À faire:**
- [ ] Debugger les deux tests
- [ ] Vérifier la logique de logout dans les models/views
- [ ] Valider la création du fixture customer_user
- [ ] Ajouter des asserts plus clairs

**Ressource:** Vérifier [deconnexion_unitaire.py](file:///c:\Users\adams\Desktop\test_SK\cod_test\tests\_deconnexionTests\test_deconnexion_unitaire.py#L30-L50)

---

### 1.2 Implémenter API Panier CRUD
**Impact:** +5 tests passants (5→10)  
**Effort:** 2-3h  
**Fichiers:** 
- `_paniersTests/test_panier_integration.py` (tests)
- `client/views.py` (endpoints)

```python
# ❌ TESTS QUI ATTENDENT CES ENDPOINTS:
def test_add_product_to_cart(self):
    # POST /api/panier/add-product/

def test_delete_product_from_cart(self):
    # DELETE /api/panier/product/{id}/

def test_update_product_quantity_in_cart(self):
    # PUT /api/panier/product/{id}/quantity/

def test_add_coupon_to_cart(self):
    # POST /api/panier/add-coupon/

def test_unauthenticated_cart_session(self):
    # POST /api/panier/add-product/ (session-based)
```

**À faire:**
- [ ] Vérifier si les endpoints existent dans `client/urls.py`
- [ ] Si manquants, créer les vues Django correspondantes
- [ ] Ajouter les décorateurs `@login_required` appropriés
- [ ] Tester les réponses JSON
- [ ] Implémenter la logique session pour panier non authentifié

**Ressource:** Consulter [models.py](file:///c:\Users\adams\Desktop\test_SK\cod_test\client\models.py) pour comprendre la structure Panier

---

### 1.3 Fixer Logique Paiement
**Impact:** +6 tests passants (4→10)  
**Effort:** 2-3h  
**Fichiers:**
- `_paiementTests/test_paiement_integration.py` (tests)
- `customer/views.py` (logique paiement)

```python
# ❌ TESTS QUI ÉCHOUENT:
def test_payment_with_valid_amount(self):
    # Montant valide devrait être accepté

def test_payment_with_zero_amount(self):
    # 0 devrait être rejeté

def test_payment_with_negative_amount(self):
    # Négatif devrait être rejeté

def test_payment_requires_authentication(self):
    # Doit rediriger non authentifiés

def test_payment_confirmation_receipt(self):
    # Génération du reçu

def test_payment_history_for_customer(self):
    # Historique des paiements
```

**À faire:**
- [ ] Vérifier endpoint paiement dans `customer/urls.py`
- [ ] Implémenter validations montant (>0, format valide)
- [ ] Ajouter logique de création reçu
- [ ] Implémenter historique paiements (modèle + vue)
- [ ] Tester avec les coupons appliqués

**Ressource:** Vérifier models Customer pour structure paiements

---

## ⚠️ PRIORITÉ 2 - IMPORTANT (6-8 heures)

### 2.1 Upgrader Django vers 5.0
**Impact:** +14 tests passants (Pages) - 20%→100%  
**Effort:** 2-3h  
**Enjeu:** Bug Django 4.2.9 + Python 3.14 avec templates

```bash
# Dans le terminal:
pip install --upgrade django>=5.0
pip install --upgrade django-admin-interface
# ... upgrader autres packages Django
```

**À faire:**
- [ ] Sauvegarder backup requirements.txt
- [ ] Upgrader Django et dépendances
- [ ] Tester un test pages simple
- [ ] Si OK, relancer tous les tests
- [ ] Sinon, adapter les tests pour éviter contexte template

**Alternative:** Refactoriser tests pages pour ne pas vérifier le contexte template

---

### 2.2 Fixer Déconnexion Intégration
**Impact:** +5 tests passants (5→10)  
**Effort:** 1-2h  
**Fichiers:** `_deconnexionTests/test_deconnexion_integration.py`

```python
# ❌ TESTS QUI ÉCHOUENT:
def test_deconnexion_redirect_to_login(self):
    # Après logout, redirection vers login

def test_deconnexion_cannot_access_protected_pages(self):
    # Après logout, pas d'accès aux pages protégées

def test_login_page_accessible_after_logout(self):
    # Page login disponible après logout
```

**À faire:**
- [ ] Vérifier routes après logout (redirect_to='login')
- [ ] Vérifier les decorateurs @login_required
- [ ] Tester manuellement: se connecter → logout → vérifier redirects
- [ ] Adapter les tests si routes différentes

---

### 2.3 Corriger Inscription
**Impact:** +2 tests passants (8→10)  
**Effort:** 1h  

```python
# ❌ TESTS ÉCHOUANTS:
def test_inscription_page_accessible(self):
    # Page inscription ne se charge pas (template issue)

def test_inscription_duplicate_email(self):
    # Devrait rejeter email en doublon
```

**À faire:**
- [ ] Si template issue: attendre Django 5.0
- [ ] Sinon: ajouter validation duplicate email dans form/view

---

## 💚 PRIORITÉ 3 - NICE TO HAVE (4-6 heures)

### 3.1 Optimiser Tests Pages
**Impact:** Améliorer maintenabilité + éviter template context  
**Effort:** 2h

**À faire:**
- [ ] Refactoriser tests pages pour tester uniquement status codes
- [ ] Ajouter des tests sans vérification contexte template
- [ ] Documenter les limitations Django 4.2.9

---

### 3.2 Ajouter Tests Limites
**Impact:** Meilleure couverture  
**Effort:** 2h

```python
# Tests à ajouter:
- Panier avec très large quantité
- Paiement avec très grand montant
- Coupon avec réduction à 100%
- Email avec caractères spéciaux
- Username très long
```

---

## 🎯 Roadmap de Correction

```
Semaine 1 - BLOCKER (heures 1-6):
  Lundi:   Corriger déconnexion unitaires + panier CRUD
  Mardi:   Implémenter paiements complets
  Mercredi: Tester et itérer

Semaine 2 - IMPORTANT (heures 7-14):
  Jeudi:   Upgrader Django 5.0
  Vendredi: Corriger tests pages
  Samedi:  Implémenter déconnexion intégration

Semaine 3 - NICE TO HAVE (heures 15-20):
  Dimanche: Optimiser tests pages
  Lundi:   Ajouter tests limites
  Mardi:   Documenter et nettoyer
```

---

## 📊 Projection d'Amélioration

```
ACTUELLEMENT:
✅ 43/71 tests passent (60.6%)
├─ Unitaires:   12/14 (85.7%)
└─ Intégration: 31/57 (54.4%)

APRÈS PRIORITÉ 1 (6h):
✅ 50/71 tests passent (70.4%)
├─ Déconnexion: 5→7 tests (+2)
├─ Panier:      5→10 tests (+5)  
└─ Paiement:    4→6 tests (+2)

APRÈS PRIORITÉ 2 (6h):
✅ 65/71 tests passent (91.5%)
├─ Pages:       2→16 tests (+14 avec Django 5.0)
├─ Déconnexion: 7→10 tests (+3)
└─ Inscription: 8→10 tests (+2)

APRÈS PRIORITÉ 3 (2h):
✅ 71/71 tests passent (100%)
└─ Pages refactorisés si Django 5.0 pas dispo
```

---

## 🔧 Outils Recommandés

### Pour Debugger
```powershell
# Voir logs détaillés
..\env\Scripts\python.exe -m pytest tests\_deconnexionTests -v -s

# Voir traceback complet
..\env\Scripts\python.exe -m pytest tests\_paniersTests -vv --tb=long

# Tester un seul test
..\env\Scripts\python.exe -m pytest tests\_paniersTests\test_panier_integration.py::TestPanierIntegration::test_add_product_to_cart -v
```

### Pour Monitoring
```powershell
# HTML Report
..\env\Scripts\python.exe -m pytest tests\ --html=report.html --self-contained-html

# JSON Report
..\env\Scripts\python.exe -m pytest tests\ --json=report.json

# Voir quels tests sont lents
..\env\Scripts\python.exe -m pytest tests\ --durations=10
```

---

## 📚 Documentation à Consulter

| Fichier | Contenu |
|---------|---------|
| [TEST_REPORT.md](file:///c:\Users\adams\Desktop\test_SK\cod_test\tests\TEST_REPORT.md) | Rapport complet détaillé |
| [SUMMARY.md](file:///c:\Users\adams\Desktop\test_SK\cod_test\tests\SUMMARY.md) | Résumé exécutif |
| [DASHBOARD.md](file:///c:\Users\adams\Desktop\test_SK\cod_test\tests\DASHBOARD.md) | Tableau de bord visuel |
| [conftest.py](file:///c:\Users\adams\Desktop\test_SK\cod_test\tests\conftest.py) | Fixtures de base |
| [README.md](file:///c:\Users\adams\Desktop\test_SK\cod_test\tests\README.md) | Guide d'utilisation |

---

## ✨ Notes Importantes

### Bug Django 4.2.9 + Python 3.14
- **Symptôme:** `AttributeError: 'super' object has no attribute 'dicts'`
- **Cause:** Incompatibilité lors de copie contexte template pendant tests HTTP
- **Solution 1:** Upgrader Django 5.0+ (recommandé)
- **Solution 2:** Refactoriser tests pour éviter inspection contexte

### Structure des Tests
```
Chaque test a 7 parties:
1. Docstring avec description
2. Arrangement (setup données)
3. Action (executer code testé)
4. Assertion (vérifier résultat)
5. Assertions secondaires
6. Cleanup (automatique avec pytest)
7. Documentation des asserts
```

### Fixtures Disponibles
- `user_data` - Données utilisateur unique (UUID)
- `customer_user` - User + Customer profile
- `product_data` - Données produit
- `categorie_etablissement` - Catégorie commerce
- `categorie_produit` - Catégorie produit
- `promo_code` - Code promo (10% réduction)
- `panier` - Panier client
- `client` - Client HTTP Django

---

## 🎓 Prochaines Étapes

1. **Aujourd'hui:** Lire ce plan d'action
2. **Demain:** Commencer par Priorité 1
3. **Cette semaine:** Finir Priorité 1 + 2
4. **Semaine prochaine:** Priorité 3 + documentation finale

**Contact:** Si des questions sur les tests, consulter les fichiers de documentation ou le code des tests eux-mêmes qui contiennent des commentaires détaillés.

---

**Statut:** 🟡 EN COURS  
**Dernière mise à jour:** 25 janvier 2026  
**Prochaine révision:** Après completion Priorité 1
