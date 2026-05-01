from django import forms
from django.db.models import Q
from .models import Tenant
from buildings.models import Unit

INPUT_CLASS = 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:border-gray-600 dark:text-white'


class TenantForm(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = ['name', 'phone', 'nid', 'entry_date', 'unit', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': 'Enter tenant name'
            }),
            'phone': forms.TextInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': '01XXXXXXXXX'
            }),
            'nid': forms.TextInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': 'National ID (optional)'
            }),
            'entry_date': forms.DateInput(attrs={
                'class': INPUT_CLASS,
                'type': 'date'
            }),
            'unit': forms.Select(attrs={'class': INPUT_CLASS}),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'h-5 w-5 text-blue-600 border-gray-300 rounded focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600'
            }),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            instance = self.instance if self.instance.pk else None
            if instance and instance.unit:
                self.fields['unit'].queryset = Unit.objects.filter(
                    user=user
                ).filter(
                    Q(status='vacant') | Q(pk=instance.unit.pk)
                )
            else:
                self.fields['unit'].queryset = Unit.objects.filter(
                    user=user,
                    status='vacant'
                )
        self.fields['unit'].required = False
        self.fields['unit'].empty_label = "No Unit Assigned"