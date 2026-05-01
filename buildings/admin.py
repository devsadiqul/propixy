from django.contrib import admin
from .models import Building, Unit


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'user', 'total_units', 'occupancy_rate', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'address', 'user__email']
    ordering = ['-created_at']


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ['flat_number', 'building', 'floor', 'monthly_rent', 'status', 'user']
    list_filter = ['status', 'building']
    search_fields = ['flat_number', 'building__name', 'user__email']
    ordering = ['building', 'floor', 'flat_number']