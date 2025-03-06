from rest_framework.response import Response
from rest_framework import status, generics
from Radhika.Utils.permissions import *
from .models import *
from .serializers import *


# --------------------    IngridientsCategoryViewset    --------------------


class IngridientsCategoryViewset(generics.GenericAPIView):
    serializer_class = IngridientsCategorySerializer
    permission_classes = [IsAdminUserOrReadOnly]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_200_OK)

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
                status=status.HTTP_200_OK,
            )
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_200_OK)

    def delete(self, request, pk=None, *args, **kwargs):
        try:
            instance = IngridientsCategory.objects.get(pk=pk)
        except IngridientsCategory.DoesNotExist:
            return Response(
                {"status": False, "message": "Ingridients Categories not found"},
                status=status.HTTP_200_OK,
            )
        instance.delete()
        return Response(
            {"status": True, "message": "Ingridients Categories deleted"},
            status=status.HTTP_200_OK,
        )


# --------------------    IngridientsItemViewset    --------------------


class IngridientsItemViewset(generics.GenericAPIView):
    serializer_class = IngridientsItemSerializer
    permission_classes = [IsAdminUserOrReadOnly]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_200_OK)

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
                status=status.HTTP_200_OK,
            )
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_200_OK)

    def delete(self, request, pk=None, *args, **kwargs):
        try:
            instance = IngridientsItem.objects.get(pk=pk)
        except IngridientsItem.DoesNotExist:
            return Response(
                {"status": False, "message": "Ingridients Item not found"},
                status=status.HTTP_200_OK,
            )
        instance.delete()
        return Response(
            {"status": True, "message": "Ingridients Item deleted"},
            status=status.HTTP_200_OK,
        )


class EventIngridientListViewSet(generics.GenericAPIView):
    # queryset = EventIngridientList.objects.all()
    serializer_class = EventIngridientListSerializer

    def post(self, request, *args, **kwargs):
        event_id = request.data.get('event_id')
        if not event_id:
            return Response({'error': 'event_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        instance, created = EventIngridientList.objects.update_or_create(
            event_id=event_id,
            defaults={'ingridient_list_data': request.data.get('ingridient_list_data', {})}
        )
        
        serializer = self.get_serializer(instance)
        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response(serializer.data, status=status_code)
