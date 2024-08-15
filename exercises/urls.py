from django.urls import path
from . import views
from .views import UserRegistrationView, UserLoginView, UserPreferencesView, AddPlanForDayView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.WelcomePageView.as_view(), name='starting-page'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('preferences/', UserPreferencesView.as_view(), name='user_preferences'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('workout-routines/', views.WorkoutRoutineListView.as_view(), name='workout_routine_list'),
    path('workout-routines/create/', views.WorkoutRoutineCreateView.as_view(), name='workout_routine_create'),
    path('workout-routines/<int:pk>/delete/', views.WorkoutRoutineDeleteView.as_view(), name='workout_routine_delete'),

    path('workout-routines/<int:pk>/', views.WorkoutRoutineDetailView.as_view(), name='workout_routine_detail'),
    path('workout-routines/<int:routine_pk>/add-plan/', views.PlanForDayCreateView.as_view(), name='plan_for_day_create'),
    path('plans/<int:plan_pk>/add-exercise-set/', views.ExerciseSetCreateView.as_view(), name='exercise_set_create'),
    path('workout-routines/<int:workout_routine_id>/add-plan/', views.AddPlanForDayView.as_view(), name='add_plan_for_day'),
    
    path('plan/<int:plan_id>/add-exercise/', views.AddExerciseSetView.as_view(), name='add_exercise_set'),
    path('add-exercise/', views.AddExerciseView.as_view(), name='add_exercise'),
    path('edit-exercise/', views.EditExerciseView.as_view(), name='edit_exercise'),
    path('delete-exercise/<int:exercise_id>/', views.DeleteExerciseView.as_view(), name='delete_exercise'),
    path('workout-routines/<int:routine_id>/analyze/', views.AnalyzeRoutineView.as_view(), name='analyze_routine'),

    path('plan/<int:pk>/edit/', views.PlanForDayUpdateView.as_view(), name='plan_for_day_edit'),
    path('plan/<int:pk>/delete/', views.PlanForDayDeleteView.as_view(), name='plan_for_day_delete'),
    path('workout-routine/<int:pk>/edit/', views.WorkoutRoutineUpdateView.as_view(), name='workout_routine_edit'),
    path('workout-routines/<int:pk>/analysis/', views.WorkoutRoutineAnalysisView.as_view(), name='workout_routine_analysis'),
]