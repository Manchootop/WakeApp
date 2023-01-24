from django.urls import path

from wakeapp_2.main import views

urlpatterns = [
    path('events/', views.CreateEventView.as_view(), name='create_event'),
    path('events/<int:pk>/', views.EventDetailView.as_view(), name='event_detail'),
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('design/', views.DesignView.as_view(), name='demo design')
]
