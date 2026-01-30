"""
Admin configuration for Customers app
"""
from django.contrib import admin
from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'whatsapp_number', 'company', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'email', 'company', 'whatsapp_number']
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'whatsapp_number', 'phone_number')
        }),
        ('Company Information', {
            'fields': ('company', 'address')
        }),
        ('Additional', {
            'fields': ('notes', 'is_active', 'created_at', 'updated_at')
        }),
    )
    readonly_fields = ['created_at', 'updated_at']
