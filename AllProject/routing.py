from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from messenger.routing import websocket_urlpatterns as ws_messenger
from anonymous.routing import websocket_urlpatterns as ws_anonymous

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            ws_messenger + ws_anonymous
        )
    ),
})
