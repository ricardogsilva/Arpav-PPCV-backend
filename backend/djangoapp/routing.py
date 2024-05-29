from django.conf.urls import url

from channels.routing import ProtocolTypeRouter, URLRouter, ChannelNameRouter
from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack
#from channels.auth import AuthMiddlewareStack
from djangoapp.consumers import AppConsumer

application = ProtocolTypeRouter({

    # WebSocket chat handler
    # "websocket": AllowedHostsOriginValidator(
    #     AuthMiddlewareStack(
    #     URLRouter([
    #         url("^chat/admin/$", AdminChatConsumer),
    #         url("^chat/$", PublicChatConsumer),
    #     ])
    #     ),
    # ),

    # WebSocket
    # "websocket": AllowedHostsOriginValidator(
    #     AuthMiddlewareStack(
    #         URLRouter([
    #
    #         ])
    #     ),
    # ),

    "channel": ChannelNameRouter({
        "app": AppConsumer,
    }),
})
