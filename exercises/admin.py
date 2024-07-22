from django.contrib import admin
from .models import User, Exercise, WorkoutRoutine, PlanForDay, ExerciseSet

admin.site.register(User)
admin.site.register(Exercise)
admin.site.register(ExerciseSet)
admin.site.register(WorkoutRoutine)
admin.site.register(PlanForDay)