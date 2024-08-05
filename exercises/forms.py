import json
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, LevelType

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class UserPreferencesForm(forms.ModelForm):
    bmi = forms.FloatField(disabled=True, required=False, label="BMI")
    
    class Meta:
        model = User
        fields = [
            'date_of_birth', 
            'gender', 
            'height', 
            'weight', 
            'fitness_level',
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'gender': forms.Select(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')]),
            'fitness_level': forms.Select(choices=LevelType.choices),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['height'].help_text = "Height in cm"
        self.fields['weight'].help_text = "Weight in kg"
        if self.instance.bmi:
            self.fields['bmi'].initial = self.instance.bmi
        