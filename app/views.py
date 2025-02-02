from rest_framework.response import Response
from rest_framework import status, generics
from django.contrib.auth import authenticate
from .models import Category, Item, EventBooking
from .serializers import *
from datetime import date, datetime
from decimal import Decimal


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


# --------------------    CategoryViewSet    --------------------


class CategoryViewSet(generics.GenericAPIView):
    serializer_class = CategorySerializer

    def post(self, request):
        if Category.objects.filter(name=request.data.get("name")).exists():
            return Response(
                {
                    "status": False,
                    "message": "Category already exists",
                    "data": {},
                },
                status=status.HTTP_200_OK,
            )
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {
                    "status": True,
                    "message": "Category created successfully",
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
        queryset = Category.objects.all()
        serializer = CategorySerializer(queryset, many=True)
        return Response(
            {
                "status": True,
                "message": "Category list",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class CategoryGetViewSet(generics.GenericAPIView):
    serializer_class = CategorySerializer

    def put(self, request, pk=None):
        try:
            category = Category.objects.get(pk=pk)
            serializer = CategorySerializer(category, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(
                    {
                        "status": True,
                        "message": "Category updated successfully",
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
        except Category.DoesNotExist:
            return Response(
                {
                    "status": False,
                    "message": "Category not found",
                    "data": {},
                },
                status=status.HTTP_200_OK,
            )

    def delete(self, request, pk=None):
        try:
            category = Category.objects.get(pk=pk)
            category.delete()
            return Response(
                {
                    "status": True,
                    "message": "Category deleted successfully",
                    "data": {},
                },
                status=status.HTTP_200_OK,
            )
        except Category.DoesNotExist:
            return Response(
                {
                    "status": False,
                    "message": "Category not found",
                    "data": {},
                },
                status=status.HTTP_200_OK,
            )

    def get(self, request, pk=None):
        try:
            category = Category.objects.get(pk=pk)
            serializer = CategorySerializer(category)
            return Response(
                {
                    "status": True,
                    "message": "Category retrieved successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        except Category.DoesNotExist:
            return Response(
                {
                    "status": False,
                    "message": "Category not found",
                    "data": {},
                },
                status=status.HTTP_200_OK,
            )


# --------------------    ItemViewSet    --------------------


class ItemViewSet(generics.GenericAPIView):
    serializer_class = ItemSerializer

    def post(self, request):
        if Item.objects.filter(name=request.data.get("name")).exists():
            return Response(
                {
                    "status": False,
                    "message": "Item already exists",
                    "data": {},
                },
                status=status.HTTP_200_OK,
            )
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {
                    "status": True,
                    "message": "Item created successfully",
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
        queryset = Item.objects.all()
        serializer = ItemSerializer(queryset, many=True)
        return Response(
            {
                "status": True,
                "message": "Item list",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class ItemGetViewSet(generics.GenericAPIView):
    serializer_class = ItemSerializer

    def put(self, request, pk=None):
        try:
            item = Item.objects.get(pk=pk)
            serializer = ItemSerializer(item, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(
                    {
                        "status": True,
                        "message": "Item updated successfully",
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
        except Item.DoesNotExist:
            return Response(
                {
                    "status": False,
                    "message": "Item not found",
                    "data": {},
                },
                status=status.HTTP_200_OK,
            )

    def get(self, request, pk=None):
        try:
            item = Item.objects.get(pk=pk)
            serializer = ItemSerializer(item)
            return Response(
                {
                    "status": True,
                    "message": "Item retrieved successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        except Item.DoesNotExist:
            return Response(
                {
                    "status": False,
                    "message": "Item not found",
                    "data": {},
                },
                status=status.HTTP_200_OK,
            )

    def delete(self, request, pk=None):
        try:
            item = Item.objects.get(pk=pk)
            item.delete()
            return Response(
                {
                    "status": True,
                    "message": "Item deleted successfully",
                    "data": {},
                },
                status=status.HTTP_200_OK,
            )
        except Item.DoesNotExist:
            return Response(
                {
                    "status": False,
                    "message": "Item not found",
                    "data": {},
                },
                status=status.HTTP_200_OK,
            )


# --------------------    EventBookingViewSet    --------------------


class EventBookingViewSet(generics.GenericAPIView):
    serializer_class = EventBookingSerializer

    def post(self, request):
        # Convert the selected_items payload
        selected_items = request.data.get("selected_items", {})
        converted_payload = {
            key: [{"name": item} for item in value]
            for key, value in selected_items.items()
        }
        request.data["selected_items"] = converted_payload

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
        queryset = EventBooking.objects.all().filter(status__in=['confirm', 'completed'])
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

    def put(self, request, pk=None):
        try:
            eventbooking = EventBooking.objects.get(pk=pk)
            selected_items = request.data.get("selected_items", {})
            converted_payload = {
                key: [{"name": item} for item in value]
                for key, value in selected_items.items()
            }
            request.data["selected_items"] = converted_payload
            # converted_payload = {key: {"name": value[0]} for key, value in request.data.get("selected_items").items()}
            # request.data['selected_items'] = converted_payload
            serializer = EventBookingSerializer(eventbooking, data=request.data)
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


# --------------------    StokeItemViewSet    --------------------


class StokeItemViewSet(generics.GenericAPIView):
    serializer_class = StokeItemSerializer

    def get(self, request):
        queryset = StokeItem.objects.all()
        serializer = StokeItemSerializer(queryset, many=True)
        return Response(
            {
                "status": True,
                "message": "StokeItem list",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        if StokeItem.objects.filter(name=request.data.get("name")).exists():
            return Response(
                {
                    "status": False,
                    "message": "StokeItem already exists",
                    "data": {},
                },
                status=status.HTTP_200_OK,
            )
        serializer = StokeItemSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {
                    "status": True,
                    "message": "StokeItem created successfully",
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


class EditStokeItemViewSet(generics.GenericAPIView):
    serializer_class = StokeItemSerializer

    def get(self, request, pk=None):
        try:
            stokeitem = StokeItem.objects.get(pk=pk)
            serializer = StokeItemSerializer(stokeitem)
            return Response(
                {
                    "status": True,
                    "message": "StokeItem retrieved successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        except StokeItem.DoesNotExist:
            return Response(
                {
                    "status": False,
                    "message": "StokeItem not found",
                    "data": {},
                },
                status=status.HTTP_200_OK,
            )

    def put(self, request, pk=None):
        try:
            stokeitem = StokeItem.objects.get(pk=pk)
            request.data["quantity"] = str(
                int(request.data["quantity"]) + int(stokeitem.quantity)
            )
            request.data["total_price"] = str(
                int(request.data["total_price"]) + int(stokeitem.total_price)
            )
            request.data["nte_price"] = str(
                int(int(request.data["total_price"]) / int(request.data["quantity"]))
            )
            serializer = StokeItemSerializer(stokeitem, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(
                    {
                        "status": True,
                        "message": "StokeItem updated successfully",
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
        except StokeItem.DoesNotExist:
            return Response(
                {
                    "status": False,
                    "message": "StokeItem not found",
                    "data": {},
                },
                status=status.HTTP_200_OK,
            )

    def delete(self, request, pk=None):
        try:
            stokeitem = StokeItem.objects.get(pk=pk)
            stokeitem.delete()
            return Response(
                {
                    "status": True,
                    "message": "StokeItem deleted successfully",
                    "data": {},
                },
                status=status.HTTP_200_OK,
            )
        except StokeItem.DoesNotExist:
            return Response(
                {
                    "status": False,
                    "message": "StokeItem not found",
                    "data": {},
                },
                status=status.HTTP_200_OK,
            )


# --------------------    AddRemoveStokeItemViewSet    --------------------


class AddRemoveStokeItemViewSet(generics.GenericAPIView):

    def post(self, request):
        if not StokeItem.objects.filter(
            id=request.data.get("id"), name=request.data.get("name")
        ).exists():
            return Response(
                {
                    "status": False,
                    "message": "StokeItem is not exists",
                    "data": {},
                },
                status=status.HTTP_200_OK,
            )
        quantity = request.data.get("quantity")
        nte_price = request.data.get("nte_price")
        total_price = request.data.get("total_price", None)
        price = ""
        stoke_item = StokeItem.objects.get(
            id=request.data.get("id"), name=request.data.get("name")
        )
        result = stoke_item.quantity - Decimal(quantity)
        if total_price:
            price = total_price
        else:
            price = str(int(quantity) * int(nte_price))
        stoke_item.total_price = str(int(stoke_item.total_price) - int(price))
        stoke_item.quantity = result
        stoke_item.save()
        return Response(
            {
                "status": True,
                "message": "StokeItem Quantity Remove successfully",
                "data": {
                    "id": stoke_item.id,
                    "name": stoke_item.name,
                    "quantity": str(stoke_item.quantity),
                    "nte_price": str(stoke_item.nte_price),
                    "total_price": str(stoke_item.total_price),
                },
            },
            status=status.HTTP_200_OK,
        )

    def put(self, request):
        if not StokeItem.objects.filter(
            id=request.data.get("id"), name=request.data.get("name")
        ).exists():
            return Response(
                {
                    "status": False,
                    "message": "StokeItem is not exists",
                    "data": {},
                },
                status=status.HTTP_200_OK,
            )
        quantity = request.data.get("quantity")
        total_price = request.data.get("total_price", None)
        stoke_item = StokeItem.objects.get(
            id=request.data.get("id"), name=request.data.get("name")
        )
        result = stoke_item.quantity + Decimal(quantity)
        stoke_item.quantity = result
        if total_price:
            stoke_item.total_price = str(int(stoke_item.total_price) + int(total_price))
            stoke_item.nte_price = str(
                int(int(stoke_item.total_price) / int(stoke_item.quantity))
            )
        else:
            total_price = str(int(quantity) * int(stoke_item.nte_price))
            stoke_item.total_price = int(int(stoke_item.total_price) + int(total_price))
            stoke_item.nte_price = str(
                int(int(stoke_item.total_price) / int(stoke_item.quantity))
            )
        stoke_item.save()
        return Response(
            {
                "status": True,
                "message": "StokeItem Quantity Added successfully",
                "data": {
                    "id": stoke_item.id,
                    "name": stoke_item.name,
                    "quantity": str(stoke_item.quantity),
                    "nte_price": str(stoke_item.nte_price),
                    "total_price": str(stoke_item.total_price),
                },
            },
            status=status.HTTP_200_OK,
        )


# --------------------    AddRemoveStokeItemViewSet    --------------------


class AlertstokeItemViewSet(generics.GenericAPIView):

    def get(self, request):
        alerts_list = []
        all_stoke_itmes = StokeItem.objects.all()
        for stokes in all_stoke_itmes:
            if stokes.type == "KG":
                # value_in_kilograms = stokes.quantity / Decimal('1000')
                if stokes.quantity <= Decimal(stokes.alert.split(" ")[0]):
                    alerts_list.append(stokes)

            if stokes.type == "L":
                # liters = stokes.quantity / 1000
                if stokes.quantity <= Decimal(stokes.alert.split(" ")[0]):
                    alerts_list.append(stokes)

            if stokes.type == "QTY":
                if stokes.quantity <= Decimal(stokes.alert.split(" ")[0]):
                    alerts_list.append(stokes)

        serializer = StokeItemSerializer(alerts_list, many=True)

        return Response(
            {
                "status": True,
                "message": "StokeItem Quantity Added successfully",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


# --------------------    StokeCategoryViewSet    --------------------


class StokeCategoryViewSet(generics.GenericAPIView):
    serializer_class = StokeCategorySerializer

    def post(self, request):
        if StokeCategory.objects.filter(name=request.data.get("name")).exists():
            return Response(
                {
                    "status": False,
                    "message": "Category already exists",
                    "data": {},
                },
                status=status.HTTP_200_OK,
            )
        serializer = StokeCategorySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {
                    "status": True,
                    "message": "Category created successfully",
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
        queryset = StokeCategory.objects.all()
        serializer = StokeCategorySerializer(queryset, many=True)
        return Response(
            {
                "status": True,
                "message": "Category list",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class EditeStokeCategoryViewSet(generics.GenericAPIView):
    serializer_class = StokeCategorySerializer

    def put(self, request, pk=None):
        try:
            category = StokeCategory.objects.get(pk=pk)
            serializer = StokeCategorySerializer(category, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(
                    {
                        "status": True,
                        "message": "Category updated successfully",
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
        except StokeCategory.DoesNotExist:
            return Response(
                {
                    "status": False,
                    "message": "Category not found",
                    "data": {},
                },
                status=status.HTTP_200_OK,
            )

    def delete(self, request, pk=None):
        try:
            category = StokeCategory.objects.get(pk=pk)
            category.delete()
            return Response(
                {
                    "status": True,
                    "message": "Category deleted successfully",
                    "data": {},
                },
                status=status.HTTP_200_OK,
            )
        except StokeCategory.DoesNotExist:
            return Response(
                {
                    "status": False,
                    "message": "Category not found",
                    "data": {},
                },
                status=status.HTTP_200_OK,
            )

    def get(self, request, pk=None):
        try:
            category = StokeCategory.objects.get(pk=pk)
            serializer = StokeCategorySerializer(category)
            return Response(
                {
                    "status": True,
                    "message": "Category retrieved successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        except StokeCategory.DoesNotExist:
            return Response(
                {
                    "status": False,
                    "message": "Category not found",
                    "data": {},
                },
                status=status.HTTP_200_OK,
            )


# --------------------    PaymentViewSet    --------------------


class PaymentViewSet(generics.GenericAPIView):
    serializer_class = PaymentSerializer

    def get(self, request):
        queryset = Payment.objects.select_related("billed_to").all()
        serializer = PaymentSerializer(queryset, many=True)
        return Response(
            {
                "status": True,
                "message": "Payment list retrieved successfully",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        if Payment.objects.filter(bill_no=request.data.get("bill_no")).exists():
            return Response(
                {
                    "status": False,
                    "message": "Payment with this bill number already exists",
                    "data": {},
                },
                status=status.HTTP_200_OK,
            )

        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {
                    "status": True,
                    "message": "Payment created successfully",
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


class EditPaymentViewSet(generics.GenericAPIView):
    serializer_class = PaymentSerializer

    def get(self, request, pk=None):
        try:
            payment = Payment.objects.select_related("billed_to").get(pk=pk)
            serializer = PaymentSerializer(payment)
            return Response(
                {
                    "status": True,
                    "message": "Payment retrieved successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        except Payment.DoesNotExist:
            return Response(
                {
                    "status": False,
                    "message": "Payment not found",
                    "data": {},
                },
                status=status.HTTP_200_OK,
            )

    def put(self, request, pk=None):
        try:
            payment = Payment.objects.get(pk=pk)

            # Update pending amount based on new transaction
            new_transaction_amount = float(request.data.get("transaction_amount", 0))
            current_pending = float(payment.pending_amount)
            request.data["advance_amount"] = payment.advance_amount
            if new_transaction_amount > current_pending:
                return Response(
                    {
                        "status": False,
                        "message": "Transaction amount cannot exceed pending amount",
                        "data": {},
                    },
                    status=status.HTTP_200_OK,
                )

            serializer = PaymentSerializer(payment, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(
                    {
                        "status": True,
                        "message": "Payment updated successfully",
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
        except Payment.DoesNotExist:
            return Response(
                {
                    "status": False,
                    "message": "Payment not found",
                    "data": {},
                },
                status=status.HTTP_200_OK,
            )

    def delete(self, request, pk=None):
        try:
            payment = Payment.objects.get(pk=pk)
            payment.delete()
            return Response(
                {
                    "status": True,
                    "message": "Payment deleted successfully",
                    "data": {},
                },
                status=status.HTTP_200_OK,
            )
        except Payment.DoesNotExist:
            return Response(
                {
                    "status": False,
                    "message": "Payment not found",
                    "data": {},
                },
                status=status.HTTP_200_OK,
            )


# --------------------    PendingEventBookingViewSet    --------------------


class PendingEventBookingViewSet(generics.GenericAPIView):
    serializer_class = EventBookingSerializer
    def get(self, request):
        queryset = EventBooking.objects.all().filter(status = "pending")
        serializer = EventBookingSerializer(queryset, many=True)
        return Response(
            {
                "status": True,
                "message": "EventBooking list",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


# --------------------    PendingEventBookingViewSet    --------------------


class StatusChangeEventBookingViewSet(generics.GenericAPIView):
    serializer_class = EventBookingSerializer
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
