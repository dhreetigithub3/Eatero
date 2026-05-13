from django import forms
from .models import Customer
import re

class CustomerSignupForm(forms.ModelForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm your password'}),
        label="Confirm Password"
    )

    class Meta:
        model = Customer
        fields = ['username', 'email', 'mobile', 'address', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Choose a username'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Create a password'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter 10-digit mobile', 'pattern': '[0-9]{10}'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter your delivery address', 'rows': 3}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")
        
        return cleaned_data
    
    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')
        if not re.match(r'^\d{10}$', mobile):
            raise forms.ValidationError("Mobile number must be 10 digits.")
        return mobile

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if Customer.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username
