import asyncio
from types import MethodType


class WebSocketDisconnected(Exception):
    pass


class SketchyWebSocket:
    def __init__(self, consumer):
        self.ready = True
        self.in_messages_buffer = asyncio.Queue()
        self.consumer = self._patch_consumer(consumer)

    def _patch_consumer(self, consumer):
        async def interceptor(_, text_data):
            await self._put_in_messages_buffer(text_data)

        async def disconnector(_, close_code):
            self.ready = False
            await self._put_in_messages_buffer(WebSocketDisconnected)

        consumer.receive = MethodType(interceptor, consumer)
        consumer.disconnect = MethodType(disconnector, consumer)

        return consumer

    async def _put_in_messages_buffer(self, text):
        await self.in_messages_buffer.put(text)

    async def receive_text(self):
        if not self.ready:
            raise WebSocketDisconnected
        msg = await self.in_messages_buffer.get()

        if msg == WebSocketDisconnected:
            raise WebSocketDisconnected

        return msg

    async def send_text(self, text):
        if not self.ready:
            raise WebSocketDisconnected
        await self.consumer.send(text_data=text)

    async def accept(self):
        if not self.ready:
            raise WebSocketDisconnected
        await self.consumer.accept()