"""
API Views for Payments app
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import models
from .models import PaymentPart
from .serializers import PaymentPartSerializer
from services.google_sheets import GoogleSheetsService


class PaymentPartViewSet(viewsets.ModelViewSet):
    """ViewSet for PaymentPart"""
    queryset = PaymentPart.objects.select_related('project', 'project__customer').all()
    serializer_class = PaymentPartSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = PaymentPart.objects.select_related('project', 'project__customer').all()
        project_id = self.request.query_params.get('project', None)
        if project_id:
            queryset = queryset.filter(project_id=project_id)
        return queryset
    
    def perform_create(self, serializer):
        """Create payment part and update project totals"""
        payment = serializer.save()
        project = payment.project
        project.total_revenue = project.payment_parts.aggregate(
            total=models.Sum('amount')
        )['total'] or 0.00
        project.calculate_profit_loss()
        project.save()
    
    @action(detail=True, methods=['post'])
    def sync_to_sheets(self, request, pk=None):
        """Sync payment to Google Sheets"""
        payment = self.get_object()
        try:
            sheets_service = GoogleSheetsService()
            payments_data = [{
                'id': payment.id,
                'project': payment.project.name,
                'amount': float(payment.amount),
                'payment_date': payment.payment_date.strftime('%Y-%m-%d'),
                'payment_method': payment.get_payment_method_display(),
                'reference_number': payment.reference_number or '',
                'notes': payment.notes or '',
                'created_at': payment.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at': payment.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            }]
            url = sheets_service.sync_payments(payments_data)
            return Response({
                'success': True,
                'message': 'Payment synced to Google Sheets successfully',
                'sheet_url': url
            })
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

