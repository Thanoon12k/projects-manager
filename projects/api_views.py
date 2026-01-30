"""
API Views for Projects app
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Project, ProjectType, ProjectImage, ProjectFile
from .serializers import (
    ProjectSerializer, ProjectListSerializer, ProjectTypeSerializer,
    ProjectImageSerializer, ProjectFileSerializer
)
from services.google_sheets import GoogleSheetsService
from services.whatsapp import WhatsAppService


class ProjectTypeViewSet(viewsets.ModelViewSet):
    """ViewSet for ProjectType"""
    queryset = ProjectType.objects.all()
    serializer_class = ProjectTypeSerializer
    permission_classes = [IsAuthenticated]


class ProjectViewSet(viewsets.ModelViewSet):
    """ViewSet for Project"""
    queryset = Project.objects.select_related('customer', 'project_type').prefetch_related('images', 'files', 'payment_parts').all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ProjectListSerializer
        return ProjectSerializer
    
    @action(detail=True, methods=['post'])
    def calculate_profit_loss(self, request, pk=None):
        """Calculate and update profit/loss for a project"""
        project = self.get_object()
        profit, loss = project.calculate_profit_loss()
        return Response({
            'profit': float(profit),
            'loss': float(loss),
            'message': 'Profit and loss calculated successfully'
        })
    
    @action(detail=True, methods=['post'])
    def sync_to_sheets(self, request, pk=None):
        """Sync project to Google Sheets"""
        project = self.get_object()
        try:
            sheets_service = GoogleSheetsService()
            projects_data = [{
                'id': project.id,
                'name': project.name,
                'description': project.description or '',
                'project_type': project.project_type.name if project.project_type else '',
                'customer': project.customer.name,
                'status': project.get_status_display(),
                'total_budget': float(project.total_budget),
                'total_revenue': float(project.total_revenue),
                'total_cost': float(project.total_cost),
                'profit': float(project.profit),
                'loss': float(project.loss),
                'live_url': project.live_url or '',
                'repository_url': project.repository_url or '',
                'start_date': project.start_date.strftime('%Y-%m-%d') if project.start_date else '',
                'end_date': project.end_date.strftime('%Y-%m-%d') if project.end_date else '',
                'deadline': project.deadline.strftime('%Y-%m-%d') if project.deadline else '',
                'created_at': project.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at': project.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            }]
            url = sheets_service.sync_projects(projects_data)
            return Response({
                'success': True,
                'message': 'Project synced to Google Sheets successfully',
                'sheet_url': url
            })
        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=True, methods=['post'])
    def send_whatsapp_update(self, request, pk=None):
        """Send WhatsApp update to customer"""
        project = self.get_object()
        message = request.data.get('message', '')
        
        if not message:
            return Response({
                'success': False,
                'error': 'Message is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if not project.customer.whatsapp_number:
            return Response({
                'success': False,
                'error': 'Customer does not have a WhatsApp number'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            whatsapp_service = WhatsAppService()
            result = whatsapp_service.send_project_update(
                project.customer.whatsapp_number,
                project.name,
                message
            )
            
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


class ProjectImageViewSet(viewsets.ModelViewSet):
    """ViewSet for ProjectImage"""
    queryset = ProjectImage.objects.all()
    serializer_class = ProjectImageSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = ProjectImage.objects.all()
        project_id = self.request.query_params.get('project', None)
        if project_id:
            queryset = queryset.filter(project_id=project_id)
        return queryset


class ProjectFileViewSet(viewsets.ModelViewSet):
    """ViewSet for ProjectFile"""
    queryset = ProjectFile.objects.all()
    serializer_class = ProjectFileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = ProjectFile.objects.all()
        project_id = self.request.query_params.get('project', None)
        if project_id:
            queryset = queryset.filter(project_id=project_id)
        return queryset

