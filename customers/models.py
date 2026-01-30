from django.db import models
from django.core.validators import EmailValidator
from django.urls import reverse


class Customer(models.Model):
    """Customer model to store customer information"""
    name = models.CharField(max_length=200)
    email = models.EmailField(validators=[EmailValidator()], blank=True, null=True)
    whatsapp_number = models.CharField(max_length=20, blank=True, null=True, help_text="WhatsApp number with country code")
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    company = models.CharField(max_length=200, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('customers:detail', kwargs={'pk': self.pk})

    def get_whatsapp_link(self):
        """Generate WhatsApp link for the customer"""
        if self.whatsapp_number:
            # Remove any non-digit characters except +
            clean_number = ''.join(c for c in self.whatsapp_number if c.isdigit() or c == '+')
            if not clean_number.startswith('+'):
                clean_number = '+' + clean_number
            return f"https://wa.me/{clean_number.replace('+', '')}"
        return None
