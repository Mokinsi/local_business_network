# business/routing.py
from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/chat/<int:business_owner_id>/', consumers.ChatConsumer.as_asgi()),
]