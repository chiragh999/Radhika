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

class NoteViewSet(generics.GenericAPIView):
    serializer_class = NoteSerializer

    # def post(self, request):
        
    #     serializer = NoteSerializer(data = request.data)

    #     if serializer.is_valid(raise_exception=True):
    #         serializer.save()

    #         return Response(
    #             {
    #                 "status": True,
    #                 "message": "Note Store successfully",
    #                 "data": {}
    #             },
    #             status=status.HTTP_200_OK,
    #         )
    #     return Response(
    #         {
    #             "status": False,
    #             "message": "Something went wrong",
    #             "data": {},
    #         },
    #         status=status.HTTP_200_OK,
    #     )

    def put(self, request,pk):

        get_note = Note.objects.filter(id=pk).first()
        if not get_note:
            return Response(
                {
                    "status": False,
                    "message": "Note not found",
                    "data": {},
                },
                status=status.HTTP_200_OK,
            )
        
        serializer = NoteSerializer(get_note, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(
                    {
                        "status": True,
                        "message": "Note updated successfully",
                        "data": serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )

        return Response(
                {
                    "status": False,
                    "message": "Something went wrong",
                    "data": {},
                },
                status=status.HTTP_200_OK,
            )
    
    def get(self, request):
        queryset = Note.objects.all()
        serializer = NoteSerializer(queryset, many=True)
        return Response(
            {
                "status": True,
                "message": "Note list",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )