from rest_framework.response import Response
from rest_framework import status, generics
from .serializers import *


# --------------------    PaymentViewSet    --------------------


class PaymentViewSet(generics.GenericAPIView):
    serializer_class = PaymentSerializer

    def get(self, request):
        payments = Payment.objects.all().order_by("-payment_date")
        serializer = PaymentSerializer(payments, many=True)
        return Response(
            {
                "status": True,
                "message": "Payment list retrieved successfully",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        # Validate the input using the serializer
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            billed_to_ids = data.get("billed_to_ids", [])
            total_amount = data.get("total_amount", 0)
            advance_amount = data.get("advance_amount", 0)
            total_extra_amount = data.get("total_extra_amount", 0)

            # Initialize lists
            event_booking_name_list = []
            event_booking_mobile_no_list = []

            # Populate lists based on billed_to_ids
            if billed_to_ids:
                for bill_id in billed_to_ids:
                    try:
                        event_booking = EventBooking.objects.get(id=bill_id)
                        event_booking_name_list.append(event_booking.name)
                        event_booking_mobile_no_list.append(event_booking.mobile_no)
                    except EventBooking.DoesNotExist:
                        return Response(
                            {
                                "status": False,
                                "message": f"EventBooking with ID {bill_id} does not exist.",
                                "data": {},
                            },
                            status=status.HTTP_400_BAD_REQUEST,
                        )

            # Check Payments and update/create logic
            payments = Payment.objects.all().filter(
                payment_status__in=["PARTIAL", "UNPAID"]
            )
            payment_found = False

            for payment in payments:
                event_bookings = EventBooking.objects.filter(
                    id__in=payment.billed_to_ids
                )
                for event_booking in event_bookings:
                    if (
                        event_booking.name in event_booking_name_list
                        and event_booking.mobile_no in event_booking_mobile_no_list
                    ):
                        # Update the existing payments
                        payment.billed_to_ids.extend(billed_to_ids)
                        payment.total_amount += total_amount
                        payment.advance_amount += advance_amount
                        payment.pending_amount = (
                            payment.total_amount - payment.advance_amount
                        )
                        payment.total_extra_amount += total_extra_amount
                        payment.save()
                        payment_found = True
                        break

            if not payment_found:
                # Create a new payment
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
            payment = Payment.objects.get(pk=pk)
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
            request.data["advance_amount"] = str(
                int(request.data.get("transaction_amount")) + payment.advance_amount
            )
            # request.data["transaction_amount"] = str(int(request.data.get("transaction_amount")) + payment.transaction_amount)
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


class AllTransactionViewSet(generics.GenericAPIView):
    """
    User Login ViewSet
    """

    def get(self, request):
        payments = Payment.objects.all()
        if not payments.exists():
            return Response(
                {
                    "status": False,
                    "message": "No transactions found",
                    "data": {},
                },
                status=status.HTTP_200_OK,
            )
        net_amount = 0
        total_paid_amount = 0
        total_unpaid_amount = 0
        total_settlement_amount = 0
        final_response = {}
        for payment in payments:
            if payment.payment_status == "PAID":
                total_paid_amount += payment.total_amount
            elif payment.payment_status in ["UNPAID", "PARTIAL"]:
                total_unpaid_amount += payment.pending_amount
                total_paid_amount += payment.advance_amount
            total_settlement_amount += payment.settlement_amount
            net_amount += payment.total_amount

        final_response["net_amount"] = int(net_amount)
        final_response["total_paid_amount"] = int(total_paid_amount)
        final_response["total_unpaid_amount"] = int(total_unpaid_amount)
        final_response["total_settlement_amount"] = int(total_settlement_amount)
        return Response(
            {
                "status": True,
                "message": "Transaction list",
                "data": final_response,
            },
            status=status.HTTP_200_OK,
        )