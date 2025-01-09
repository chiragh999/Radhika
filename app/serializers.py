from rest_framework import serializers
from .models import *

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'category']

class CategorySerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'items']

class EventBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventBooking
        fields = [
            'id',  # Include the primary key for reference
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
            'selected_items',
            'description',
            'created_at',
            'updated_at'
        ]