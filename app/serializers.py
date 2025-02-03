from rest_framework import serializers
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
    advance_amount = serializers.CharField(required=False, allow_blank=True, allow_null=True, default="")
    advance_payment_mode = serializers.CharField(required=False, allow_blank=True, allow_null=True, default="")
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
            "advance_amount",
            "advance_payment_mode",
            "per_dish_amount",
            "estimated_persons",
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
    billed_to_details = EventBookingSerializer(source="billed_to", read_only=True)
    payment_date = serializers.DateField(
        input_formats=["%d-%m-%Y"],  # Accept DD-MM-YYYY in the payload
        format="%d-%m-%Y",  # Return DD-MM-YYYY in the response
    )

    class Meta:
        model = Payment
        fields = [
            "bill_no",
            "billed_to",
            "total_amount",
            "pending_amount",
            "advance_amount",
            "payment_date",
            "transaction_amount",
            "payment_mode",
            "settlement_amount",
            "payment_status",
            "note",
            "billed_to_details",
        ]
