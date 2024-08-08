from django.contrib import admin
from .models import User, Exercise, WorkoutRoutine, PlanForDay, ExerciseSet

admin.site.register(User)
admin.site.register(Exercise)
class ExerciseSetInline(admin.TabularInline):
    model = PlanForDay.exercise_sets.through
    extra = 1

class PlanForDayAdmin(admin.ModelAdmin):
    inlines = [ExerciseSetInline]
    exclude = ('exercise_sets',)

class PlanForDayInline(admin.TabularInline):
    model = PlanForDay
    extra = 1

class WorkoutRoutineAdmin(admin.ModelAdmin):
    inlines = [PlanForDayInline]

admin.site.register(ExerciseSet)
admin.site.register(PlanForDay, PlanForDayAdmin)
admin.site.register(WorkoutRoutine, WorkoutRoutineAdmin)