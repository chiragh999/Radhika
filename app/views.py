from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import action
from rest_framework import status, viewsets 
from django.contrib.auth import authenticate
from django.utils import timezone
from .models import Category, Item, EventBooking
from .serializers import (
    CategorySerializer, LoginSerializer, ItemSerializer,
    EventBookingSerializer,
    EventBookingCreateSerializer,
    EventBookingUpdateSerializer,
    EventBookingListSerializer
)


# --------------------    CategoryViewSet    --------------------


class CategoryViewSet(viewsets.ModelViewSet):
    """
    A viewset for admin-only access to add, update, retrieve, and delete categories.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]

    
    def list(self, request):
        queryset = Category.objects.all()
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        try:
            category = Category.objects.get(pk=pk)
            serializer = CategorySerializer(category)
            return Response(serializer.data)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def update(self, request, pk=None):
        try:
            category = Category.objects.get(pk=pk)
            serializer = CategorySerializer(category, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk=None):
        try:
            category = Category.objects.get(pk=pk)
            category.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


# --------------------    LoginViewSet    --------------------


class LoginViewSet(viewsets.ViewSet):
    """
    User Login ViewSet
    """
    serializer_class = LoginSerializer

    @action(detail=False, methods=['post'])
    def login(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        
        if user:
            response_data = {
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "tokens": user.tokens,
            }
            return Response(
                {
                    "status": True,
                    "message": "Login successfully",
                    "data": response_data,
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {
                    "status": True,
                    "message": "Something went wrong",  # Fixed typo
                    "data": {},
                },
                status=status.HTTP_201_CREATED,
            )


# --------------------    ItemViewSet    --------------------


class ItemViewSet(viewsets.ModelViewSet):
    """
    A viewset for admin-only access to add, update, retrieve, and delete categories.
    """
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAdminUser]

    def list(self, request):
        queryset = Item.objects.all()
        category = request.query_params.get('category', None)
        print(category,'category')
        if category:
            queryset = queryset.filter(category=category)
        serializer = ItemSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        try:
            item = Item.objects.get(pk=pk)
            serializer = ItemSerializer(item)
            return Response(serializer.data)
        except Item.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def update(self, request, pk=None):
        try:
            item = Item.objects.get(pk=pk)
            serializer = ItemSerializer(item, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Item.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, pk=None):
        try:
            item = Item.objects.get(pk=pk)
            item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Item.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


# --------------------    EventBookingViewSet    --------------------


class EventBookingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling Event Booking operations.
    
    list:
        Get all event bookings with pagination
    create:
        Create a new event booking
    retrieve:
        Get a specific event booking by ID
    update:
        Update a specific event booking
    partial_update:
        Partially update a specific event booking
    destroy:
        Delete a specific event booking
    """
    queryset = EventBooking.objects.all()
    permission_classes = [IsAdminUser]
    # filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    
    # Filter fields
    filterset_fields = {
        'event_date': ['exact', 'gte', 'lte'],
        'created_at': ['exact', 'gte', 'lte'],
        'estimated_persons': ['exact', 'gte', 'lte'],
    }
    
    # Search fields
    search_fields = ['name', 'reference', 'mobile_no', 'event_address']
    
    # Ordering fields
    ordering_fields = ['event_date', 'created_at', 'estimated_persons']
    ordering = ['-created_at']

    def get_serializer_class(self):
        """
        Return appropriate serializer class based on the action
        """
        if self.action == 'create':
            return EventBookingCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return EventBookingUpdateSerializer
        elif self.action == 'list':
            return EventBookingListSerializer
        return EventBookingSerializer

    def get_queryset(self):
        """
        Custom queryset to filter upcoming/past events
        """
        queryset = EventBooking.objects.all()
        upcoming = self.request.query_params.get('upcoming', None)
        
        if upcoming is not None:
            today = timezone.now().date()
            if upcoming.lower() == 'true':
                queryset = queryset.filter(event_date__gte=today)
            elif upcoming.lower() == 'false':
                queryset = queryset.filter(event_date__lt=today)
                
        return queryset

    @action(detail=True, methods=['post'])
    def update_advance_payment(self, request, pk=None):
        """
        Custom action to update advance payment
        """
        booking = self.get_object()
        new_advance = request.data.get('advance_amount')
        
        if not new_advance:
            return Response(
                {'error': 'advance_amount is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            new_advance = float(new_advance)
            if new_advance < 0:
                raise ValueError
        except ValueError:
            return Response(
                {'error': 'Invalid advance amount'},
                status=status.HTTP_400_BAD_REQUEST
            )

        booking.advance_amount = new_advance
        booking.save()
        
        serializer = self.get_serializer(booking)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def upcoming_events(self, request):
        """
        Get all upcoming events
        """
        today = timezone.now().date()
        events = self.get_queryset().filter(event_date__gte=today)
        serializer = EventBookingListSerializer(events, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def today_events(self, request):
        """
        Get all events scheduled for today
        """
        today = timezone.now().date()
        events = self.get_queryset().filter(event_date=today)
        serializer = EventBookingListSerializer(events, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        """
        Custom create method
        """
        serializer.save()

    def perform_update(self, serializer):
        """
        Custom update method
        """
        serializer.save()


# --------------------    CategoryViewSet    --------------------

