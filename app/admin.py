from django.contrib import admin
from .models import EventBooking

# Register your models here.

@admin.register(EventBooking)
class EventBookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'reference', 'event_date', 'event_time', 'total_estimated_amount')
    search_fields = ('name', 'reference', 'mobile_no')
    list_filter = ('event_date', 'created_at')
    readonly_fields = ('created_at', 'updated_at')
