from django import forms
from .models import Patient
from datetime import date


class PatientForm(forms.ModelForm):

    class Meta:
        model = Patient
        fields = [
            'full_name',
            'dob',
            'email',
            'glucose',
            'haemoglobin',
            'cholesterol'
        ]

        widgets = {
            'dob': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),

            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'glucose': forms.NumberInput(attrs={'class': 'form-control'}),
            'haemoglobin': forms.NumberInput(attrs={'class': 'form-control'}),
            'cholesterol': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean_dob(self):
        dob = self.cleaned_data['dob']

        if dob and dob > date.today():
            raise forms.ValidationError("Date of birth cannot be future date")

        return dob