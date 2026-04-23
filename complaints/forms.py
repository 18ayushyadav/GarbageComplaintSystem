"""
Smart Garbage Complaint System — Forms

Django forms for:
- ComplaintForm: Main complaint submission form with Bootstrap styling
- UserRegisterForm: Extended user registration with email field

Each form uses Bootstrap 5 classes for consistent, modern styling.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Complaint


class ComplaintForm(forms.ModelForm):
    """
    Form for submitting a new garbage complaint.

    Uses Bootstrap 5 form-control classes via widget attrs for styling.
    Image upload uses a custom file input with preview support.
    """

    class Meta:
        model = Complaint
        fields = [
            'reporter_name',
            'reporter_email',
            'reporter_phone',
            'location_text',
            'google_maps_link',
            'description',
            'image',
            'priority',
        ]
        widgets = {
            'reporter_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Rajesh Kumar',
                'id': 'reporter-name',
            }),
            'reporter_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., rajesh@email.com',
                'id': 'reporter-email',
            }),
            'reporter_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., +91 98765 43210 (optional)',
                'id': 'reporter-phone',
            }),
            'location_text': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Near Sector 5 Market, Noida, UP',
                'id': 'location-text',
            }),
            'google_maps_link': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://maps.google.com/... (optional)',
                'id': 'google-maps-link',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe the garbage issue in detail...\n'
                               'e.g., Large pile of household waste dumped near the park entrance. '
                               'Waste includes plastic bags, food waste, and construction debris. '
                               'Causing foul smell and attracting stray animals.',
                'id': 'description',
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*',
                'id': 'complaint-image',
            }),
            'priority': forms.Select(attrs={
                'class': 'form-select',
                'id': 'priority',
            }),
        }
        labels = {
            'reporter_name': 'Your Full Name',
            'reporter_email': 'Email Address',
            'reporter_phone': 'Phone Number',
            'location_text': 'Location',
            'google_maps_link': 'Google Maps Link',
            'description': 'Complaint Description',
            'image': 'Upload Photo Evidence',
            'priority': 'Priority Level',
        }
        help_texts = {
            'google_maps_link': 'Open Google Maps → Right-click location → "Share" → Copy link',
            'image': 'Upload a clear photo of the garbage issue (JPG, PNG)',
        }


class UserRegisterForm(UserCreationForm):
    """
    Extended registration form that adds an email field.

    Django's default UserCreationForm only has username + password.
    We add email and first_name for a better user experience.
    """

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your.email@example.com',
            'id': 'register-email',
        })
    )
    first_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your full name',
            'id': 'register-name',
        })
    )

    class Meta:
        model = User
        fields = ['first_name', 'username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        """Add Bootstrap classes to the default password fields."""
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Choose a username',
            'id': 'register-username',
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Create a password (min 4 chars)',
            'id': 'register-password1',
        })
        self.fields['password1'].help_text = 'Your password must contain at least 4 characters.'
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm your password',
            'id': 'register-password2',
        })
        self.fields['password2'].help_text = 'Enter the same password again for confirmation.'

    def save(self, commit=True):
        """Save user with email and first_name."""
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        if commit:
            user.save()
        return user
