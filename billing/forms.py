from django import forms
from .models import BillingSettings, Bill


INPUT_CLASS = 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:border-gray-600 dark:text-white'


class BillingSettingsForm(forms.ModelForm):
    class Meta:
        model = BillingSettings
        exclude = ['user', 'created_at', 'updated_at']
        widgets = {
            'electricity_rate': forms.NumberInput(attrs={'class': INPUT_CLASS, 'step': '0.01', 'min': '0'}),
            'gas_charge': forms.NumberInput(attrs={'class': INPUT_CLASS, 'step': '0.01', 'min': '0'}),
            'gas_distribution': forms.Select(attrs={'class': INPUT_CLASS}),
            'water_charge': forms.NumberInput(attrs={'class': INPUT_CLASS, 'step': '0.01', 'min': '0'}),
            'water_distribution': forms.Select(attrs={'class': INPUT_CLASS}),
            'service_charge': forms.NumberInput(attrs={'class': INPUT_CLASS, 'step': '0.01', 'min': '0'}),
            'service_distribution': forms.Select(attrs={'class': INPUT_CLASS}),
            'generator_charge': forms.NumberInput(attrs={'class': INPUT_CLASS, 'step': '0.01', 'min': '0'}),
            'generator_distribution': forms.Select(attrs={'class': INPUT_CLASS}),
            'guard_charge': forms.NumberInput(attrs={'class': INPUT_CLASS, 'step': '0.01', 'min': '0'}),
            'guard_distribution': forms.Select(attrs={'class': INPUT_CLASS}),
            'cleaner_charge': forms.NumberInput(attrs={'class': INPUT_CLASS, 'step': '0.01', 'min': '0'}),
            'cleaner_distribution': forms.Select(attrs={'class': INPUT_CLASS}),
            'due_day': forms.NumberInput(attrs={'class': INPUT_CLASS, 'min': '1', 'max': '28'}),
        }


class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = [
            'prev_electricity_reading', 'curr_electricity_reading',
            'gas', 'water', 'service_charge', 'generator', 'guard', 'cleaner',
            'extra', 'advance', 'notes'
        ]
        widgets = {
            'prev_electricity_reading': forms.NumberInput(attrs={'class': INPUT_CLASS, 'step': '0.01', 'min': '0'}),
            'curr_electricity_reading': forms.NumberInput(attrs={'class': INPUT_CLASS, 'step': '0.01', 'min': '0'}),
            'gas': forms.NumberInput(attrs={'class': INPUT_CLASS, 'step': '0.01', 'min': '0'}),
            'water': forms.NumberInput(attrs={'class': INPUT_CLASS, 'step': '0.01', 'min': '0'}),
            'service_charge': forms.NumberInput(attrs={'class': INPUT_CLASS, 'step': '0.01', 'min': '0'}),
            'generator': forms.NumberInput(attrs={'class': INPUT_CLASS, 'step': '0.01', 'min': '0'}),
            'guard': forms.NumberInput(attrs={'class': INPUT_CLASS, 'step': '0.01', 'min': '0'}),
            'cleaner': forms.NumberInput(attrs={'class': INPUT_CLASS, 'step': '0.01', 'min': '0'}),
            'extra': forms.NumberInput(attrs={'class': INPUT_CLASS, 'step': '0.01', 'min': '0'}),
            'advance': forms.NumberInput(attrs={'class': INPUT_CLASS, 'step': '0.01', 'min': '0'}),
            'notes': forms.Textarea(attrs={'class': INPUT_CLASS, 'rows': 3}),
        }


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = ['paid_amount', 'payment_method']
        widgets = {
            'paid_amount': forms.NumberInput(attrs={'class': INPUT_CLASS, 'step': '0.01', 'min': '0'}),
            'payment_method': forms.Select(attrs={'class': INPUT_CLASS}),
        }