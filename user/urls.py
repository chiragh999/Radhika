from django.urls import path
from .views import *

urlpatterns = [
    path("login/", LoginViewSet.as_view()),
    path("add-note/",NoteViewSet.as_view()),
    path("get-note/",NoteViewSet.as_view()),
    path("update-note/<int:pk>",NoteViewSet.as_view())
]