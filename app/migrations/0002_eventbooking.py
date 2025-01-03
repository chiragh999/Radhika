# Generated by Django 5.1.4 on 2025-01-02 06:36

import django.core.validators
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventBooking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('mobile_no', models.CharField(max_length=17, validators=[django.core.validators.RegexValidator(message="Mobile number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('reference', models.CharField(max_length=50, unique=True)),
                ('event_date', models.DateField()),
                ('event_time', models.TimeField()),
                ('event_address', models.TextField()),
                ('advance_amount', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('per_dish_amount', models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(0)])),
                ('estimated_persons', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-event_date', '-event_time'],
            },
        ),
    ]
