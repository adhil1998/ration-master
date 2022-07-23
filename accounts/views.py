from rest_framework.generics import ListAPIView, ListCreateAPIView, \
    CreateAPIView, RetrieveAPIView, UpdateAPIView

from accounts.constants import OTPType
from accounts.filter import CardFilter, ShopFilter
from accounts.serializers import *
from accounts.models import Admin, RationShop, OtpToken
from common.exceptions import BadRequest
from common.permissions import IsAuthenticated, IsAdmin, MultiPermissionView, IsShop
from common.functions import success_response, decode
from common.services import send_otp
from rest_framework.views import APIView
from rest_framework.response import Response


class AdminCreateView(CreateAPIView, RetrieveAPIView):
    """Serializer for lis and create User(s)"""
    serializer_class = AdminSerializer
    queryset = Admin.objects.all()


class ShopCreateView(ListCreateAPIView, RetrieveAPIView, MultiPermissionView):
    """Serializer for lis and create User(s)"""
    permissions = {
        'GET': (
            IsAuthenticated, IsAdmin),
        'POST': ()
    }
    serializer_class = ShopSerializer
    queryset = RationShop.objects.all()
    filterset_class = ShopFilter


class CardCreateView(ListCreateAPIView, RetrieveAPIView, MultiPermissionView):
    """Serializer for lis and create User(s)"""
    permissions = {
        'GET': (
            IsAuthenticated, IsAdmin or IsShop),
        'POST': ()
    }
    serializer_class = CardSerializer
    queryset = Card.objects.all()
    filterset_class = CardFilter


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
        data = {"otp": otp.otp}
        return Response(data)


class VerifyShopView(APIView):
    """to verify shops"""
    permission_classes = (IsAuthenticated, IsAdmin)

    def patch(self, request, *args, **kwargs):
        """Override get method"""
        try:
            shop = RationShop.objects.get(id=kwargs['pk'])
            shop.verified = True
            shop.save()
            return success_response('shop is verified now')
        except:
            raise BadRequest("INVALID ID")


class VerifyCardView(UpdateAPIView):
    """to verify shops"""
    permission_classes = (IsAuthenticated, IsAdmin)

    def get(self, request, *args, **kwargs):
        """Override get method"""
        try:
            shop = Card.objects.get(id=kwargs['pk'])
            shop.verified = True
            shop.save()
            return success_response('shop is verified now')
        except:
            raise BadRequest("INVALID ID")
