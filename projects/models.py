from django.db import models
from django.core.validators import URLValidator
from django.urls import reverse
from customers.models import Customer


class ProjectType(models.Model):
    """Project type/category model"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Project Type'
        verbose_name_plural = 'Project Types'

    def __str__(self):
        return self.name


class Project(models.Model):
    """Main project model"""
    STATUS_CHOICES = [
        ('planning', 'Planning'),
        ('in_progress', 'In Progress'),
        ('on_hold', 'On Hold'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    project_type = models.ForeignKey(ProjectType, on_delete=models.SET_NULL, null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='projects')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planning')
    
    # Financial fields
    total_budget = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    profit = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    loss = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    # Links
    live_url = models.URLField(validators=[URLValidator()], blank=True, null=True, help_text="Live project URL")
    repository_url = models.URLField(validators=[URLValidator()], blank=True, null=True, help_text="Repository URL")
    
    # Dates
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    deadline = models.DateField(blank=True, null=True)
    
    # Additional fields
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('projects:detail', kwargs={'pk': self.pk})

    def calculate_profit_loss(self):
        """Calculate profit or loss"""
        self.profit = max(0, self.total_revenue - self.total_cost)
        self.loss = max(0, self.total_cost - self.total_revenue)
        self.save(update_fields=['profit', 'loss'])
        return self.profit, self.loss

    @property
    def total_paid(self):
        """Calculate total amount paid from payment parts"""
        return self.payment_parts.aggregate(
            total=models.Sum('amount')
        )['total'] or 0.00


class ProjectImage(models.Model):
    """Project images model"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='projects/images/')
    caption = models.CharField(max_length=200, blank=True, null=True)
    is_primary = models.BooleanField(default=False, help_text="Primary image for project")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_primary', '-uploaded_at']
        verbose_name = 'Project Image'
        verbose_name_plural = 'Project Images'

    def __str__(self):
        return f"{self.project.name} - Image {self.id}"


class ProjectFile(models.Model):
    """Project files/documents model"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='projects/files/')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'Project File'
        verbose_name_plural = 'Project Files'

    def __str__(self):
        return f"{self.project.name} - {self.name}"
