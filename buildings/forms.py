from django import forms
from .models import Building, Unit


INPUT_CLASS = 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:border-gray-600 dark:text-white'


class BuildingForm(forms.ModelForm):
    class Meta:
        model = Building
        fields = ['name', 'address']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': 'Enter building name'
            }),
            'address': forms.Textarea(attrs={
                'class': INPUT_CLASS,
                'placeholder': 'Enter full address',
                'rows': 3
            }),
        }


class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ['building', 'flat_number', 'floor', 'monthly_rent', 'status']
        widgets = {
            'building': forms.Select(attrs={'class': INPUT_CLASS}),
            'flat_number': forms.TextInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': 'e.g., A-101'
            }),
            'floor': forms.NumberInput(attrs={
                'class': INPUT_CLASS,
                'min': 1
            }),
            'monthly_rent': forms.NumberInput(attrs={
                'class': INPUT_CLASS,
                'min': 0,
                'placeholder': 'Monthly rent in BDT'
            }),
            'status': forms.Select(attrs={'class': INPUT_CLASS}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['building'].queryset = Building.objects.filter(user=user)