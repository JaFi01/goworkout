# Generated by Django 5.0.7 on 2024-08-13 22:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0024_alter_planforday_options_remove_planforday_day_name_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='planforday',
            unique_together={('fk_routine', 'day_of_week')},
        ),
    ]
