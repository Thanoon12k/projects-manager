"""
Serializers for Payments app
"""
from rest_framework import serializers
from .models import PaymentPart


class PaymentPartSerializer(serializers.ModelSerializer):
    """Serializer for PaymentPart"""
    project_name = serializers.CharField(source='project.name', read_only=True)
    customer_name = serializers.CharField(source='project.customer.name', read_only=True)
    
    class Meta:
        model = PaymentPart
        fields = [
            'id', 'project', 'project_name', 'customer_name',
            'amount', 'payment_date', 'payment_method',
            'reference_number', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

