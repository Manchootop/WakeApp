from django.urls import path
from django.contrib.auth.views import LogoutView
from wakeapp_2.auth_app.views import RegisterView, LoginView

urlpatterns = [
    # path('edit/<int:id>/, EditProfileView.as_view', name='edit profile'),
    path('register/', RegisterView.as_view(), name='register user'),
    path('login/', LoginView.as_view(), name='login user'),
    path('logout/', LogoutView.as_view(), name='logout user')
]
