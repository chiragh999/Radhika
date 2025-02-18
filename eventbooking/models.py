from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone

class EventBooking(models.Model):
    ADVANCE_PAYMENT_MODE_CHOICES = [
        ("CASH", "CASH"),
        ("CHEQUE", "CHEQUE"),
        ("BANK_TRANSFER", "BANK TRANSFER"),
        ("ONLINE", "ONLINE"),
        ("OTHER", "OTHER"),
    ]

    # Phone number validation
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,15}$",
        message="Mobile number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
    )
    # Status choices
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirm", "Confirm"),
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

    # Advance payment fields (now nullable)
    advance_amount = models.CharField(
        max_length=150, null=True, blank=True  # Allows NULL values in the database
    )
    advance_payment_mode = models.CharField(
        max_length=20, choices=ADVANCE_PAYMENT_MODE_CHOICES, null=True, blank=True
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
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    # extraservice
    extra_service_amount = models.CharField(max_length=250,blank=True, null= True)
    extra_service = models.JSONField(default=dict)
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
