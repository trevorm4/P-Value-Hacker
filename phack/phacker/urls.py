from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('failed', views.failed, name='failed'),
    path('success', views.success, name='success')
]