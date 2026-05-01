from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Tenant
from .forms import TenantForm
from buildings.models import Unit


@login_required
def tenant_list(request):
    """List all tenants"""
    tenants = Tenant.objects.filter(user=request.user).select_related('unit', 'unit__building')
    return render(request, 'tenants/tenant_list.html', {'tenants': tenants})


@login_required
def tenant_create(request):
    """Create a new tenant"""
    if request.method == 'POST':
        form = TenantForm(request.POST, user=request.user)
        if form.is_valid():
            tenant = form.save(commit=False)
            tenant.user = request.user
            tenant.save()
            messages.success(request, f'Tenant "{tenant.name}" added successfully!')
            return redirect('tenant_list')
    else:
        form = TenantForm(user=request.user)
    
    return render(request, 'tenants/tenant_form.html', {
        'form': form,
        'title': 'Add Tenant',
        'button_text': 'Add Tenant'
    })


@login_required
def tenant_edit(request, pk):
    """Edit a tenant"""
    tenant = get_object_or_404(Tenant, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = TenantForm(request.POST, instance=tenant, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Tenant "{tenant.name}" updated successfully!')
            return redirect('tenant_list')
    else:
        form = TenantForm(instance=tenant, user=request.user)
    
    return render(request, 'tenants/tenant_form.html', {
        'form': form,
        'tenant': tenant,
        'title': 'Edit Tenant',
        'button_text': 'Update Tenant'
    })


@login_required
def tenant_delete(request, pk):
    """Delete a tenant"""
    tenant = get_object_or_404(Tenant, pk=pk, user=request.user)
    
    if request.method == 'POST':
        # If tenant had a unit, set it back to vacant
        if tenant.unit:
            tenant.unit.status = 'vacant'
            tenant.unit.save()
        
        name = tenant.name
        tenant.delete()
        messages.success(request, f'Tenant "{name}" removed successfully!')
        return redirect('tenant_list')
    
    return render(request, 'tenants/tenant_confirm_delete.html', {'tenant': tenant})
