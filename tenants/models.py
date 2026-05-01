from django.db import models
from django.conf import settings
from buildings.models import Unit


class Tenant(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tenants')
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True, blank=True, related_name='tenants')
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    nid = models.CharField(max_length=50, blank=True, null=True, verbose_name='NID')
    entry_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.pk:
            old = Tenant.objects.filter(pk=self.pk).first()
            if old and old.unit and old.unit != self.unit:
                old.unit.status = 'vacant'
                old.unit.save()

        if self.unit and self.is_active:
            self.unit.status = 'occupied'
            self.unit.save()
        elif self.unit and not self.is_active:
            self.unit.status = 'vacant'
            self.unit.save()

        super().save(*args, **kwargs)