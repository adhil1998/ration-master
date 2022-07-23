from rest_framework.generics import ListAPIView, ListCreateAPIView, \
    CreateAPIView, RetrieveAPIView

from accounts.constants import OTPType
from accounts.serializers import *
from accounts.models import Admin, RationShop, OtpToken
from common.exceptions import BadRequest
from common.permissions import IsAuthenticated
from common.functions import success_response
from common.services import send_otp
from rest_framework.views import APIView
from rest_framework.response import Response


class AdminCreateView(CreateAPIView, RetrieveAPIView):
    """Serializer for lis and create User(s)"""
    serializer_class = AdminSerializer
    queryset = Admin.objects.all()


class ShopCreateView(CreateAPIView, RetrieveAPIView):
    """Serializer for lis and create User(s)"""
    serializer_class = ShopSerializer
    queryset = RationShop.objects.all()


class CardCreateView(CreateAPIView, RetrieveAPIView):
    """Serializer for lis and create User(s)"""
    serializer_class = CardSerializer
    queryset = RationShop.objects.all()


class LoginView(CreateAPIView):
    """Serializer for lis and create User(s)"""
    serializer_class = LoginSerializer


class LoginOTPView(CreateAPIView):
    """Serializer for lis and create User(s)"""
    serializer_class = LoginOTPSerializer


class CreateOtp(APIView):
    """Create otp for card"""

    def get(self, request, user=None, *args, **kwargs):
        """Override get method"""
        try:
            number = self.request.GET.get('card_number')
            card = Card.objects.get(card_number=number)
            otp, created = OtpToken.objects.get_or_create(
                user=card, type=OTPType.LOGIN)
            otp.refresh()
            body = f"OTP to login into ration master {otp.otp}. valid for 10 mints"
            # send_otp(card.mobile, body)
        except Exception as e:
            raise BadRequest('INVALID CARD NUMBER' + str(e))
        data = {"hello": "world"}
        return Response(data)
