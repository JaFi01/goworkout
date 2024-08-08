# Generated by Django 5.0.7 on 2024-08-08 15:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0019_remove_user_workout_routines_workoutroutine_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workoutroutine',
            name='plans_for_day',
        ),
        migrations.AddField(
            model_name='planforday',
            name='fk_routine',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='routine_daily_plans', to='exercises.workoutroutine'),
        ),
    ]
