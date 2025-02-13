from rest_framework import serializers
from decimal import Decimal
from .models import *


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ["id", "name", "category"]


class CategorySerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ["id", "name", "items"]


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


class StokeItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = StokeItem
        fields = [
            "id",
            "name",
            "category",
            "quantity",
            "alert",
            "type",
            "nte_price",
            "total_price",
        ]


class StokeCategorySerializer(serializers.ModelSerializer):
    stokeitem = StokeItemSerializer(many=True, read_only=True)

    class Meta:
        model = StokeCategory
        fields = ["id", "name", "stokeitem"]


class PaymentSerializer(serializers.ModelSerializer):
    payment_date = serializers.DateField(
        input_formats=["%d-%m-%Y"],  # Accept DD-MM-YYYY in the payload
        format="%d-%m-%Y",  # Return DD-MM-YYYY in the response
    )
    formatted_event_date = serializers.ReadOnlyField()

    class Meta:
        model = Payment
        fields = [
            "bill_no",
            "total_amount",
            "advance_amount",
            "total_extra_amount",
            "pending_amount",
            "payment_date",
            "transaction_amount",
            "payment_mode",
            "settlement_amount",
            "payment_status",
            "note",
            "formatted_event_date",
            "billed_to_ids",
        ]
        read_only_fields = ["bill_no", "created_at", "updated_at"]

    def get_event_bookings(self, obj):
        """
        Returns the details of all associated event bookings
        """

        bookings = EventBooking.objects.filter(id__in=obj.billed_to_ids)
        return [
            {
                "id": booking.id,
                "name": booking.name,
                # Add other fields you want to include
            }
            for booking in bookings
        ]

    def validate_billed_to_ids(self, value):
        """
        Validate that all provided booking IDs exist
        """

        if not isinstance(value, list):
            raise serializers.ValidationError("billed_to_ids must be a list")

        if not value:
            raise serializers.ValidationError("At least one booking ID is required")

        existing_ids = set(
            EventBooking.objects.filter(id__in=value).values_list("id", flat=True)
        )
        invalid_ids = set(value) - existing_ids
        if invalid_ids:
            raise serializers.ValidationError(
                f"Invalid booking IDs: {', '.join(map(str, invalid_ids))}"
            )

        return value


    def to_representation(self, instance):
        data = super().to_representation(instance)
        if isinstance(instance, dict):
            billed_ids = instance.get("billed_to_ids", [])  # Extract billed_to_ids from the dict
        else:
            # For model instances, fetch billed_to_ids as an attribute
            billed_ids = instance.billed_to_ids


        # Fetch event booking details for all billed IDs
        detailed_bookings = []
        event_bookings = EventBooking.objects.filter(
            id__in=billed_ids
        )  # Optimize query
        for event_booking in event_bookings:
            detailed_bookings.append(
                {
                    "id": event_booking.id,
                    "name": event_booking.name,
                    "mobile_no": event_booking.mobile_no,
                    "date": event_booking.date.strftime("%d-%m-%Y"),
                    "reference": event_booking.reference,
                    "event_date": event_booking.event_date.strftime("%d-%m-%Y"),
                    "event_time": event_booking.event_time,
                    "status": event_booking.status,
                    "event_address": event_booking.event_address,
                    "advance_amount": str(
                        event_booking.advance_amount
                    ),  # Ensure decimals are strings
                    "advance_payment_mode": event_booking.advance_payment_mode,
                    "per_dish_amount": str(event_booking.per_dish_amount),
                    "estimated_persons": event_booking.estimated_persons,
                    "extra_service_amount" : event_booking.extra_service_amount,
                    "extra_service" : event_booking.extra_service,
                    "selected_items": event_booking.selected_items,
                    "description": event_booking.description,
                }
            )

        # Replace billed_to_ids with detailed booking data
        data["billed_to_ids"] = detailed_bookings

        # Format decimal fields in the Payment
        decimal_fields = [
            "total_amount",
            "advance_amount",
            "pending_amount",
            "transaction_amount",
            "settlement_amount",
        ]
        for field in decimal_fields:
            if data.get(field) is not None:
                data[field] = str(Decimal(data[field]))

        return data
