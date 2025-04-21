from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, URLValidator
import re
from .models import BusinessProfile, Review, Message

class CustomUserCreationForm(UserCreationForm):
    """A custom user creation form that includes an email field and validates its uniqueness."""
    email = forms.EmailField(required=True, validators=[EmailValidator()])

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with that email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class StyledForm(forms.ModelForm):
    """Base form with bootstrap styling for form controls."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control', 'placeholder': field.label})

class BusinessProfileForm(StyledForm):
    """Form for creating and updating business profiles with enhanced validation."""
    
    contact_phone = forms.CharField(
        required=True,
        min_length=10,
        max_length=15,
        help_text="Enter a valid phone number."
    )

    website = forms.URLField(
        required=False,
        validators=[URLValidator(schemes=['http', 'https'])],
        help_text="Include 'http' or 'https' in the URL."
    )

    class Meta:
        model = BusinessProfile
        fields = [
            'business_name',
            'services_offered',
            'working_hours',
            'location',
            'contact_phone',
            'contact_whatsapp',
            'contact_email',
            'website',
            'overview_picture',
        ]

    def clean_contact_phone(self):
        phone = self.cleaned_data['contact_phone']
        if not re.match(r'^\+?[1-9]\d{9,14}$', phone):
            raise forms.ValidationError("Enter a valid international phone number.")
        return phone

class ReviewForm(StyledForm):
    """Form for submitting a review with a limited rating choice and custom labels."""
    
    RATING_CHOICES = [(i, f"{i} - {'★' * i}") for i in range(1, 6)]
    rating = forms.ChoiceField(choices=RATING_CHOICES, label="Rating")

    class Meta:
        model = Review
        fields = ['rating', 'comment']

class MessageForm(forms.ModelForm):
    """Form for sending a message to a business owner."""
    class Meta:
        model = Message  # Assuming you have a Message model related to business
        fields = ['content']  # Adjust based on your message model's field names
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': 'Type your message here...', 'rows': 4}),
        }