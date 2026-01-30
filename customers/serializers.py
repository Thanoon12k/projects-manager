"""
Serializers for Customers app
"""
from rest_framework import serializers
from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    """Serializer for Customer"""
    whatsapp_link = serializers.SerializerMethodField()
    projects_count = serializers.SerializerMethodField()
    total_projects_value = serializers.SerializerMethodField()
    
    class Meta:
        model = Customer
        fields = [
            'id', 'name', 'email', 'whatsapp_number', 'whatsapp_link',
            'phone_number', 'company', 'address', 'notes',
            'projects_count', 'total_projects_value',
            'created_at', 'updated_at', 'is_active'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_whatsapp_link(self, obj):
        return obj.get_whatsapp_link()
    
    def get_projects_count(self, obj):
        return obj.projects.count()
    
    def get_total_projects_value(self, obj):
        return sum(project.total_budget for project in obj.projects.all())


class CustomerListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for customer lists"""
    projects_count = serializers.SerializerMethodField()
    whatsapp_link = serializers.SerializerMethodField()
    
    class Meta:
        model = Customer
        fields = [
            'id', 'name', 'email', 'whatsapp_number', 'whatsapp_link',
            'phone_number', 'company', 'projects_count', 'created_at', 'is_active'
        ]
    
    def get_projects_count(self, obj):
        return obj.projects.count()
    
    def get_whatsapp_link(self, obj):
        return obj.get_whatsapp_link()

