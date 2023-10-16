from django.urls import path
from . import views

urlpatterns = [
    path('admin/', views.admin, name='admin'),
    path('complaint/<int:pk>', views.complaint, name='complaint'),
]
