# Generated by Django 5.1.4 on 2025-04-29 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='rule',
            field=models.BooleanField(default=False),
        ),
    ]
