from django.urls import path
from .views import *
urlpatterns = [
     path("login/",LoginViewSet.as_view()),
     path("category/",CategoryViewSet.as_view()),
     path("category/<int:pk>/",CategoryGetViewSet.as_view()),
     path("item/",ItemViewSet.as_view()),
     path("item/<int:pk>/",ItemGetViewSet.as_view()),
     path("event/",EventBookingViewSet.as_view()),
     path("evnet/<int:pk>/",EventBookingGetViewSet.as_view()),
     path("eventfilter/",EventFilterViewSet.as_view()),
     
]