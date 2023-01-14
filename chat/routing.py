
from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/chat/', consumers.ChatConsumer.as_asgi()),
]

from django.core.asgi import get_asgi_application

application = get_asgi_application()
application.add_routes(websocket_urlpatterns)
