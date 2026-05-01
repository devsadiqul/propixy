from django.contrib import admin
from .models import Tenant


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'unit', 'is_active', 'entry_date', 'user']
    list_filter = ['is_active', 'entry_date']
    search_fields = ['name', 'phone', 'nid', 'user__email']
    ordering = ['-created_at']