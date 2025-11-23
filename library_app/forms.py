
from django import forms
from .models import Book
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

User = get_user_model()

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'isbn', 'description', 'cover', 'is_available']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'cover': forms.FileInput(attrs={'class': 'form-control'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class PatronRegistrationForm(UserCreationForm):
    username = forms.CharField(
        required=True,
        min_length=10,
        max_length=10,
        validators=[RegexValidator(r'^[A-Za-z0-9]{10}$', message='Username must be exactly 10 alphanumeric characters.')],
    )
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()
        if not email.endswith('@gmail.com'):
            raise ValidationError('Email must be a Gmail address ending with @gmail.com.')
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError('This email is already registered.')
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError('Passwords do not match.')
        if password1 and not password1.isdigit():
            raise ValidationError('Password must contain digits only.')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email')
        if commit:
            user.save()
        return user
