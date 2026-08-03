from django import forms
from .models import Donation, Expense, Program, Member, MonthlyDonor

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['donor_name', 'donation_type', 'amount', 'is_public']
        widgets = {
            'donor_name': forms.TextInput(attrs={'class': 'form-control', 'id': 'id_donor_name'}),
            'donation_type': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'is_public': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['title', 'category', 'amount', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.TextInput(attrs={'class': 'form-control', 'list': 'categoryOptions', 'placeholder': 'Select or type category...'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = ['title', 'program_type', 'date', 'time', 'venue', 'description', 'is_upcoming', 'banner']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'program_type': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'venue': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_upcoming': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'banner': forms.FileInput(attrs={'class': 'form-control'}),
        }

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['name', 'phone', 'role', 'order', 'photo']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+91...'}),
            'role': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Monthly Donor, Committee Member'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }

class MonthlyDonorForm(forms.ModelForm):
    class Meta:
        model = MonthlyDonor
        fields = ['name', 'phone', 'monthly_commitment', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+91...'}),
            'monthly_commitment': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
