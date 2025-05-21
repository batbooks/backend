from django.urls import path
from . import consumers

ASGI_urlpatterns = [
    path('websocket/<int:user_id>/', consumers.ChatConsumer.as_asgi(), name='routing'),
    path('ws/group/<int:group_id>/', consumers.GroupChatConsumer.as_asgi(), name='group-chat'),

]
