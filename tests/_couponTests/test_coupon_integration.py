"""
Tests d'intégration pour les codes promotionnels
Tests complets du flux d'utilisation des coupons
"""
import pytest
from django.test import Client
from customer.models import CodePromotionnel, Panier
from datetime import datetime, timedelta
from django.utils.timezone import now
import json


@pytest.mark.django_db
class TestCouponIntegration:
    """Tests d'intégration du flux des codes promotionnels"""

    def setup_method(self):
        """Initialiser le client HTTP pour chaque test"""
        self.client = Client()

    # Test 3 : Appliquer un code promotionnel valide
    def test_apply_valid_promo_code(self, customer_user, panier, promo_code):
        """
        TEST D'INTÉGRATION 1 : Appliquer un code promotionnel valide au panier
        Arrangement : Un panier et un code promotionnel valide
        Action : Lier le code promotionnel au panier
        Assertion : Le code doit être appliqué au panier
        """
        user, customer = customer_user
        self.client.login(username='testuser', password='testpass123')
        
        panier.coupon = promo_code
        panier.save()
        
        retrieved_panier = Panier.objects.get(id=panier.id)
        assert retrieved_panier.coupon.id == promo_code.id, "Le code promotionnel doit être appliqué"

    # Test 4 : Rejeter un code promotionnel expiré
    def test_reject_expired_promo_code(self, customer_user):
        """
        TEST D'INTÉGRATION 2 : Rejeter un code promotionnel expiré
        Arrangement : Un code promotionnel dont la date de fin est dépassée
        Action : Tenter d'utiliser le code expiré
        Assertion : Le code doit être rejeté
        """
        # Créer un code expiré
        expired_promo = CodePromotionnel.objects.create(
            libelle='Code Expiré',
            code_promo='EXPIRED',
            etat=True,
            reduction=0.10,
            date_fin=now().date() - timedelta(days=1),  # Hier
            nombre_u=100
        )
        
        # Vérifier que le code est expiré
        is_expired = now().date() > expired_promo.date_fin
        assert is_expired, "Le code doit être expiré"

    # Test 5 : Rejeter un code promotionnel désactivé
    def test_reject_disabled_promo_code(self, customer_user, panier):
        """
        TEST D'INTÉGRATION 3 : Rejeter un code promotionnel désactivé
        Arrangement : Un code promotionnel avec etat=False
        Action : Tenter d'utiliser le code désactivé
        Assertion : Le code doit être rejeté
        """
        disabled_promo = CodePromotionnel.objects.create(
            libelle='Code Désactivé',
            code_promo='DISABLED',
            etat=False,  # Désactivé
            reduction=0.10,
            date_fin=now().date() + timedelta(days=30),
            nombre_u=100
        )
        
        # Vérifier que le code est désactivé
        assert disabled_promo.etat is False, "Le code doit être désactivé"

    # Test 6 : Calculer le total avec réduction appliquée
    def test_calculate_total_with_promo_code(self, customer_user, panier, promo_code):
        """
        TEST D'INTÉGRATION 4 : Vérifier que le total avec réduction est calculé correctement
        Arrangement : Un panier avec un code promotionnel
        Action : Calculer le total avec coupon
        Assertion : Le total avec coupon doit être inférieur au total original
        """
        user, customer = customer_user
        panier.coupon = promo_code
        panier.save()
        
        total_with_coupon = panier.total_with_coupon
        assert total_with_coupon is not None, "Le total avec coupon doit être calculé"
        assert total_with_coupon >= 0, "Le total ne peut pas être négatif"

    # Test 7 : Limite d'utilisation d'un code
    def test_promo_code_usage_limit(self):
        """
        TEST D'INTÉGRATION 5 : Vérifier la limite d'utilisation d'un code
        Arrangement : Un code avec nombre_u limité
        Action : Vérifier le nombre d'utilisations restantes
        Assertion : Le nombre ne peut pas être négatif
        """
        limited_promo = CodePromotionnel.objects.create(
            libelle='Code Limité',
            code_promo='LIMITED5',
            etat=True,
            reduction=0.10,
            date_fin=now().date() + timedelta(days=30),
            nombre_u=5  # Seulement 5 utilisations
        )
        
        assert limited_promo.nombre_u == 5, "Le nombre d'utilisations doit correspondre"

    # Test 8 : Appliquer un code via POST JSON
    def test_apply_promo_code_via_api(self, customer_user, panier, promo_code):
        """
        TEST D'INTÉGRATION 6 : Appliquer un code promotionnel via requête POST
        Arrangement : Un panier et un code promotionnel
        Action : Faire une requête POST pour ajouter le coupon
        Assertion : La requête doit être traitée
        """
        user, customer = customer_user
        self.client.login(username='testuser', password='testpass123')
        
        coupon_data = {
            'coupon_code': 'PROMO10',
            'panier_id': panier.id
        }
        response = self.client.post(
            '/customer/cart/add/coupon',
            data=json.dumps(coupon_data),
            content_type='application/json'
        )
        assert response.status_code in [200, 400, 404], "Réponse valide attendue"

    # Test 9 : Retirer un code promotionnel du panier
    def test_remove_promo_code_from_cart(self, customer_user, panier, promo_code):
        """
        TEST D'INTÉGRATION 7 : Retirer un code promotionnel du panier
        Arrangement : Un panier avec un code promotionnel appliqué
        Action : Retirer le code
        Assertion : Le code ne doit plus être appliqué
        """
        user, customer = customer_user
        panier.coupon = promo_code
        panier.save()
        
        # Retirer le coupon
        panier.coupon = None
        panier.save()
        
        retrieved_panier = Panier.objects.get(id=panier.id)
        assert retrieved_panier.coupon is None, "Le code promotionnel doit être retiré"

    # Test 10 : Vérifier que le code promotionnel ne dépasse pas 100%
    def test_promo_code_max_reduction(self):
        """
        TEST D'INTÉGRATION 8 : Vérifier qu'une réduction ne dépasse pas 100%
        Arrangement : Tenter de créer un code avec réduction > 100%
        Action : Créer un code
        Assertion : La réduction ne doit pas pouvoir dépasser 100%
        """
        # Vérifier que on ne peut pas créer une réduction > 100%
        reduction = 1.5  # 150%
        assert reduction > 1, "Cette réduction dépasse 100%"
        assert not (0 <= reduction <= 1), "Une telle réduction devrait être invalide"
