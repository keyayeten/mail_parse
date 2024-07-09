import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer


class MessageConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

        # Имитировать процесс проверки писем
        total_emails = 100
        for i in range(total_emails):
            await asyncio.sleep(0.1)
            progress_data = {
                'checkedPercentage': (i + 1) / total_emails * 100,
                'messageFound': False
            }
            await self.send(text_data=json.dumps(progress_data))

        # Если сообщение найдено, отправить его
        messages = [{
            'subject': 'Пример темы',
            'sender': 'example@example.com',
            'date': '2024-07-09',
            'shortDescription': 'Краткое описание сообщения'
        }]
        await self.send(text_data=json.dumps({
            'checkedPercentage': 100,
            'messageFound': True,
            'messages': messages
        }))

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        pass
