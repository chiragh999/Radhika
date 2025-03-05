from rest_framework.response import Response
from rest_framework import status, generics
from .models import *
from .serializers import *


# Create your views here.
class IngridientsCategoryViewset(generics.GenericAPIView):
    serializer_class = IngridientsCategorySerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self,request,pk=None):
        if pk:
            queryset = IngridientsCategory.objects.filter(pk=pk)
        else:
            queryset = IngridientsCategory.objects.all()

        serializer = IngridientsCategorySerializer(queryset, many=True)

        return Response(
            {
                "status": True,
                "message": "Ingridients Category list",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def put(self, request, pk=None, *args, **kwargs):
        try:
            instance = IngridientsCategory.objects.get(pk=pk)
        except IngridientsCategory.DoesNotExist:
            return Response(
                {"status": False, "message": "Ingridients Categories not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None, *args, **kwargs):
        try:
            instance = IngridientsCategory.objects.get(pk=pk)
        except IngridientsCategory.DoesNotExist:
            return Response(
                {"status": False, "message": "Ingridients Categories not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        instance.delete()
        return Response(
            {"status": True, "message": "Ingridients Categories deleted"},
            status=status.HTTP_204_NO_CONTENT,
        )


class IngridientsItemViewset(generics.GenericAPIView):
    serializer_class = IngridientsItemSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self,request,pk=None):
        if pk:
            queryset = IngridientsItem.objects.filter(pk=pk)
        else:
            queryset = IngridientsItem.objects.all()
        serializer = IngridientsItemSerializer(queryset, many=True)
        return Response(
            {
                "status": True,
                "message": "Ingridients Item list",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def put(self, request, pk=None, *args, **kwargs):
        try:
            instance = IngridientsItem.objects.get(pk=pk)
        except IngridientsItem.DoesNotExist:
            return Response(
                {"status": False, "message": "Ingridients Item not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None, *args, **kwargs):
        try:
            instance = IngridientsItem.objects.get(pk=pk)
        except IngridientsItem.DoesNotExist:
            return Response(
                {"status": False, "message": "Ingridients Item not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        instance.delete()
        return Response(
            {"status": True, "message": "Ingridients Item deleted"},
            status=status.HTTP_204_NO_CONTENT,
        )
