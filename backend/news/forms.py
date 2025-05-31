from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class RegisterForm_Personal(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2']
        
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
        


