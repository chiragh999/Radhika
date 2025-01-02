from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken
import uuid

class UserModel(AbstractUser):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    @property
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }

    class Meta:
        db_table = 'user'

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Item(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

from django.db import models
from django.core.validators import RegexValidator, MinValueValidator
from django.utils import timezone

class EventBooking(models.Model):
    # Phone number validation
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Mobile number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )

    # Basic information
    name = models.CharField(max_length=100)
    mobile_no = models.CharField(validators=[phone_regex], max_length=17)
    date = models.DateField(default=timezone.now)  # Booking creation date
    reference = models.CharField(max_length=50, unique=True)
    
    # Event details
    event_date = models.DateField()
    event_time = models.TimeField()
    event_address = models.TextField()
    
    # Financial details
    advance_amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    per_dish_amount = models.DecimalField(
        max_digits=8, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    estimated_persons = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )
    
    # Additional details
    description = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-event_date', '-event_time']
        
    def __str__(self):
        return f"{self.name} - {self.event_date}"

    @property
    def total_estimated_amount(self):
        """Calculate the total estimated amount based on per dish amount and estimated persons"""
        return self.per_dish_amount * self.estimated_persons

    @property
    def remaining_amount(self):
        """Calculate the remaining amount after advance payment"""
        return self.total_estimated_amount - self.advance_amount

    def clean(self):
        from django.core.exceptions import ValidationError
        # Ensure event date is not in the past
        if self.event_date < timezone.now().date():
            raise ValidationError('Event date cannot be in the past')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)