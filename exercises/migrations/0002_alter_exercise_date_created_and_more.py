# Generated by Django 5.0.7 on 2024-07-17 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercises', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercise',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='exercise',
            name='date_updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
