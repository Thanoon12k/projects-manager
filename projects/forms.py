"""
Forms for Projects app
"""
from django import forms
from .models import Project, ProjectImage, ProjectFile


class ProjectForm(forms.ModelForm):
    """Form for creating/editing projects"""
    
    class Meta:
        model = Project
        fields = [
            'name', 'description', 'project_type', 'customer', 'status',
            'total_budget', 'total_revenue', 'total_cost',
            'live_url', 'repository_url',
            'start_date', 'end_date', 'deadline', 'notes', 'is_active'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4}),
            'project_type': forms.Select(attrs={'class': 'form-select'}),
            'customer': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'total_budget': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01'}),
            'total_revenue': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01'}),
            'total_cost': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01'}),
            'live_url': forms.URLInput(attrs={'class': 'form-input'}),
            'repository_url': forms.URLInput(attrs={'class': 'form-input'}),
            'start_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'deadline': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'notes': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }


class ProjectImageForm(forms.ModelForm):
    """Form for uploading project images"""
    
    class Meta:
        model = ProjectImage
        fields = ['image', 'caption', 'is_primary']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-input', 'accept': 'image/*'}),
            'caption': forms.TextInput(attrs={'class': 'form-input'}),
            'is_primary': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }


class ProjectFileForm(forms.ModelForm):
    """Form for uploading project files"""
    
    class Meta:
        model = ProjectFile
        fields = ['file', 'name', 'description']
        widgets = {
            'file': forms.FileInput(attrs={'class': 'form-input'}),
            'name': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3}),
        }

