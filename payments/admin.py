"""
Admin configuration for Payments app
"""
from django.contrib import admin
from .models import PaymentPart


@admin.register(PaymentPart)
class PaymentPartAdmin(admin.ModelAdmin):
    list_display = ['project', 'amount', 'payment_date', 'payment_method', 'reference_number', 'created_at']
    list_filter = ['payment_method', 'payment_date', 'created_at']
    search_fields = ['project__name', 'reference_number', 'notes']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Payment Information', {
            'fields': ('project', 'amount', 'payment_date', 'payment_method')
        }),
        ('Additional', {
            'fields': ('reference_number', 'notes', 'created_at', 'updated_at')
        }),
    )
