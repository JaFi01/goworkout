from django.shortcuts import render
from django.views import View
from django.views.generic import CreateView, FormView, UpdateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from .forms import UserRegistrationForm, UserPreferencesForm
from .models import User

# Create your views here.
class WelcomePageView(View):
    def get(self, request):
        return render(request, "exercises/welcome.html")
    
class UserRegistrationView(SuccessMessageMixin, CreateView):
    template_name = 'exercises/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('user_preferences')
    success_message = "Your account was created successfully. Please set your preferences."

    def form_valid(self, form):
        response = super().form_valid(form)
        # Log the user in after registration
        login(self.request, self.object)
        return response

class UserLoginView(LoginView):
    template_name = 'exercises/login.html'
    success_url = reverse_lazy('user_preferences')

    def get_success_url(self):
        return self.success_url

class UserPreferencesView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserPreferencesForm
    template_name = 'exercises/user_preferences.html'
    success_url = reverse_lazy('starting-page')
    success_message = "Your preferences have been updated successfully."

    def get_object(self, queryset=None):
        return self.request.user
    
    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.update_bmi()  # Aktualizujemy BMI
        self.object.save()
        return response
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['bmi'].initial = round(self.object.bmi, 2) if self.object.bmi is not None else None
        return form