from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import CreateView, FormView, UpdateView, ListView, DetailView, DeleteView
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count
from .forms import UserRegistrationForm, UserPreferencesForm, WorkoutRoutineForm, PlanForDayForm, ExerciseSetForm
from .models import User, WorkoutRoutine, PlanForDay, ExerciseSet, Exercise
from .analysis import Analysis
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
    
#WORKOUTS
class WorkoutRoutineListView(LoginRequiredMixin, ListView):
    model = WorkoutRoutine
    template_name = 'exercises/workout_routine_list.html'
    context_object_name = 'routines'

    def get_queryset(self):
        return WorkoutRoutine.objects.filter(user=self.request.user)

class WorkoutRoutineCreateView(LoginRequiredMixin, CreateView):
    model = WorkoutRoutine
    form_class = WorkoutRoutineForm
    template_name = 'exercises/workout_routine_form.html'
    success_url = reverse_lazy('workout_routine_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class WorkoutRoutineDeleteView(LoginRequiredMixin, DeleteView):
    model = WorkoutRoutine
    success_url = reverse_lazy('workout_routine_list')
    
    def get_queryset(self):
        return WorkoutRoutine.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(self.request, "Workout routine deleted successfully.")
        return HttpResponseRedirect(success_url)

class WorkoutRoutineDetailView(LoginRequiredMixin, DetailView):
    model = WorkoutRoutine
    template_name = 'exercises/workout_routine_detail.html'
    context_object_name = 'routine'

    def check_and_remove_duplicates(self):
        routine = self.object
        duplicates = (
            PlanForDay.objects.filter(fk_routine=routine)
            .values('day_of_week')
            .annotate(count=Count('id'))
            .filter(count__gt=1)
        )

        for duplicate in duplicates:
            day = duplicate['day_of_week']
            plans = PlanForDay.objects.filter(fk_routine=routine, day_of_week=day).order_by('id')
            # Zachowaj najstarszy plan (z najniższym ID), usuń resztę
            for plan in plans[1:]:
                messages.warning(self.request, f"Usunięto duplikat planu dla {plan.get_day_of_week_display()}.")
                plan.delete()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plans'] = self.object.plans_for_day.all().order_by('day_of_week')
        context['exercises'] = Exercise.objects.all()
        context['daily_plans_count'] = self.object.count_daily_plans()
        context['available_days'] = self.get_available_days()
        self.check_and_remove_duplicates()
        
        daily_plans_count = self.object.count_daily_plans()
        #print(daily_plans_count)
        return context
    
    def get_available_days(self):
        used_days = set(self.object.plans_for_day.values_list('day_of_week', flat=True))
        return [day for day in PlanForDay.DAYS_OF_WEEK if day[0] not in used_days]

class WorkoutRoutineUpdateView(LoginRequiredMixin, UpdateView):
    model = WorkoutRoutine
    form_class = WorkoutRoutineForm
    template_name = 'exercises/workout_routine_form.html'

    def get_success_url(self):
        return reverse_lazy('workout_routine_detail', kwargs={'pk': self.object.pk})

    def get_object(self, queryset=None):
        return get_object_or_404(WorkoutRoutine, pk=self.kwargs['pk'], user=self.request.user)


class PlanForDayCreateView(LoginRequiredMixin, CreateView):
    model = PlanForDay
    form_class = PlanForDayForm
    template_name = 'exercises/plan_for_day_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.workout_routine = get_object_or_404(WorkoutRoutine, pk=self.kwargs['routine_pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['workout_routine'] = self.workout_routine
        return context

    def form_valid(self, form):
        form.instance.fk_routine = self.workout_routine
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('workout_routine_detail', kwargs={'pk': self.kwargs['routine_pk']})

class PlanForDayUpdateView(LoginRequiredMixin, UpdateView):
    model = PlanForDay
    form_class = PlanForDayForm
    template_name = 'exercises/plan_for_day_form.html'

    def get_success_url(self):
        return reverse_lazy('workout_routine_detail', kwargs={'pk': self.object.fk_routine.pk})

class PlanForDayDeleteView(LoginRequiredMixin, DeleteView):
    model = PlanForDay
    template_name = 'exercises/plan_for_day_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('workout_routine_detail', kwargs={'pk': self.object.fk_routine.pk})

class ExerciseSetCreateView(LoginRequiredMixin, CreateView):
    model = ExerciseSet
    form_class = ExerciseSetForm
    template_name = 'exercises/exercise_set_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.plan = get_object_or_404(PlanForDay, pk=self.kwargs['plan_pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.plan_for_day = self.plan
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('workout_routine_detail', kwargs={'pk': self.plan.fk_routine.pk})
 
class AddPlanForDayView(CreateView):
    model = PlanForDay
    form_class = PlanForDayForm
    template_name = 'exercises/plan_for_day_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        self.routine = get_object_or_404(WorkoutRoutine, id=self.kwargs['workout_routine_id'])
        return kwargs

    def form_valid(self, form):
        form.instance.fk_routine = self.routine
        response = super().form_valid(form)
        
        # Sprawdź, czy istnieje już plan na ten dzień
        existing_plans = PlanForDay.objects.filter(
            fk_routine=self.routine,
            day_of_week=form.instance.day_of_week
        ).exclude(id=form.instance.id)
        
        if existing_plans.exists():
            # Jeśli istnieje, usuń nowo dodany plan i wyświetl komunikat
            form.instance.delete()
            messages.error(self.request, "Plan for this day already exists. Please choose another day.")
            return self.form_invalid(form)
        
        messages.success(self.request, "Plan added successfully!")
        return response

    def get_success_url(self):
        return reverse_lazy('workout_routine_detail', kwargs={'pk': self.routine.id})
    
class AddExerciseSetView(CreateView):
    model = ExerciseSet
    form_class = ExerciseSetForm
    template_name = 'add_exercise_set.html'

    def form_valid(self, form):
        plan = PlanForDay.objects.get(id=self.kwargs['plan_id'])
        form.instance.plan_for_day = plan
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('workout_routine_detail', kwargs={'pk': self.object.plan_for_day.fk_routine.id})
    
class AddExerciseView(View):
    @method_decorator(require_POST)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        plan_id = request.POST.get('plan_id')
        exercise_id = request.POST.get('exercise')
        series = request.POST.get('series')
        repetitions = request.POST.get('repetitions')
        pause_time = request.POST.get('pause_time')

        plan = get_object_or_404(PlanForDay, id=plan_id)
        exercise = get_object_or_404(Exercise, id=exercise_id)

        exercise_set = ExerciseSet.objects.create(
            plan_for_day=plan,
            exercise=exercise,
            series=series,
            repetitions=repetitions,
            pause_time=pause_time
        )

        return JsonResponse({'success': True})

class EditExerciseView(View):
    def post(self, request):
        exercise_set_id = request.POST.get('exercise_set_id')
        exercise_id = request.POST.get('exercise')
        series = request.POST.get('series')
        repetitions = request.POST.get('repetitions')
        pause_time = request.POST.get('pause_time')

        exercise_set = get_object_or_404(ExerciseSet, id=exercise_set_id)
        exercise = get_object_or_404(Exercise, id=exercise_id)

        exercise_set.exercise = exercise
        exercise_set.series = series
        exercise_set.repetitions = repetitions
        exercise_set.pause_time = pause_time
        exercise_set.save()

        return JsonResponse({'success': True})
class DeleteExerciseView(View):
    def post(self, request, exercise_id):
        exercise_set = get_object_or_404(ExerciseSet, id=exercise_id)
        exercise_set.delete()
        return JsonResponse({'success': True})
    
class AnalyzeRoutineView(LoginRequiredMixin, View):
    def get(self, request, routine_id):
        routine = get_object_or_404(WorkoutRoutine, id=routine_id, user=request.user)
        daily_plans_count = routine.count_daily_plans()
        print(f"Liczba planów dziennych dla rutyny '{routine.routine_name}': {daily_plans_count}")
        return JsonResponse({'status': 'success'})
    
class WorkoutRoutineAnalysisView(LoginRequiredMixin, DetailView):
    model = WorkoutRoutine
    template_name = 'exercises/workout_routine_analysis.html'
    context_object_name = 'routine'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        analysis = Analysis(self.object)
        context['analysis_report'] = analysis.get_analysis_report()
        return context