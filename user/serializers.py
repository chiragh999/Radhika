from rest_framework import serializers
from .models import *

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

class NoteSerializer(serializers.ModelSerializer):

     class Meta:
        model = Note
        fields = ['id','title','content']