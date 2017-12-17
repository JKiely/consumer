from django.urls import path

from consumer.views import index

urlpatterns = [
    path('', index),
]