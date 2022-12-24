import asyncio
import logging
from typing import Tuple
from channels.generic.websocket import AsyncJsonWebsocketConsumer


from chat.ws import SketchyWebSocket, WebSocketDisconnected
from chat import messages


class Consumer(AsyncJsonWebsocketConsumer):
    waiting_queue = asyncio.Queue()

    async def connect(self):
        ws = SketchyWebSocket(self)

        try:
            await ws.accept()
        except WebSocketDisconnected:
            return

        async def runner():
            try:
                read_task, write_task = await self.new_match(ws)
            except WebSocketDisconnected:
                return

            while not read_task.done():
                await write_task

                read_task.cancel()

                try:
                    read_task, write_task = await self.new_match(ws)
                except WebSocketDisconnected:
                    return

        asyncio.create_task(runner())
    
    async def new_match(
        self, ws: SketchyWebSocket
    ) -> Tuple[asyncio.Task, asyncio.Task]:
        in_feed = asyncio.Queue()
        try:
            out_feed = await self.find_match(ws, in_feed)
        except WebSocketDisconnected as e:
            raise e

        read_task = asyncio.create_task(self.read_socket(ws, out_feed))
        write_task = asyncio.create_task(self.run_conversation(ws, in_feed))

        return read_task, write_task

    async def find_match(
        self, ws: SketchyWebSocket, mq: asyncio.Queue
    ) -> asyncio.Queue:
        if self.waiting_queue.empty():
            await self.waiting_queue.put(mq)

            while ws.ready and not self.waiting_queue.empty():
                await asyncio.sleep(0)

            if not ws.ready:
                await self.waiting_queue.get()
                raise WebSocketDisconnected

            await mq.put(messages.ConnectedMessage())
            return await mq.get()

        inter_feed = await self.waiting_queue.get()
        await inter_feed.put(mq)

        await mq.put(messages.connected)
        return inter_feed

    @staticmethod
    async def read_socket(ws: SketchyWebSocket, out: asyncio.Queue):
        while True:
            try:
                message = await ws.receive_text()

            except WebSocketDisconnected:
                await out.put(messages.disconnect)
                break

            await out.put(messages.Text(message))

    @staticmethod
    async def run_conversation(ws: SketchyWebSocket, inp: asyncio.Queue):
        while True:
            while inp.empty():
                await asyncio.sleep(0)

            msg = await inp.get()
            try:
                await ws.send_text(str(msg))
            except WebSocketDisconnected:
                pass

            if isinstance(msg, messages.Disconnect):
                break