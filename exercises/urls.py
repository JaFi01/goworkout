from django.urls import path
from . import views

urlpatterns = [
    path('', views.WelcomePageView.as_view(), name='starting-page'),
]