from django.db import models
from django.conf import settings


class Building(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='buildings')
    name = models.CharField(max_length=200)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @property
    def total_units(self):
        return self.units.count()

    @property
    def occupied_units(self):
        return self.units.filter(status='occupied').count()

    @property
    def vacant_units(self):
        return self.units.filter(status='vacant').count()

    @property
    def occupancy_rate(self):
        total = self.total_units
        if total == 0:
            return 0
        return round((self.occupied_units / total) * 100, 1)


class Unit(models.Model):
    STATUS_CHOICES = [
        ('vacant', 'Vacant'),
        ('booked', 'Booked'),
        ('occupied', 'Occupied'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='units')
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='units')
    flat_number = models.CharField(max_length=50)
    floor = models.PositiveIntegerField(default=1)
    monthly_rent = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='vacant')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['building', 'floor', 'flat_number']
        unique_together = ['building', 'flat_number']

    def __str__(self):
        return f"{self.flat_number} - {self.building.name}"

    @property
    def current_tenant(self):
        return self.tenants.filter(is_active=True).first()