from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, UserManager
from django.contrib.auth import get_user_model
from django.db import models
import uuid
from django.utils import timezone
from django.conf import settings

class Muscle(models.TextChoices):
    ABDOMINALS = 'abdominals'
    HAMSTRINGS = 'hamstrings'
    ADDUCTORS = 'adductors'
    QUADRICEPS = 'quadriceps'
    BICEPS = 'biceps'
    SHOULDERS = 'shoulders'
    CHEST = 'chest'
    MIDDLE_BACK = 'middle back'
    CALVES = 'calves'
    GLUTES = 'glutes'
    LOWER_BACK = 'lower back'
    LATS = 'lats'
    TRICEPS = 'triceps'
    TRAPS = 'traps'
    FOREARMS = 'forearms'
    NECK = 'neck'
    ABDUCTORS = 'abductors'

class ForceType(models.TextChoices):
    PULL = 'pull'
    PUSH = 'push'
    STATIC = 'static'

class LevelType(models.TextChoices):
    BEGINNER = 'beginner'
    INTERMEDIATE = 'intermediate'
    EXPERT = 'expert'

class MechanicType(models.TextChoices):
    COMPOUND = 'compound'
    ISOLATION = 'isolation'

class EquipmentType(models.TextChoices):
    BODY_ONLY = 'body only'
    MACHINE = 'machine'
    OTHER = 'other'
    FOAM_ROLL = 'foam roll'
    KETTLEBELLS = 'kettlebells'
    DUMBBELL = 'dumbbell'
    CABLE = 'cable'
    BARBELL = 'barbell'
    BANDS = 'bands'
    MEDICINE_BALL = 'medicine ball'
    EXERCISE_BALL = 'exercise ball'
    EZ_CURL_BAR = 'e-z curl bar'

class CategoryType(models.TextChoices):
    STRENGTH = 'strength'
    STRETCHING = 'stretching'
    PLYOMETRICS = 'plyometrics'
    STRONGMAN = 'strongman'
    POWERLIFTING = 'powerlifting'
    CARDIO = 'cardio'
    OLYMPIC_WEIGHTLIFTING = 'olympic weightlifting'

class Exercise(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.TextField(unique=True)
    aliases = ArrayField(models.TextField(), blank=True, null=True)
    primary_muscles = ArrayField(models.CharField(max_length=20, choices=Muscle.choices), blank=True, null=True)
    secondary_muscles = ArrayField(models.CharField(max_length=20, choices=Muscle.choices), blank=True, null=True)
    force = models.CharField(max_length=10, choices=ForceType.choices, blank=True, null=True)
    level = models.CharField(max_length=15, choices=LevelType.choices)
    mechanic = models.CharField(max_length=10, choices=MechanicType.choices, blank=True, null=True)
    equipment = models.CharField(max_length=20, choices=EquipmentType.choices, blank=True, null=True)
    category = models.CharField(max_length=25, choices=CategoryType.choices)
    instructions = ArrayField(models.TextField(), blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    tips = ArrayField(models.TextField(), blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)
    

    class Meta:
        db_table = 'exercises'


    def __str__(self):
        return self.name
    
class DayOfWeek(models.TextChoices):
    MONDAY = 'Monday'
    TUESDAY = 'Tuesday'
    WEDNESDAY = 'Wednesday'
    THURSDAY = 'Thursday'
    FRIDAY = 'Friday'
    SATURDAY = 'Saturday'
    SUNDAY = 'Sunday'
    
    
class ExerciseSet(models.Model):
    plan_for_day = models.ForeignKey('PlanForDay', on_delete=models.CASCADE, related_name='exercise_sets', null=True)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, null=True)
    series = models.PositiveIntegerField()
    repetitions = models.PositiveIntegerField()
    pause_time = models.PositiveIntegerField()
    date_created = models.DateTimeField(default=timezone.now, editable=False)
    date_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        db_table = 'exercise_sets'
        
    def __str__(self):
        return f"{self.exercise.name} - Series:{self.series} x Reps:{self.repetitions}"

class PlanForDay(models.Model):
    DAYS_OF_WEEK = [
        (1, 'Monday'),
        (2, 'Tuesday'),
        (3, 'Wednesday'),
        (4, 'Thursday'),
        (5, 'Friday'),
        (6, 'Saturday'),
        (7, 'Sunday'),
    ]
     
    fk_routine = models.ForeignKey('WorkoutRoutine', on_delete=models.CASCADE, null=True, related_name='plans_for_day')
    day_of_week = models.IntegerField(choices=DAYS_OF_WEEK, default=1)
    custom_name = models.CharField(max_length=100, null=True, blank=True)
    #CHANGE THIS TO PROPERTY
    #exercise_sets = models.ManyToManyField(ExerciseSet) # Changed to ManyToManyField
    date_created = models.DateTimeField(default=timezone.now, editable=False)
    date_updated = models.DateTimeField(auto_now=True, editable=False)
    notes = models.TextField(blank=True, null=True, max_length=500)

    class Meta:
        db_table = 'plan_for_day'
        ordering = ['day_of_week']
        #unique_together = ['fk_routine', 'day_of_week']

    @property
    def exercise_sets(self):
        return self.exercise_sets.all()
        
    def __str__(self):
        return f"Plan for {self.get_day_of_week_display()} - {self.custom_name}"

def get_default_user():
    User = get_user_model()
    return User.objects.get_or_create(username='default_user')[0].id

class WorkoutRoutine(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_workout_routines', null=True)
    routine_name = models.CharField(max_length=100)
    
    begin_date = models.DateField(blank=True, null=True)  # Add this line
    end_date = models.DateField(blank=True, null=True)  # Add this line
    is_current = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True, max_length=500)
    is_public = models.BooleanField(default=False)
    class Meta:
        db_table = 'workout_routines'

    @property
    def plans_for_day(self):
        return self.plans_for_day.all()

    def __str__(self):
        return f"{self.routine_name } - {self.display_if_current()}"

    def display_if_current(self):
        return "CURRENT" if self.is_current else "NOT CURRENT"
    
    def count_daily_plans(self):
        return self.plans_for_day.count()
    
    def save(self, *args, **kwargs):
        if self.is_current:
            # Ustawienie wszystkich innych planów użytkownika jako nieaktualne
            WorkoutRoutine.objects.filter(user=self.user).exclude(pk=self.pk).update(is_current=False)
        super().save(*args, **kwargs)
    
#SECTION: User Model    
class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not username:
            raise ValueError('User must have a username')
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            username=username, 
            email=self.normalize_email(email)
            )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user( 
            username=username, 
            email=self.normalize_email(email),
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    
class User(AbstractBaseUser):
    #basic information section
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True, max_length=100)
    
    #forced by django conventions
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    
    
    #TODO! Add profile picture handling
    #profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    
    #personal information section
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], blank=True)
    
    
    #physical information section
    height = models.FloatField(help_text=("Height in cm"), null=True, blank=True)
    weight = models.FloatField(help_text=("Weight in kg"), null=True, blank=True)
    bmi = models.FloatField(help_text="Body Mass Index", null=True, blank=True, editable=False)
    fitness_level = models.CharField(
        max_length=20,
        choices=LevelType.choices,
        default=LevelType.BEGINNER,
        blank=True
    )

    preferred_sport = models.CharField(
        max_length=25,
        choices=CategoryType.choices,
        blank=True,
        null=True
    )

    #!IMPORTANT User's workout routines
    @property
    def workout_routines(self):
        return self.user_workout_routines.all()
    
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']
    
    objects = UserManager()
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True
    
    def save(self, *args, **kwargs):
        self.update_bmi()
        super().save(*args, **kwargs)
    
    def update_bmi(self):
        if self.height and self.weight and self.height > 0:
            height_in_meters = self.height / 100
            self.bmi = round(self.weight / (height_in_meters ** 2), 2)
        else:
            self.bmi = None

    class Meta:
        db_table = 'users'
    

        
              