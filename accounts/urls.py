from django.urls import path
from accounts.views import AdminCreateView, ShopCreateView, CardCreateView, \
    LoginView, CreateOtp, LoginOTPView, VerifyCardView, VerifyShopView, MemberListCreate

urlpatterns = [
    path(r'signup/admin/', AdminCreateView .as_view()),
    path(r'signup/shop/', ShopCreateView .as_view()),
    path(r'get/shop/<idencode:pk>/', ShopCreateView .as_view()),
    path(r'signup/card/', CardCreateView .as_view()),
    path(r'get/card/<idencode:pk>/', CardCreateView.as_view()),
    path(r'login/', LoginView .as_view()),
    path(r'login/create/otp/', CreateOtp .as_view()),
    path(r'login/otp/', LoginOTPView .as_view()),
    path(r'verify/card/<idencode:pk>/', VerifyCardView .as_view()),
    path(r'verify/shop/<idencode:pk>/', VerifyShopView .as_view()),
    path(r'member/', MemberListCreate.as_view()),

]