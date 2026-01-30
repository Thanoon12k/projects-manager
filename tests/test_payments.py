"""
Tests for Payments app
"""
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from payments.models import PaymentPart
from projects.models import Project
from customers.models import Customer


class PaymentModelTest(TestCase):
    """Test PaymentPart model"""
    
    def setUp(self):
        self.customer = Customer.objects.create(
            name="Test Customer",
            email="test@example.com"
        )
        self.project = Project.objects.create(
            name="Test Project",
            customer=self.customer,
            total_budget=10000.00
        )
        self.payment = PaymentPart.objects.create(
            project=self.project,
            amount=2000.00,
            payment_date='2024-01-15',
            payment_method='bank_transfer'
        )
    
    def test_payment_creation(self):
        """Test payment creation"""
        self.assertEqual(self.payment.project, self.project)
        self.assertEqual(self.payment.amount, 2000.00)
        self.assertEqual(self.payment.payment_method, 'bank_transfer')
    
    def test_payment_str(self):
        """Test payment string representation"""
        self.assertIn("Test Project", str(self.payment))
        self.assertIn("2000.00", str(self.payment))


class PaymentViewTest(TestCase):
    """Test Payment views"""
    
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
        self.project = Project.objects.create(
            name="Test Project",
            customer=self.customer,
            total_budget=10000.00
        )
    
    def test_payment_list_requires_login(self):
        """Test that payment list requires login"""
        response = self.client.get(reverse('payments:list'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_payment_list_authenticated(self):
        """Test payment list for authenticated user"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('payments:list'))
        self.assertEqual(response.status_code, 200)
    
    def test_payment_create_post(self):
        """Test payment creation POST"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('payments:create'), {
            'project': self.project.id,
            'amount': 1500.00,
            'payment_date': '2024-01-20',
            'payment_method': 'bank_transfer',
        })
        self.assertEqual(response.status_code, 302)  # Redirect after creation
        self.assertTrue(PaymentPart.objects.filter(project=self.project, amount=1500.00).exists())

