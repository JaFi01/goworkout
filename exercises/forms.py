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
    social_media_links = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = User
        fields = [
            'date_of_birth', 
            'gender', 
            'social_media_links',
            'height', 
            'weight', 
            'fitness_level',
            'disliked_exercises'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'gender': forms.Select(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')]),
            'fitness_level': forms.Select(choices=LevelType.choices),
            'disliked_exercises': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['height'].help_text = "Height in cm"
        self.fields['weight'].help_text = "Weight in kg"
        
        # Convert JSON to string for initial display
        if self.instance.social_media_links:
            self.initial['social_media_links'] = json.dumps(self.instance.social_media_links)

    def clean_social_media_links(self):
        data = self.cleaned_data['social_media_links']
        if data:
            try:
                return json.loads(data)
            except json.JSONDecodeError:
                raise forms.ValidationError("Invalid JSON format for social media links")
        return {}