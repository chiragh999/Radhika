from django.urls import path
from .views import *

urlpatterns = [
    path("login/", LoginViewSet.as_view()),
]