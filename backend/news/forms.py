from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class RegisterForm_Personal(forms.ModelForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())
    country = forms.ChoiceField(
        choices=CustomUser._meta.get_field('country').choices,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2', 'country']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2
        
class RegisterForm_News(forms.ModelForm):
    is_subscribed = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Subscribe to newsletter',
        initial=True
    )
    
    class Meta:
        model = CustomUser
        fields = ['interests', 'frequency', 'preferred_time', 'is_subscribed']
        widgets = {
            'preferred_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control'
            }),
            'interests': forms.CheckboxSelectMultiple(attrs={
                'class': 'form-check-input'
            }),
            'frequency': forms.Select(attrs={
                'class': 'form-select'
            }, choices=[
                ('daily', 'Daily'),
                ('weekly', 'Weekly')
            ])
        }
        


