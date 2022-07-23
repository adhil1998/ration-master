from rest_framework.generics import ListAPIView, ListCreateAPIView, \
    CreateAPIView, RetrieveAPIView
from common.permissions import IsAuthenticated
from common.functions import success_response
from rest_framework.views import APIView
from accounts.serializers import *
# from accounts.filter import *
from accounts.models import Admin
from rest_framework.response import Response


class AdminCreateView(CreateAPIView, RetrieveAPIView):
    """Serializer for lis and create User(s)"""
    serializer_class = AdminSerializer
    queryset = Admin.objects.all()
