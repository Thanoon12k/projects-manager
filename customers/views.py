"""
Views for Customers app
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Customer
from .forms import CustomerForm
from services.google_sheets import GoogleSheetsService
from services.whatsapp import WhatsAppService


@login_required
def customer_list(request):
    """List all customers"""
    customers = Customer.objects.prefetch_related('projects').all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        customers = customers.filter(
            Q(name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(company__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(customers, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'customers': page_obj,
        'search_query': search_query,
    }
    
    return render(request, 'customers/list.html', context)


@login_required
def customer_detail(request, pk):
    """View customer details"""
    customer = get_object_or_404(
        Customer.objects.prefetch_related('projects'),
        pk=pk
    )
    
    context = {
        'customer': customer,
    }
    
    return render(request, 'customers/detail.html', context)


@login_required
def customer_create(request):
    """Create new customer"""
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save()
            messages.success(request, f'Customer "{customer.name}" created successfully!')
            
            # Sync to Google Sheets
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
                sheets_service.sync_customers(customers_data)
            except Exception as e:
                messages.warning(request, f'Customer created but Google Sheets sync failed: {str(e)}')
            
            return redirect('customers:detail', pk=customer.pk)
    else:
        form = CustomerForm()
    
    return render(request, 'customers/form.html', {'form': form, 'title': 'Create Customer'})


@login_required
def customer_update(request, pk):
    """Update customer"""
    customer = get_object_or_404(Customer, pk=pk)
    
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            customer = form.save()
            messages.success(request, f'Customer "{customer.name}" updated successfully!')
            
            # Sync to Google Sheets
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
                sheets_service.sync_customers(customers_data)
            except Exception as e:
                messages.warning(request, f'Customer updated but Google Sheets sync failed: {str(e)}')
            
            return redirect('customers:detail', pk=customer.pk)
    else:
        form = CustomerForm(instance=customer)
    
    return render(request, 'customers/form.html', {'form': form, 'customer': customer, 'title': 'Update Customer'})


@login_required
def customer_delete(request, pk):
    """Delete customer"""
    customer = get_object_or_404(Customer, pk=pk)
    
    if request.method == 'POST':
        customer_name = customer.name
        customer.delete()
        messages.success(request, f'Customer "{customer_name}" deleted successfully!')
        return redirect('customers:list')
    
    return render(request, 'customers/delete_confirm.html', {'customer': customer})


@login_required
def send_whatsapp(request, pk):
    """Send WhatsApp message to customer"""
    customer = get_object_or_404(Customer, pk=pk)
    
    if request.method == 'POST':
        message = request.POST.get('message', '')
        
        if not message:
            messages.error(request, 'Message is required!')
            return redirect('customers:detail', pk=customer.pk)
        
        if not customer.whatsapp_number:
            messages.error(request, 'Customer does not have a WhatsApp number!')
            return redirect('customers:detail', pk=customer.pk)
        
        try:
            whatsapp_service = WhatsAppService()
            result = whatsapp_service.send_message(customer.whatsapp_number, message)
            
            if result.get('success'):
                messages.success(request, 'WhatsApp message sent successfully!')
            else:
                messages.error(request, f'Failed to send message: {result.get("error", "Unknown error")}')
        except Exception as e:
            messages.error(request, f'Error sending message: {str(e)}')
        
        return redirect('customers:detail', pk=customer.pk)
    
    return render(request, 'customers/send_whatsapp.html', {'customer': customer})
