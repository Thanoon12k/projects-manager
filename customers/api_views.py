"""
API Views for Customers app
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Customer
from .serializers import CustomerSerializer, CustomerListSerializer
from services.google_sheets import GoogleSheetsService
from services.whatsapp import WhatsAppService


class CustomerViewSet(viewsets.ModelViewSet):
    """ViewSet for Customer"""
    queryset = Customer.objects.prefetch_related('projects').all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return CustomerListSerializer
        return CustomerSerializer
    
    @action(detail=True, methods=['post'])
    def send_whatsapp(self, request, pk=None):
        """Send WhatsApp message to customer"""
        customer = self.get_object()
        message = request.data.get('message', '')
        
        if not message:
            return Response({
                'success': False,
                'error': 'Message is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if not customer.whatsapp_number:
            return Response({
                'success': False,
                'error': 'Customer does not have a WhatsApp number'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            whatsapp_service = WhatsAppService()
            result = whatsapp_service.send_message(customer.whatsapp_number, message)
            
            if result.get('success'):
                return Response({
                    'success': True,
                    'message': 'WhatsApp message sent successfully',
                    'details': result
                })
            else:
                return Response({
                    'success': False,
                    'error': result.get('error', 'Failed to send message')
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=True, methods=['post'])
    def sync_to_sheets(self, request, pk=None):
        """Sync customer to Google Sheets"""
        customer = self.get_object()
        try:
            sheets_service = GoogleSheetsService()
            customers_data = [{
                'id': customer.id,
                'name': customer.name,
                'email': customer.email or '',
                'whatsapp_number': customer.whatsapp_number or '',
                'phone_number': customer.phone_number or '',
                'company': customer.company or '',
                'address': customer.address or '',
                'notes': customer.notes or '',
                'created_at': customer.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at': customer.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            }]
            url = sheets_service.sync_customers(customers_data)
            return Response({
                'success': True,
                'message': 'Customer synced to Google Sheets successfully',
                'sheet_url': url
            })
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

