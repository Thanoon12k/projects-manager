"""
Forms for Customers app
"""
from django import forms
from .models import Customer


class CustomerForm(forms.ModelForm):
    """Form for creating/editing customers"""
    
    class Meta:
        model = Customer
        fields = [
            'name', 'email', 'whatsapp_number', 'phone_number',
            'company', 'address', 'notes', 'is_active'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'whatsapp_number': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '+1234567890'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-input'}),
            'company': forms.TextInput(attrs={'class': 'form-input'}),
            'address': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}),
            'notes': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }

