from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import CreateView, FormView, UpdateView, ListView, DetailView
from django.shortcuts import get_object_or_404
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.contrib.messages.views import SuccessMessageMixin
from .forms import UserRegistrationForm, UserPreferencesForm, WorkoutRoutineForm, PlanForDayForm, ExerciseSetForm
from .models import User, WorkoutRoutine, PlanForDay, ExerciseSet, Exercise

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

class WorkoutRoutineDetailView(LoginRequiredMixin, DetailView):
    model = WorkoutRoutine
    template_name = 'exercises/workout_routine_detail.html'
    context_object_name = 'routine'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plans'] = self.object.plans_for_day.all().order_by('day_name')
        context['exercises'] = Exercise.objects.all()
        return context

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
    
class AddPlanForDayView(LoginRequiredMixin, CreateView):
    model = PlanForDay
    form_class = PlanForDayForm
    template_name = 'exercises/plan_for_day_form.html'

    def form_valid(self, form):
        workout_routine = get_object_or_404(WorkoutRoutine, id=self.kwargs['workout_routine_id'])
        form.instance.workout_routine = workout_routine
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['routine'] = get_object_or_404(WorkoutRoutine, id=self.kwargs['workout_routine_id'])
        return context

    def get_success_url(self):
        return reverse_lazy('workout_routine_detail', kwargs={'pk': self.kwargs['workout_routine_id']})
    
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