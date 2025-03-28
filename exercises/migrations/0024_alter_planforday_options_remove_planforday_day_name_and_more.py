# Generated by Django 5.0.7 on 2024-08-13 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0023_alter_planforday_fk_routine'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='planforday',
            options={'ordering': ['day_of_week']},
        ),
        migrations.RemoveField(
            model_name='planforday',
            name='day_name',
        ),
        migrations.AddField(
            model_name='planforday',
            name='day_of_week',
            field=models.IntegerField(choices=[(1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday'), (6, 'Saturday'), (7, 'Sunday')], default=1),
        ),
    ]
