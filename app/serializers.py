from rest_framework import serializers
from django.utils import timezone
from .models import Category, Item, EventBooking

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'category']

class CategorySerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'items']

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

class EventBookingSerializer(serializers.ModelSerializer):
    total_estimated_amount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    remaining_amount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    
    class Meta:
        model = EventBooking
        fields = [
            'id',
            'name',
            'mobile_no',
            'date',
            'reference',
            'event_date',
            'event_time',
            'event_address',
            'advance_amount',
            'per_dish_amount',
            'estimated_persons',
            'description',
            'total_estimated_amount',
            'remaining_amount',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate_event_date(self, value):
        """
        Validate that the event date is not in the past
        """
        if value < timezone.now().date():
            raise serializers.ValidationError("Event date cannot be in the past")
        return value

    def validate(self, data):
        """
        Custom validation for the entire serializer
        """
        # Validate advance amount is not greater than total estimated amount
        if 'advance_amount' in data and 'per_dish_amount' in data and 'estimated_persons' in data:
            total_amount = data['per_dish_amount'] * data['estimated_persons']
            if data['advance_amount'] > total_amount:
                raise serializers.ValidationError({
                    'advance_amount': 'Advance amount cannot be greater than total estimated amount'
                })
        return data

class EventBookingCreateSerializer(EventBookingSerializer):
    """
    Serializer specifically for creating event bookings
    """
    class Meta(EventBookingSerializer.Meta):
        extra_kwargs = {
            'reference': {'required': True},
            'name': {'required': True},
            'mobile_no': {'required': True},
            'event_date': {'required': True},
            'event_time': {'required': True},
            'event_address': {'required': True},
            'advance_amount': {'required': True},
            'per_dish_amount': {'required': True},
            'estimated_persons': {'required': True},
        }

class EventBookingUpdateSerializer(EventBookingSerializer):
    """
    Serializer specifically for updating event bookings
    """
    class Meta(EventBookingSerializer.Meta):
        # Make certain fields optional during updates
        extra_kwargs = {
            'reference': {'required': False},
            'name': {'required': False},
            'mobile_no': {'required': False},
            'event_date': {'required': False},
            'event_time': {'required': False},
            'event_address': {'required': False},
            'advance_amount': {'required': False},
            'per_dish_amount': {'required': False},
            'estimated_persons': {'required': False},
        }

class EventBookingListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for list views
    """
    class Meta:
        model = EventBooking
        fields = [
            'id',
            'name',
            'reference',
            'event_date',
            'event_time',
            'total_estimated_amount',
            'remaining_amount'
        ]
