from rest_framework.generics import ListAPIView, ListCreateAPIView, \
    CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView

from accounts.constants import OTPType
from accounts.filter import CardFilter, ShopFilter
from accounts.serializers import *
from accounts.models import Admin, RationShop, OtpToken
from common.exceptions import BadRequest
from common.permissions import IsAuthenticated, IsAdmin, \
    MultiPermissionView, IsShop, IsCard
from common.functions import success_response, decode
from common.services import send_otp
from rest_framework.views import APIView
from rest_framework.response import Response

from supply.models import Token


class AdminCreateView(CreateAPIView, RetrieveAPIView):
    """Serializer for lis and create User(s)"""
    serializer_class = AdminSerializer
    queryset = Admin.objects.all()


class ShopCreateView(ListCreateAPIView, MultiPermissionView):
    """Serializer for lis and create User(s)"""
    permissions = {
        'GET': (
            IsAuthenticated, IsAdmin),
        'POST': ()
    }
    serializer_class = ShopSerializer
    queryset = RationShop.objects.all()
    filterset_class = ShopFilter


class ShopDetailView(RetrieveAPIView,):
    """Serializer for lis and create User(s)"""
    permissions = {
        'GET': (
            IsAuthenticated),
    }
    serializer_class = ShopSerializer
    queryset = RationShop.objects.all()
    filterset_class = ShopFilter


class CardCreateView(ListCreateAPIView, MultiPermissionView):
    """Serializer for lis and create User(s)"""
    permissions = {
        'GET': (
            IsAuthenticated, IsAdmin or IsShop),
        'POST': ()
    }
    serializer_class = CardSerializer
    queryset = Card.objects.all()
    filterset_class = CardFilter


class CardDetailView(RetrieveAPIView,):
    """Serializer for lis and create User(s)"""
    permissions = {
        'GET': (
            IsAuthenticated),
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
            send_otp(card.mobile, body)
        except Exception as e:
            raise BadRequest('INVALID CARD NUMBER' + str(e))
        data = {"otp": otp.otp}
        return Response(data)


class VerifyShopView(UpdateAPIView, DestroyAPIView):
    """to verify shops"""
    permission_classes = (IsAuthenticated, IsAdmin)

    def patch(self, request, *args, **kwargs):
        """Override get method"""
        try:
            shop = RationShop.objects.get(id=kwargs['pk'])
            shop.verified = True
            shop.save()
            send_otp(shop.mobile, f'Dear {shop.holder_name}, '
                                  f'Your Ration shop verified.....Enjoyyyyy::))))')
            return success_response('shop is verified now')
        except:
            raise BadRequest("INVALID ID")

    def destroy(self, request, *args, **kwargs):
        """Override delete"""
        try:
            shop = RationShop.objects.get(id=kwargs['pk'])
            send_otp(shop.mobile, f'Dear {shop.username},Your shop permission rejected..Enjoyyyyy:)')
            shop.delete()
        except:
            raise BadRequest('Card not found')
        return success_response('deleted')


class VerifyCardView(UpdateAPIView, DestroyAPIView):
    """to verify shops"""
    permission_classes = (IsAuthenticated, IsAdmin)

    def patch(self, request, *args, **kwargs):
        """Override get method"""
        try:
            card = Card.objects.get(id=kwargs['pk'])
            card.verified = True
            card.save()
            send_otp(card.mobile, f'Dear {card.holder_name}, Your Ration card verified.....Enjoyyyyy::))))')
            return success_response('shop is verified now')
        except:
            raise BadRequest("INVALID ID")

    def destroy(self, request, *args, **kwargs):
        """Override delete"""
        try:
            card = Card.objects.get(id=kwargs['pk'])
            send_otp(card.mobile, f'Dear {card.holder_name}, Your Ration card rejected.....Enjoyyyyy::))))')
            card.delete()
        except:
            raise BadRequest('Card not found')
        return success_response('deleted')


class MemberListCreate(ListCreateAPIView, MultiPermissionView):
    """View for list and create member"""
    permissions = permissions = {
        'GET': (IsAuthenticated,),
        'POST': (IsAuthenticated, IsCard)
    }
    serializer_class = MemberSerializer

    def get_queryset(self):
        """Override queryset"""
        user = self.kwargs['user']
        try:
            if user.type == UserType.CARD:
                queryset = Member.objects.filter(card=user)
            else:
                queryset = Member.objects.filter(
                    card__id=decode(self.request.GET.get('card')))
            return queryset
        except:
            raise BadRequest('INVALID DATA')


class ShopListView(ListAPIView):
    """Serializer for lis and create User(s)"""
    permission_classes = (IsAuthenticated, )
    serializer_class = ShopLiteSerializer
    queryset = RationShop.objects.all()
    filterset_class = ShopFilter


class AdminDashboardView(APIView):
    permission_classes = (IsAuthenticated, IsAdmin)

    def get(self, request, *args, **kwargs):
        """Override get"""
        data = {
            "total_card": Card.objects.all().count(),
            "verified_cards": Card.objects.filter(verified=True).count(),
            "non_verified_cards": Card.objects.filter(verified=False).count(),
            "total_shops": RationShop.objects.all().count(),
            "verified_shops": RationShop.objects.filter(verified=True).count(),
            "non_verified_shops": RationShop.objects.filter(verified=False).count(),

        }
        return success_response(data)


class ShopDashboardView(APIView):
    permission_classes = (IsAuthenticated, IsShop)

    def get(self, request, *args, **kwargs):
        """Override get"""
        data = {
            "total_tokens": Token.objects.all().count(),
            "remaining_tokens": Token.objects.filter(
                status=TokenStatus.INITIATED, shop=self.kwargs['shop']).count(),
            "completed_tokens": Token.objects.filter(
                status=TokenStatus.COMPLETED, shop=self.kwargs['shop']).count(),
            "canceled_tokens": Token.objects.filter(
                status=TokenStatus.CANCELED, shop=self.kwargs['shop']).count(),
        }
        return success_response(data)