import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from .mail_receiving import mail_receiving


class MessageConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

        total_emails = 10
        index = 0
        async for message in mail_receiving():
            index += 1
            await asyncio.sleep(1)

            progress_data = {
                'checkedPercentage': (index / total_emails) * 100,
                'messageFound': False
            }
            await self.send(text_data=json.dumps(progress_data))

            await asyncio.sleep(1)

            await self.send(text_data=json.dumps({
                'checkedPercentage': 100,
                'messageFound': True,
                'messages': [message]
            }))

        # Добавьте завершающее сообщение, если нужно
        await self.send(text_data=json.dumps({
            'checkedPercentage': 100,
            'messageFound': False,
            'messages': []
        }))

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        pass
