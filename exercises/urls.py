from django.urls import path
from . import views
from .views import UserRegistrationView, UserLoginView, UserPreferencesView

urlpatterns = [
    path('', views.WelcomePageView.as_view(), name='starting-page'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('preferences/', UserPreferencesView.as_view(), name='user_preferences'),
]