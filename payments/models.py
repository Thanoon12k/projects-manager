from django.db import models
from django.urls import reverse
from projects.models import Project


class PaymentPart(models.Model):
    """Payment parts model - tracks partial payments for projects"""
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('bank_transfer', 'Bank Transfer'),
        ('check', 'Check'),
        ('credit_card', 'Credit Card'),
        ('online', 'Online Payment'),
        ('other', 'Other'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='payment_parts')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_date = models.DateField()
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='bank_transfer')
    reference_number = models.CharField(max_length=100, blank=True, null=True, help_text="Transaction/Check reference")
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-payment_date', '-created_at']
        verbose_name = 'Payment Part'
        verbose_name_plural = 'Payment Parts'

    def __str__(self):
        return f"{self.project.name} - {self.amount} on {self.payment_date}"

    def get_absolute_url(self):
        return reverse('payments:detail', kwargs={'pk': self.pk})
