from rest_framework import serializers
from .models import CashMovement


class CashMovementSerializer(serializers.ModelSerializer):
    movement_type_display = serializers.CharField(source='get_movement_type_display', read_only=True)

    class Meta:
        model = CashMovement
        fields = ['id', 'movement_type', 'movement_type_display', 'amount', 'comment', 'created_at']