from rest_framework.response import Response
from rest_framework import status, generics
from Radhika.Utils.permissions import *
from .serializers import *

# --------------------    EventBookingViewSet    --------------------


class EventBookingViewSet(generics.GenericAPIView):
    serializer_class = EventBookingSerializer
    permission_classes = [IsAdminUserOrReadOnly]

    def post(self, request):
        # Convert the selected_items payload
        selected_items = request.data.get("selected_items", {})
        converted_payload = {
            key: [{"name": item} for item in value]
            for key, value in selected_items.items()
        }
        request.data["selected_items"] = converted_payload
        amount = 0
        for extra_service in request.data["extra_service"]:
            if extra_service.get("amount"):
                amount = amount + int(extra_service.get("amount"))
            else:
                amount = 0
        request.data["extra_service_amount"] = str(amount)

        # converted_payload = {key: {"name": value[0]} for key, value in request.data.get("selected_items").items()}
        # request.data['selected_items'] = converted_payload
        serializer = EventBookingSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {
                    "status": True,
                    "message": "EventBooking created successfully",
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
        queryset = (
            EventBooking.objects.all()
            .filter(status__in=["confirm", "completed"])
            .order_by("-event_date")
        )
        serializer = EventBookingSerializer(queryset, many=True)
        return Response(
            {
                "status": True,
                "message": "EventBooking list",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class EventBookingGetViewSet(generics.GenericAPIView):
    serializer_class = EventBookingSerializer
    permission_classes = [IsAdminUserOrReadOnly]

    def put(self, request, pk=None):
        try:
            eventbooking = EventBooking.objects.get(pk=pk)
            selected_items = request.data.get("selected_items", {})
            if selected_items:
                converted_payload = {
                    key: [{"name": item} for item in value]
                    for key, value in selected_items.items()
                }
                request.data["selected_items"] = converted_payload
            else:
                request.data["selected_items"] = eventbooking.selected_items
            # Partially update the instance with only provided fields
            serializer = EventBookingSerializer(eventbooking, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(
                    {
                        "status": True,
                        "message": "EventBooking updated successfully",
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
        except EventBooking.DoesNotExist:
            return Response(
                {
                    "status": False,
                    "message": "EventBooking not found",
                    "data": {},
                },
                status=status.HTTP_200_OK,
            )

    def get(self, request, pk=None):
        try:
            eventbooking = EventBooking.objects.get(pk=pk)
            serializer = EventBookingSerializer(eventbooking)
            return Response(
                {
                    "status": True,
                    "message": "EventBooking retrieved successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        except EventBooking.DoesNotExist:
            return Response(
                {
                    "status": False,
                    "message": "EventBooking not found",
                    "data": {},
                },
                status=status.HTTP_200_OK,
            )

    def delete(self, request, pk=None):
        try:
            eventbooking = EventBooking.objects.get(pk=pk)
            eventbooking.delete()
            return Response(
                {
                    "status": True,
                    "message": "EventBooking deleted successfully",
                    "data": {},
                },
                status=status.HTTP_200_OK,
            )
        except EventBooking.DoesNotExist:
            return Response(
                {
                    "status": False,
                    "message": "EventBooking not found",
                    "data": {},
                },
                status=status.HTTP_200_OK,
            )


# --------------------    StatusChangeEventBookingViewSet    --------------------


class StatusChangeEventBookingViewSet(generics.GenericAPIView):
    serializer_class = EventBookingSerializer
    permission_classes = [IsOwnerOrAdmin]

    def post(self, request, pk=None):
        queryset = EventBooking.objects.get(pk=pk)
        queryset.status = request.data.get("status")
        queryset.save()
        return Response(
            {
                "status": True,
                "message": "EventBooking list",
                "data": {},
            },
            status=status.HTTP_200_OK,
        )


# --------------------    PendingEventBookingViewSet    --------------------


class PendingEventBookingViewSet(generics.GenericAPIView):
    serializer_class = EventBookingSerializer
    permission_classes = [IsAdminUserOrReadOnly]

    def get(self, request):
        queryset = EventBooking.objects.all().filter(status="pending").order_by("-date")
        serializer = EventBookingSerializer(queryset, many=True)
        return Response(
            {
                "status": True,
                "message": "EventBooking list",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

class GetAllEvent(generics.GenericAPIView):
    def get(self,request):
        queryset = EventBooking.objects.all()
        serializer = EventBookingSerializer(queryset, many=True)
        return Response(
            {
                "status": True,
                "message": "EventBooking list",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )