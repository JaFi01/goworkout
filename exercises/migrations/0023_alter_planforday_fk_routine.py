# Generated by Django 5.0.7 on 2024-08-08 20:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0022_remove_planforday_exercise_sets_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='planforday',
            name='fk_routine',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='plans_for_day', to='exercises.workoutroutine'),
        ),
    ]
