from django.urls import path
from . import views
from .views import UserRegistrationView, UserLoginView, UserPreferencesView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.WelcomePageView.as_view(), name='starting-page'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('preferences/', UserPreferencesView.as_view(), name='user_preferences'),
    path('logout/', LogoutView.as_view(), name='logout'),
]