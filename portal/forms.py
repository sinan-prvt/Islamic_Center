from django import forms
from .models import Donation, Expense, Program, Member, MonthlyDonor, Gallery

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['donor_name', 'monthly_donor', 'donation_type', 'amount', 'date', 'is_public']
        widgets = {
            'donor_name': forms.TextInput(attrs={'class': 'form-control'}),
            'monthly_donor': forms.Select(attrs={'class': 'form-control'}),
            'donation_type': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
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
        fields = ['name', 'phone', 'role', 'order', 'photo', 'instagram', 'whatsapp', 'facebook']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+91...'}),
            'role': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Monthly Donor, Committee Member'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'instagram': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://instagram.com/...'}),
            'whatsapp': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+91...'}),
            'facebook': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://facebook.com/...'}),
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

class GalleryForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = ['title', 'image', 'program']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'program': forms.Select(attrs={'class': 'form-control'}),
        }

from django.contrib.auth.models import User

class AdminUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=False, help_text="Leave blank to keep the current password.")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        # Ensure the user is an admin
        user.is_staff = True
        user.is_superuser = True
        if commit:
            user.save()
        return user
