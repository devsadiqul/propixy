from django.contrib import admin
from .models import BillingSettings, Bill


@admin.register(BillingSettings)
class BillingSettingsAdmin(admin.ModelAdmin):
    list_display = ['user', 'electricity_rate', 'gas_charge', 'water_charge', 'service_charge', 'due_day']
    list_filter = ['created_at']
    search_fields = ['user__email', 'user__name']


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ['unit', 'tenant', 'month', 'total', 'paid_amount', 'due_amount', 'payment_status', 'user']
    list_filter = ['payment_status', 'month']
    search_fields = ['unit__flat_number', 'tenant__name', 'user__email']
    ordering = ['-month', 'unit']