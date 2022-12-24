from django.conf.urls import url

from chat.consumers import Consumer


websocket_urlpatterns = [
    url(r"^ws/$", Consumer.as_asgi()),
]
