"""
Views for Projects app
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q, Sum
from .models import Project, ProjectType, ProjectImage, ProjectFile
from .forms import ProjectForm, ProjectImageForm, ProjectFileForm
from services.google_sheets import GoogleSheetsService


@login_required
def project_list(request):
    """List all projects"""
    projects = Project.objects.select_related('customer', 'project_type').prefetch_related('images', 'payment_parts').all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        projects = projects.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(customer__name__icontains=search_query)
        )
    
    # Filter by status
    status_filter = request.GET.get('status', '')
    if status_filter:
        projects = projects.filter(status=status_filter)
    
    # Filter by project type
    type_filter = request.GET.get('type', '')
    if type_filter:
        projects = projects.filter(project_type_id=type_filter)
    
    # Pagination
    paginator = Paginator(projects, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Calculate totals
    total_budget = projects.aggregate(Sum('total_budget'))['total_budget__sum'] or 0
    total_revenue = projects.aggregate(Sum('total_revenue'))['total_revenue__sum'] or 0
    total_cost = projects.aggregate(Sum('total_cost'))['total_cost__sum'] or 0
    
    project_types = ProjectType.objects.all()
    
    context = {
        'page_obj': page_obj,
        'projects': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
        'type_filter': type_filter,
        'project_types': project_types,
        'total_budget': total_budget,
        'total_revenue': total_revenue,
        'total_cost': total_cost,
    }
    
    return render(request, 'projects/list.html', context)


@login_required
def project_detail(request, pk):
    """View project details"""
    project = get_object_or_404(
        Project.objects.select_related('customer', 'project_type')
        .prefetch_related('images', 'files', 'payment_parts'),
        pk=pk
    )
    
    context = {
        'project': project,
    }
    
    return render(request, 'projects/detail.html', context)


@login_required
def project_create(request):
    """Create new project"""
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save()
            messages.success(request, f'Project "{project.name}" created successfully!')
            
            # Sync to Google Sheets
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
                sheets_service.sync_projects(projects_data)
            except Exception as e:
                messages.warning(request, f'Project created but Google Sheets sync failed: {str(e)}')
            
            return redirect('projects:detail', pk=project.pk)
    else:
        form = ProjectForm()
    
    return render(request, 'projects/form.html', {'form': form, 'title': 'Create Project'})


@login_required
def project_update(request, pk):
    """Update project"""
    project = get_object_or_404(Project, pk=pk)
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save()
            project.calculate_profit_loss()
            messages.success(request, f'Project "{project.name}" updated successfully!')
            
            # Sync to Google Sheets
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
                sheets_service.sync_projects(projects_data)
            except Exception as e:
                messages.warning(request, f'Project updated but Google Sheets sync failed: {str(e)}')
            
            return redirect('projects:detail', pk=project.pk)
    else:
        form = ProjectForm(instance=project)
    
    return render(request, 'projects/form.html', {'form': form, 'project': project, 'title': 'Update Project'})


@login_required
def project_delete(request, pk):
    """Delete project"""
    project = get_object_or_404(Project, pk=pk)
    
    if request.method == 'POST':
        project_name = project.name
        project.delete()
        messages.success(request, f'Project "{project_name}" deleted successfully!')
        return redirect('projects:list')
    
    return render(request, 'projects/delete_confirm.html', {'project': project})
