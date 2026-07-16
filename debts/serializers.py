from rest_framework import serializers
from .models import Debtor, DebtPayment


class DebtPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DebtPayment  
        fields = ['id', 'amount', 'comment', 'created_at']


class DebtorSerializer(serializers.ModelSerializer):
    current_balance = serializers.SerializerMethodField()
    payments = DebtPaymentSerializer(many=True, read_only=True)

    class Meta:
        model = Debtor
        fields = ['id', 'name', 'phone', 'comment', 'initial_debt', 'current_balance', 'payments', 'created_at']

    def get_current_balance(self, obj):
        return float(obj.current_balance)