from django.urls import path
from .views import CategoryViewSet, LoginViewSet, ItemViewSet, EventBookingViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'', LoginViewSet, basename='login')
router.register(r'items', ItemViewSet, basename='item')
router.register('event-bookings', EventBookingViewSet, basename='event-booking')


urlpatterns = [
] + router.urls