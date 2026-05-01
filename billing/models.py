from django.db import models
from django.conf import settings
from buildings.models import Unit
from tenants.models import Tenant


class BillingSettings(models.Model):
    DISTRIBUTION_CHOICES = [
        ('equal', 'Equal'),
        ('floor', 'Floor-based'),
        ('manual', 'Manual'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='billing_settings')
    electricity_rate = models.DecimalField(max_digits=10, decimal_places=2, default=8.0)
    gas_charge = models.DecimalField(max_digits=10, decimal_places=2, default=1000)
    gas_distribution = models.CharField(max_length=20, choices=DISTRIBUTION_CHOICES, default='equal')
    water_charge = models.DecimalField(max_digits=10, decimal_places=2, default=500)
    water_distribution = models.CharField(max_length=20, choices=DISTRIBUTION_CHOICES, default='equal')
    service_charge = models.DecimalField(max_digits=10, decimal_places=2, default=1500)
    service_distribution = models.CharField(max_length=20, choices=DISTRIBUTION_CHOICES, default='equal')
    generator_charge = models.DecimalField(max_digits=10, decimal_places=2, default=500)
    generator_distribution = models.CharField(max_length=20, choices=DISTRIBUTION_CHOICES, default='equal')
    guard_charge = models.DecimalField(max_digits=10, decimal_places=2, default=300)
    guard_distribution = models.CharField(max_length=20, choices=DISTRIBUTION_CHOICES, default='equal')
    cleaner_charge = models.DecimalField(max_digits=10, decimal_places=2, default=200)
    cleaner_distribution = models.CharField(max_length=20, choices=DISTRIBUTION_CHOICES, default='equal')
    due_day = models.PositiveIntegerField(default=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Billing Settings'

    def __str__(self):
        return f"Billing Settings for {self.user.email}"


class Bill(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('unpaid', 'Unpaid'),
        ('partial', 'Partial'),
        ('paid', 'Paid'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('bkash', 'bKash'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bills')
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='bills')
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='bills')
    month = models.CharField(max_length=20)

    rent = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    prev_electricity_reading = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    curr_electricity_reading = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    electricity_units = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    electricity_rate = models.DecimalField(max_digits=10, decimal_places=2, default=8.0)
    electricity_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    gas = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    water = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    service_charge = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    generator = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    guard = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    cleaner = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    extra = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    advance = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    due_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='unpaid')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, null=True, blank=True)
    payment_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-month', 'unit']
        unique_together = ['unit', 'month']

    def __str__(self):
        return f"Bill for {self.unit} - {self.month}"

    def calculate_total(self):
        self.electricity_units = self.curr_electricity_reading - self.prev_electricity_reading
        self.electricity_amount = self.electricity_units * self.electricity_rate

        self.total = (
            self.rent +
            self.electricity_amount +
            self.gas +
            self.water +
            self.service_charge +
            self.generator +
            self.guard +
            self.cleaner +
            self.extra -
            self.advance
        )
        self.due_amount = self.total - self.paid_amount

        if self.due_amount <= 0:
            self.payment_status = 'paid'
        elif self.paid_amount > 0:
            self.payment_status = 'partial'
        else:
            self.payment_status = 'unpaid'

    def save(self, *args, **kwargs):
        self.calculate_total()
        super().save(*args, **kwargs)