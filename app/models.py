from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken
import uuid


class UserModel(AbstractUser):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )

    @property
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}

    class Meta:
        db_table = "user"


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Item(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="items"
    )
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class EventBooking(models.Model):
    # Phone number validation
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Mobile number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
    )
    # Status choices
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
        ("done", "Done"),
    ]
    # listfild [cat->itme multipul]
    selected_items = models.JSONField(default=dict)
    # Basic information
    name = models.CharField(max_length=100)
    mobile_no = models.CharField(validators=[phone_regex], max_length=17)
    date = models.DateField(default=timezone.now)  # Booking creation date
    reference = models.CharField(max_length=50, unique=False)
    # Event details
    event_date = models.DateField()
    event_time = models.CharField(max_length=100)
    event_address = models.TextField()
    advance_amount = models.CharField(
        max_length=150,  # Adjust length as needed
    )
    per_dish_amount = models.CharField(
        max_length=150,  # Adjust length as needed
    )
    estimated_persons = models.CharField(
        max_length=150,  # Adjust length as needed
    )
    # Additional details
    description = models.TextField(blank=True)
    # Status field
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pending"
    )
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-event_date", "-event_time"]

    def __str__(self):
        return f"{self.name} - {self.event_date}"

    @property
    def formatted_event_date(self):
        return self.event_date.strftime("%d-%m-%Y")

    @property
    def formatted_date(self):
        return self.event_date.strftime("%d-%m-%Y")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class StokeCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class StokeItem(models.Model):

    TYPE_CHOICES = [
        ("KG", "કિલોગ્રામ"),  # Kilograms
        ("G", "ગ્રામ"),  # Grams
        ("L", "લીટર"),  # Liters
        ("ML", "મિલીલીટર"),  # Milliliters
        ("QTY", "જથ્થો"),  # Quantity
    ]

    name = models.CharField(max_length=200, unique=True)
    category = models.ForeignKey(
        StokeCategory, on_delete=models.CASCADE, related_name="stokeitem"
    )
    nte_price = models.CharField(max_length=250)
    total_price = models.CharField(max_length=250)
    quantity = models.DecimalField(max_digits=100, decimal_places=0)
    alert = models.CharField(max_length=500)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)

    def __str__(self):
        return f"{self.name} - {self.quantity} {self.alert}"

class Payment(models.Model):
    PAYMENT_MODE_CHOICES = [
        ('CASH', 'Cash'),
        ('CARD', 'Card'),
        ('UPI', 'UPI'),
        ('BANK_TRANSFER', 'Bank Transfer'),
    ]

    bill_no = models.AutoField(primary_key=True)
    billed_to = models.ForeignKey(EventBooking, on_delete=models.CASCADE, related_name='payments')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    pending_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    transaction_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_mode = models.CharField(max_length=20, choices=PAYMENT_MODE_CHOICES)
    settlement_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment {self.bill_no} - {self.billed_to.name}"

    @property
    def formatted_event_date(self):
        return self.payment_date.strftime("%d-%m-%Y")
