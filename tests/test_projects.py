"""
Tests for Projects app
"""
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from projects.models import Project, ProjectType
from customers.models import Customer


class ProjectModelTest(TestCase):
    """Test Project model"""
    
    def setUp(self):
        self.customer = Customer.objects.create(
            name="Test Customer",
            email="test@example.com"
        )
        self.project_type = ProjectType.objects.create(
            name="Web Development"
        )
        self.project = Project.objects.create(
            name="Test Project",
            customer=self.customer,
            project_type=self.project_type,
            total_budget=10000.00,
            total_revenue=8000.00,
            total_cost=6000.00
        )
    
    def test_project_creation(self):
        """Test project creation"""
        self.assertEqual(self.project.name, "Test Project")
        self.assertEqual(self.project.customer, self.customer)
        self.assertEqual(self.project.total_budget, 10000.00)
    
    def test_calculate_profit_loss(self):
        """Test profit/loss calculation"""
        profit, loss = self.project.calculate_profit_loss()
        self.assertEqual(float(self.project.profit), 2000.00)
        self.assertEqual(float(self.project.loss), 0.00)
    
    def test_project_str(self):
        """Test project string representation"""
        self.assertEqual(str(self.project), "Test Project")


class ProjectViewTest(TestCase):
    """Test Project views"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.customer = Customer.objects.create(
            name="Test Customer",
            email="test@example.com"
        )
    
    def test_project_list_requires_login(self):
        """Test that project list requires login"""
        response = self.client.get(reverse('projects:list'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_project_list_authenticated(self):
        """Test project list for authenticated user"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('projects:list'))
        self.assertEqual(response.status_code, 200)
    
    def test_project_create_get(self):
        """Test project create form GET"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('projects:create'))
        self.assertEqual(response.status_code, 200)
    
    def test_project_create_post(self):
        """Test project creation POST"""
        self.client.login(username='testuser', password='testpass123')
        project_type = ProjectType.objects.create(name="Web Development")
        response = self.client.post(reverse('projects:create'), {
            'name': 'New Project',
            'customer': self.customer.id,
            'project_type': project_type.id,
            'status': 'planning',
            'total_budget': 5000.00,
            'total_revenue': 0.00,
            'total_cost': 0.00,
        })
        self.assertEqual(response.status_code, 302)  # Redirect after creation
        self.assertTrue(Project.objects.filter(name='New Project').exists())

