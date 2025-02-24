from rest_framework import serializers
from .models import *

class EventBookingSerializer(serializers.ModelSerializer):
    advance_amount = serializers.CharField(
        required=False, allow_blank=True, allow_null=True, default=""
    )
    advance_payment_mode = serializers.CharField(
        required=False, allow_blank=True, allow_null=True, default=""
    )
    event_date = serializers.DateField(
        input_formats=["%d-%m-%Y"],  # Accept DD-MM-YYYY in the payload
        format="%d-%m-%Y",  # Return DD-MM-YYYY in the response
    )
    date = serializers.DateField(
        format="%d-%m-%Y", read_only=True  # Format for response
    )

    class Meta:
        model = EventBooking
        fields = [
            "id",  # Include the primary key for reference
            "name",
            "mobile_no",
            "date",
            "reference",
            "event_date",
            "event_time",
            "status",
            "event_address",
            "extra_service_amount",
            "advance_amount",
            "advance_payment_mode",
            "per_dish_amount",
            "estimated_persons",
            "extra_service",
            "selected_items",
            "description",
        ]
