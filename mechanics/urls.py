from django.urls import path

from .auth_views import register_user
from .views import MechanicDetailView, MechanicListCreateView, ServiceRequestListCreateView

urlpatterns = [
    path('register/', register_user, name='register-user'),
    path('mechanics/', MechanicListCreateView.as_view(), name='mechanic-list'),
    path('mechanics/<int:pk>/', MechanicDetailView.as_view(), name='mechanic-detail'),
    path('service-requests/', ServiceRequestListCreateView.as_view(), name='service-request-list'),
]
