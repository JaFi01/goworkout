# Generated by Django 5.0.7 on 2024-08-14 19:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0025_alter_planforday_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='planforday',
            unique_together=set(),
        ),
    ]
