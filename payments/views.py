"""
Views for Payments app
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q, Sum
from .models import PaymentPart
from .forms import PaymentPartForm
from services.google_sheets import GoogleSheetsService


@login_required
def payment_list(request):
    """List all payment parts"""
    payments = PaymentPart.objects.select_related('project', 'project__customer').all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        payments = payments.filter(
            Q(project__name__icontains=search_query) |
            Q(reference_number__icontains=search_query) |
            Q(notes__icontains=search_query)
        )
    
    # Filter by project
    project_filter = request.GET.get('project', '')
    if project_filter:
        payments = payments.filter(project_id=project_filter)
    
    # Pagination
    paginator = Paginator(payments, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Calculate totals
    total_amount = payments.aggregate(Sum('amount'))['amount__sum'] or 0
    
    context = {
        'page_obj': page_obj,
        'payments': page_obj,
        'search_query': search_query,
        'project_filter': project_filter,
        'total_amount': total_amount,
    }
    
    return render(request, 'payments/list.html', context)


@login_required
def payment_detail(request, pk):
    """View payment details"""
    payment = get_object_or_404(
        PaymentPart.objects.select_related('project', 'project__customer'),
        pk=pk
    )
    
    context = {
        'payment': payment,
    }
    
    return render(request, 'payments/detail.html', context)


@login_required
def payment_create(request):
    """Create new payment part"""
    if request.method == 'POST':
        form = PaymentPartForm(request.POST)
        if form.is_valid():
            payment = form.save()
            
            # Update project totals
            project = payment.project
            project.total_revenue = payment.project.payment_parts.aggregate(
                total=Sum('amount')
            )['total'] or 0.00
            project.calculate_profit_loss()
            project.save()
            
            messages.success(request, f'Payment of ${payment.amount} recorded successfully!')
            
            # Sync to Google Sheets
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
                sheets_service.sync_payments(payments_data)
            except Exception as e:
                messages.warning(request, f'Payment recorded but Google Sheets sync failed: {str(e)}')
            
            return redirect('payments:detail', pk=payment.pk)
    else:
        form = PaymentPartForm()
    
    return render(request, 'payments/form.html', {'form': form, 'title': 'Create Payment'})


@login_required
def payment_update(request, pk):
    """Update payment part"""
    payment = get_object_or_404(PaymentPart, pk=pk)
    project = payment.project
    
    if request.method == 'POST':
        form = PaymentPartForm(request.POST, instance=payment)
        if form.is_valid():
            payment = form.save()
            
            # Update project totals
            project.total_revenue = project.payment_parts.aggregate(
                total=Sum('amount')
            )['total'] or 0.00
            project.calculate_profit_loss()
            project.save()
            
            messages.success(request, f'Payment updated successfully!')
            
            # Sync to Google Sheets
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
                sheets_service.sync_payments(payments_data)
            except Exception as e:
                messages.warning(request, f'Payment updated but Google Sheets sync failed: {str(e)}')
            
            return redirect('payments:detail', pk=payment.pk)
    else:
        form = PaymentPartForm(instance=payment)
    
    return render(request, 'payments/form.html', {'form': form, 'payment': payment, 'title': 'Update Payment'})


@login_required
def payment_delete(request, pk):
    """Delete payment part"""
    payment = get_object_or_404(PaymentPart, pk=pk)
    project = payment.project
    
    if request.method == 'POST':
        amount = payment.amount
        payment.delete()
        
        # Update project totals
        project.total_revenue = project.payment_parts.aggregate(
            total=Sum('amount')
        )['total'] or 0.00
        project.calculate_profit_loss()
        project.save()
        
        messages.success(request, f'Payment of ${amount} deleted successfully!')
        return redirect('payments:list')
    
    return render(request, 'payments/delete_confirm.html', {'payment': payment})
