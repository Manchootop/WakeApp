from django.contrib.auth import get_user_model, authenticate
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic as generic_views
from rest_framework import generics as api_generic_views, permissions
from rest_framework.authtoken import views as api_views
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from django.contrib.auth import views as auth_views, logout

from django.views import generic as views
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from wakeapp_2.auth_app import serializers as auth_serializers
from wakeapp_2.auth_app.forms import UserRegisterForm
from wakeapp_2.auth_app.serializers import LoginSerializer

UserModel = get_user_model()


# class RegisterView(api_generic_views.CreateAPIView):
#     queryset = UserModel.objects.all()
#     serializer_class = auth_serializers.CreateUserSerializer
#     permission_classes = (
#         permissions.AllowAny,
#     )
#
#
# class LoginView(ObtainAuthToken):
#
#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data,
#                                            context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         token, created = Token.objects.get_or_create(user=user)
#         return Response({
#             'token': token.key,
#             'user_id': user.pk,
#             'email': user.email
#         })
#
# class LogoutView(api_views.APIView):
#     @staticmethod
#     def __perform_logout(request):
#         token = Token.objects.get(user=request.user)
#         token.delete()
#         return Response({
#             'message': 'User logged out',
#         })
#
#     def get(self, request):
#         return self.__perform_logout(request)
#
#     def post(self, request):
#         return self.__perform_logout(request)

class LoginView(auth_views.LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')


class RegisterView(views.CreateView, SuccessMessageMixin):
    template_name = 'register.html'
    success_url = reverse_lazy('login')
    form_class = UserRegisterForm
    success_message = "Your profile was created successfully"
