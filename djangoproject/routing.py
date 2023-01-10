import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from django.urls import path
from chat.consumers import *


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
application=get_asgi_application()


application = ProtocolTypeRouter({
    "http": get_asgi_application(),

    # WebSocket chat handler
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter([
               path('ws/chat/<int:roomid>/<int:senderid>/',ChatConsumer.as_asgi()),
            ])
        )
    ),
})