"""
Tests for Customers app
"""
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from customers.models import Customer


class CustomerModelTest(TestCase):
    """Test Customer model"""
    
    def setUp(self):
        self.customer = Customer.objects.create(
            name="John Doe",
            email="john@example.com",
            whatsapp_number="+1234567890"
        )
    
    def test_customer_creation(self):
        """Test customer creation"""
        self.assertEqual(self.customer.name, "John Doe")
        self.assertEqual(self.customer.email, "john@example.com")
        self.assertEqual(self.customer.whatsapp_number, "+1234567890")
    
    def test_get_whatsapp_link(self):
        """Test WhatsApp link generation"""
        link = self.customer.get_whatsapp_link()
        self.assertIsNotNone(link)
        self.assertIn('wa.me', link)
    
    def test_customer_str(self):
        """Test customer string representation"""
        self.assertEqual(str(self.customer), "John Doe")


class CustomerViewTest(TestCase):
    """Test Customer views"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_customer_list_requires_login(self):
        """Test that customer list requires login"""
        response = self.client.get(reverse('customers:list'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_customer_list_authenticated(self):
        """Test customer list for authenticated user"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('customers:list'))
        self.assertEqual(response.status_code, 200)
    
    def test_customer_create_get(self):
        """Test customer create form GET"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('customers:create'))
        self.assertEqual(response.status_code, 200)
    
    def test_customer_create_post(self):
        """Test customer creation POST"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('customers:create'), {
            'name': 'Jane Doe',
            'email': 'jane@example.com',
            'whatsapp_number': '+1234567890',
        })
        self.assertEqual(response.status_code, 302)  # Redirect after creation
        self.assertTrue(Customer.objects.filter(name='Jane Doe').exists())

