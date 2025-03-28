# Generated by Django 5.0.7 on 2024-08-19 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0026_alter_planforday_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='workoutroutine',
            name='workout_type',
            field=models.CharField(choices=[('FBW', 'Full Body Workout'), ('PPL', 'Push-Pull-Legs'), ('UL', 'Upper-Lower'), ('OTHER', 'Other')], default='OTHER', max_length=10),
        ),
    ]
