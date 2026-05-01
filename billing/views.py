from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import date
from .models import BillingSettings, Bill
from .forms import BillingSettingsForm, BillForm, PaymentForm
from buildings.models import Unit


@login_required
def billing_settings(request):
    billing_settings_obj, _ = BillingSettings.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = BillingSettingsForm(request.POST, instance=billing_settings_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Billing settings updated successfully!')
            return redirect('billing_settings')
    else:
        form = BillingSettingsForm(instance=billing_settings_obj)

    return render(request, 'billing/settings.html', {'form': form})


@login_required
def generate_bills(request):
    if request.method == 'POST':
        month = request.POST.get('month')
        if not month:
            messages.error(request, 'Please select a month.')
            return redirect('generate_bills')

        billing_settings_obj, _ = BillingSettings.objects.get_or_create(user=request.user)
        occupied_units = Unit.objects.filter(user=request.user, status='occupied')

        bills_created = 0
        bills_skipped = 0

        for unit in occupied_units:
            tenant = unit.current_tenant
            if not tenant:
                continue

            if Bill.objects.filter(unit=unit, month=month).exists():
                bills_skipped += 1
                continue

            bill = Bill(
                user=request.user,
                unit=unit,
                tenant=tenant,
                month=month,
                rent=unit.monthly_rent,
                electricity_rate=billing_settings_obj.electricity_rate,
                gas=billing_settings_obj.gas_charge,
                water=billing_settings_obj.water_charge,
                service_charge=billing_settings_obj.service_charge,
                generator=billing_settings_obj.generator_charge,
                guard=billing_settings_obj.guard_charge,
                cleaner=billing_settings_obj.cleaner_charge,
            )
            bill.save()
            bills_created += 1

        if bills_created > 0:
            messages.success(request, f'{bills_created} bills generated successfully!')
        if bills_skipped > 0:
            messages.warning(request, f'{bills_skipped} bills already existed and were skipped.')
        if bills_created == 0 and bills_skipped == 0:
            messages.info(request, 'No occupied units found to generate bills.')

        return redirect('bill_list')

    current_month = date.today().strftime('%Y-%m')
    return render(request, 'billing/generate.html', {'current_month': current_month})


@login_required
def bill_list(request):
    bills = Bill.objects.filter(user=request.user).select_related('unit', 'unit__building', 'tenant')

    month = request.GET.get('month')
    if month:
        bills = bills.filter(month=month)

    status = request.GET.get('status')
    if status:
        bills = bills.filter(payment_status=status)

    months = Bill.objects.filter(user=request.user).values_list('month', flat=True).distinct().order_by('-month')

    return render(request, 'billing/bill_list.html', {
        'bills': bills,
        'months': months,
        'selected_month': month,
        'selected_status': status,
    })


@login_required
def bill_edit(request, pk):
    bill = get_object_or_404(Bill, pk=pk, user=request.user)

    if request.method == 'POST':
        form = BillForm(request.POST, instance=bill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Bill updated successfully!')
            return redirect('bill_list')
    else:
        form = BillForm(instance=bill)

    return render(request, 'billing/bill_form.html', {
        'form': form,
        'bill': bill,
        'title': 'Edit Bill',
        'button_text': 'Update Bill',
    })


@login_required
def bill_payment(request, pk):
    bill = get_object_or_404(Bill, pk=pk, user=request.user)

    if request.method == 'POST':
        form = PaymentForm(request.POST, instance=bill)
        if form.is_valid():
            bill = form.save(commit=False)
            bill.payment_date = date.today()
            bill.save()
            messages.success(request, 'Payment recorded successfully!')
            return redirect('bill_list')
    else:
        form = PaymentForm(instance=bill)

    return render(request, 'billing/payment_form.html', {
        'form': form,
        'bill': bill,
    })


@login_required
def bill_receipt(request, pk):
    bill = get_object_or_404(Bill, pk=pk, user=request.user)
    return render(request, 'billing/receipt.html', {'bill': bill})


@login_required
def bill_delete(request, pk):
    bill = get_object_or_404(Bill, pk=pk, user=request.user)

    if request.method == 'POST':
        bill.delete()
        messages.success(request, 'Bill deleted successfully!')
        return redirect('bill_list')

    return render(request, 'billing/bill_confirm_delete.html', {'bill': bill})