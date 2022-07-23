from django.urls import path
from accounts.views import AdminCreateView, ShopCreateView, CardCreateView, \
    LoginView, CreateOtp, LoginOTPView

urlpatterns = [
    path(r'signup/admin/', AdminCreateView .as_view()),
    path(r'signup/shop/', ShopCreateView .as_view()),
    path(r'signup/card/', CardCreateView .as_view()),
    path(r'login/', LoginView .as_view()),
    path(r'login/create/otp/', CreateOtp .as_view()),
    path(r'login/otp/', LoginOTPView .as_view())
]
    # path(r'login/', LoginView .as_view()),
    # path(r'logout/', LogoutView .as_view()),
    # path(r'contact/', ContactListCreateView .as_view()),
    # path(r'contact/list/', ContactListView.as_view()),
    # path(r'dashboard/', DashboardView .as_view()),
    # path(r'user-details/<idencode:pk>', UserGetView .as_view())