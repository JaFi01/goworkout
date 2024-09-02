from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from .models import User, LevelType, CategoryType, WorkoutRoutine, PlanForDay, ExerciseSet, Exercise
from datetime import date

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
            'preferred_sport',
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'gender': forms.Select(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')]),
            'fitness_level': forms.Select(choices=LevelType.choices),
            'preferred_sport': forms.Select(choices=CategoryType.choices),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['height'].help_text = "Height in cm"
        self.fields['weight'].help_text = "Weight in kg"
        if self.instance.bmi:
            self.fields['bmi'].initial = self.instance.bmi
        

class WorkoutRoutineForm(forms.ModelForm):
    class Meta:
        model = WorkoutRoutine
        fields = ['routine_name', 'begin_date', 'end_date', 'is_current', 'notes', 'is_public', 'workout_type']

        widgets = {
            'routine_name': forms.TextInput(attrs={'class': 'form-control'}),
            'begin_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'is_current': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'notes': forms.Textarea(attrs={'class': 'form-control'}),
            'workout_type': forms.Select(choices=CategoryType.choices),
            'is_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        begin_date = cleaned_data.get('begin_date')
        end_date = cleaned_data.get('end_date')

        if begin_date and not isinstance(begin_date, date):
            self.add_error('begin_date', 'Invalid date format')
        if end_date and not isinstance(end_date, date):
            self.add_error('end_date', 'Invalid date format')

        if isinstance(begin_date, date) and isinstance(end_date, date):
            if end_date < begin_date:
                self.add_error('end_date', 'End date cannot be earlier than begin date')

        return cleaned_data

class PlanForDayForm(forms.ModelForm):
    class Meta:
        model = PlanForDay
        fields = ['day_of_week', 'custom_name', 'notes']
    
class ExerciseSetForm(forms.ModelForm):
    exercise = forms.ModelChoiceField(queryset=Exercise.objects.all())
    
    class Meta:
        model = ExerciseSet
        fields = ['exercise', 'series', 'repetitions', 'pause_time']

class ExerciseSetForm(forms.ModelForm):
    class Meta:
        model = ExerciseSet
        fields = ['exercise', 'series', 'repetitions', 'pause_time']