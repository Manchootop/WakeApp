from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic as generic_views
from rest_framework import generics as api_generic_views, permissions
from rest_framework.authtoken import views as api_views
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated

from wakeapp_2.auth_app import serializers as auth_serializers

UserModel = get_user_model()


class RegisterView(api_generic_views.CreateAPIView):
    queryset = UserModel.objects.all()
    serializer_class = auth_serializers.CreateUserSerializer
    permission_classes = (
        permissions.AllowAny,
    )


class LoginView(api_views.ObtainAuthToken):
    pass


class LogoutView(api_views.APIView):
    @staticmethod
    def __perform_logout(request):
        token = Token.objects.get(user=request.user)
        token.delete()
        return Response({
            'message': 'User logged out',
        })

    def get(self, request):
        return self.__perform_logout(request)

    def post(self, request):
        return self.__perform_logout(request)
