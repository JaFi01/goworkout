from django.contrib import admin
from .models import User, Exercise, WorkoutRoutine, PlanForDay, ExerciseSet

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_active', 'date_joined')
    search_fields = ('username', 'email')
    list_filter = ('is_active', 'is_staff', 'is_superuser')

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'level')
    search_fields = ('name', 'category')
    list_filter = ('category', 'level', 'equipment')

class ExerciseSetInline(admin.TabularInline):
    model = ExerciseSet
    extra = 1
    fields = ('exercise', 'series', 'repetitions', 'pause_time')

@admin.register(PlanForDay)
class PlanForDayAdmin(admin.ModelAdmin):
    inlines = [ExerciseSetInline]
    list_display = ('get_day_of_week_display', 'custom_name', 'fk_routine')
    search_fields = ('custom_name', 'fk_routine__routine_name')
    list_filter = ('day_of_week', 'fk_routine')

class PlanForDayInline(admin.TabularInline):
    model = PlanForDay
    extra = 1
    fields = ('day_of_week', 'custom_name')

@admin.register(WorkoutRoutine)
class WorkoutRoutineAdmin(admin.ModelAdmin):
    inlines = [PlanForDayInline]
    list_display = ('routine_name', 'user', 'begin_date', 'end_date', 'is_current', 'is_public')
    search_fields = ('routine_name', 'user__username')
    list_filter = ('is_current', 'is_public', 'begin_date', 'end_date')

@admin.register(ExerciseSet)
class ExerciseSetAdmin(admin.ModelAdmin):
    list_display = ('exercise', 'plan_for_day', 'series', 'repetitions', 'pause_time')
    list_filter = ('plan_for_day__day_of_week', 'exercise__category')
    search_fields = ('exercise__name', 'plan_for_day__custom_name')