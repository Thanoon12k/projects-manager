"""
Forms for Payments app
"""
from django import forms
from .models import PaymentPart


class PaymentPartForm(forms.ModelForm):
    """Form for creating/editing payment parts"""
    
    class Meta:
        model = PaymentPart
        fields = [
            'project', 'amount', 'payment_date', 'payment_method',
            'reference_number', 'notes'
        ]
        widgets = {
            'project': forms.Select(attrs={'class': 'form-select'}),
            'amount': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01'}),
            'payment_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'payment_method': forms.Select(attrs={'class': 'form-select'}),
            'reference_number': forms.TextInput(attrs={'class': 'form-input'}),
            'notes': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}),
        }

