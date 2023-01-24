from django.urls import path, reverse_lazy
from django.contrib.auth.views import LogoutView
from django.views.generic import RedirectView

from wakeapp_2.auth_app.views import RegisterView, LoginView, ChangeUserPasswordView

urlpatterns = [
    # path('edit/<int:id>/, EditProfileView.as_view', name='edit profile'),
    path('register/', RegisterView.as_view(), name='register user'),
    path('login/', LoginView.as_view(), name='login user'),
    path('logout/', LogoutView.as_view(), name='logout user'),
    path('edit-password/', ChangeUserPasswordView.as_view(), name='change password'),
    path('password_change_done/', RedirectView.as_view(url=reverse_lazy('dashboard')), name='password_change_done'),

]
