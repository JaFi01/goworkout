# Generated by Django 5.0.7 on 2024-07-22 10:29

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0012_update_admin_log_references'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='planforday',
            name='temp_begin_date',
        ),
        migrations.RemoveField(
            model_name='planforday',
            name='temp_end_date',
        ),
        migrations.AddField(
            model_name='exerciseset',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='exerciseset',
            name='date_updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='planforday',
            name='custom_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='planforday',
            name='date_updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.RemoveField(
            model_name='planforday',
            name='exercise_sets',
        ),
        migrations.RemoveField(
            model_name='workoutroutine',
            name='plans_for_day',
        ),
        migrations.AddField(
            model_name='planforday',
            name='exercise_sets',
            field=models.ManyToManyField(to='exercises.exerciseset'),
        ),
        migrations.AddField(
            model_name='workoutroutine',
            name='plans_for_day',
            field=models.ManyToManyField(to='exercises.planforday'),
        ),
    ]
