"""
Views for Dashboard app
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta
from projects.models import Project, ProjectType
from customers.models import Customer
from payments.models import PaymentPart


@login_required
def dashboard(request):
    """Main dashboard view"""
    # Overall statistics
    total_projects = Project.objects.count()
    active_projects = Project.objects.filter(is_active=True).count()
    total_customers = Customer.objects.count()
    active_customers = Customer.objects.filter(is_active=True).count()
    
    # Financial statistics
    total_budget = Project.objects.aggregate(Sum('total_budget'))['total_budget__sum'] or 0
    total_revenue = Project.objects.aggregate(Sum('total_revenue'))['total_revenue__sum'] or 0
    total_cost = Project.objects.aggregate(Sum('total_cost'))['total_cost__sum'] or 0
    total_profit = Project.objects.aggregate(Sum('profit'))['profit__sum'] or 0
    total_loss = Project.objects.aggregate(Sum('loss'))['loss__sum'] or 0
    total_paid = PaymentPart.objects.aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Projects by status
    projects_by_status = Project.objects.values('status').annotate(
        count=Count('id')
    ).order_by('status')
    
    # Projects by type
    projects_by_type = ProjectType.objects.annotate(
        project_count=Count('project')
    ).order_by('-project_count')[:10]
    
    # Recent projects
    recent_projects = Project.objects.select_related('customer', 'project_type').order_by('-created_at')[:10]
    
    # Recent payments
    recent_payments = PaymentPart.objects.select_related('project', 'project__customer').order_by('-payment_date')[:10]
    
    # Upcoming deadlines (next 30 days)
    upcoming_deadlines = Project.objects.filter(
        deadline__gte=timezone.now().date(),
        deadline__lte=timezone.now().date() + timedelta(days=30),
        is_active=True
    ).select_related('customer').order_by('deadline')[:10]
    
    # Projects on hold
    on_hold_projects = Project.objects.filter(
        status='on_hold',
        is_active=True
    ).select_related('customer', 'project_type')[:10]
    
    # Top customers by project count
    top_customers = Customer.objects.annotate(
        project_count=Count('projects')
    ).filter(project_count__gt=0).order_by('-project_count')[:10]
    
    context = {
        # Statistics
        'total_projects': total_projects,
        'active_projects': active_projects,
        'total_customers': total_customers,
        'active_customers': active_customers,
        'total_budget': total_budget,
        'total_revenue': total_revenue,
        'total_cost': total_cost,
        'total_profit': total_profit,
        'total_loss': total_loss,
        'total_paid': total_paid,
        
        # Charts data
        'projects_by_status': projects_by_status,
        'projects_by_type': projects_by_type,
        
        # Lists
        'recent_projects': recent_projects,
        'recent_payments': recent_payments,
        'upcoming_deadlines': upcoming_deadlines,
        'on_hold_projects': on_hold_projects,
        'top_customers': top_customers,
    }
    
    return render(request, 'dashboard/home.html', context)
