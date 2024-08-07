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

    path('workout-routines/', views.WorkoutRoutineListView.as_view(), name='workout_routine_list'),
    path('workout-routines/create/', views.WorkoutRoutineCreateView.as_view(), name='workout_routine_create'),
    path('workout-routines/<int:pk>/', views.WorkoutRoutineDetailView.as_view(), name='workout_routine_detail'),
    path('workout-routines/<int:routine_pk>/add-plan/', views.PlanForDayCreateView.as_view(), name='plan_for_day_create'),
    path('plans/<int:plan_pk>/add-exercise-set/', views.ExerciseSetCreateView.as_view(), name='exercise_set_create'),
]