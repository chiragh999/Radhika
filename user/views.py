from rest_framework.response import Response
from rest_framework import status, generics
from django.contrib.auth import authenticate
from .serializers import *

# --------------------    LoginViewSet    --------------------


class LoginViewSet(generics.GenericAPIView):
    """
    User Login ViewSet
    """

    serializer_class = LoginSerializer

    def post(self, request):
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
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {
                    "status": False,
                    "message": "Something went wrong",  # Fixed typo
                    "data": {},
                },
                status=status.HTTP_200_OK,
            )
