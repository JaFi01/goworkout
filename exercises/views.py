from django.shortcuts import render
from django.views import View
from django.views.generic import CreateView, FormView, UpdateView, ListView, DetailView
from django.shortcuts import get_object_or_404
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from .forms import UserRegistrationForm, UserPreferencesForm, WorkoutRoutineForm, PlanForDayForm, ExerciseSetForm
from .models import User, WorkoutRoutine, PlanForDay, ExerciseSet

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

class PlanForDayCreateView(LoginRequiredMixin, CreateView):
    model = PlanForDay
    form_class = PlanForDayForm
    template_name = 'exercises/plan_for_day_form.html'

    def form_valid(self, form):
        routine = WorkoutRoutine.objects.get(pk=self.kwargs['routine_pk'])
        plan = form.save(commit=False)
        plan.fk_routine = routine
        plan.save()
        routine.plans_for_day.add(plan)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('workout_routine_detail', kwargs={'pk': self.kwargs['routine_pk']})

class ExerciseSetCreateView(LoginRequiredMixin, CreateView):
    model = ExerciseSet
    form_class = ExerciseSetForm
    template_name = 'exercises/exercise_set_form.html'

    def form_valid(self, form):
        plan = PlanForDay.objects.get(pk=self.kwargs['plan_pk'])
        exercise_set = form.save()
        plan.exercise_sets.add(exercise_set)
        return super().form_valid(form)

    def get_success_url(self):
        plan = PlanForDay.objects.get(pk=self.kwargs['plan_pk'])
        return reverse_lazy('workout_routine_detail', kwargs={'pk': plan.workoutroutine_set.first().pk})
    
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