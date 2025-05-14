from django.urls import path
from . import consumers

ASGI_urlpatterns = [
    path('websocket/<int:user_id>/', consumers.ChatConsumer.as_asgi(), name='routing'),
]