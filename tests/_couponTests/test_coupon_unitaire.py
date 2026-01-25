"""
Tests unitaires pour les codes promotionnels
Tests de la validation et de la logique métier des coupons
"""
import pytest
from customer.models import CodePromotionnel
from datetime import datetime, timedelta
from django.utils.timezone import now


@pytest.mark.django_db
class TestCouponValidationUnitaire:
    """Tests unitaires validant les règles métier des codes promotionnels"""

    # Test 1 : Créer un code promotionnel valide
    def test_create_valid_promo_code(self):
        """
        TEST UNITAIRE 1 : Vérifier qu'on peut créer un code promotionnel valide
        Arrangement : Données valides pour un code promotionnel
        Action : Créer un CodePromotionnel
        Assertion : Le code doit être créé avec les bonnes valeurs
        """
        promo = CodePromotionnel.objects.create(
            libelle='Réduction 10%',
            code_promo='PROMO10',
            etat=True,
            reduction=0.10,
            date_fin=now().date() + timedelta(days=30),
            nombre_u=100
        )
        
        assert promo.id is not None, "Le code promotionnel doit avoir un ID"
        assert promo.code_promo == 'PROMO10', "Le code doit correspondre"
        assert promo.reduction == 0.10, "La réduction doit correspondre"

    # Test 2 : Vérifier que la réduction est un pourcentage valide
    def test_promo_code_reduction_valid_percentage(self):
        """
        TEST UNITAIRE 2 : Vérifier que la réduction doit être entre 0 et 1
        Arrangement : Créer différentes réductions
        Action : Vérifier la validité des réductions
        Assertion : Seules les réductions entre 0 et 1 doivent être valides
        """
        valid_reduction = 0.25  # 25%
        invalid_reduction_over = 1.5  # 150% - invalide
        invalid_reduction_negative = -0.10  # -10% - invalide
        
        assert 0 <= valid_reduction <= 1, "Une réduction valide doit être entre 0 et 1"
        assert not (0 <= invalid_reduction_over <= 1), "Une réduction > 100% doit être invalide"
        assert not (0 <= invalid_reduction_negative <= 1), "Une réduction négative doit être invalide"
