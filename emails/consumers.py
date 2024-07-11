import json
import logging
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from .mail_receiving import mail_receiving


class MessageConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.messages_gen = None  # Инициализация генератора сообщений как None

    async def receive(self, text_data):
        user_data = json.loads(text_data)
        email = user_data.get('email')
        email_password = user_data.get('email_password')

        # Инициализация генератора сообщений с данными пользователя
        if not self.messages_gen:
            self.messages_gen = mail_receiving(
                email,
                email_password
            )

        total_emails = 10
        index = 0

        while index < total_emails:
            await asyncio.sleep(1)
            progress_data = {
                'checkedPercentage': (index / total_emails) * 100,
                'messageFound': False
            }
            await self.send(text_data=json.dumps(progress_data))

            try:
                message = next(self.messages_gen)
                logging.info(message)
                await asyncio.sleep(1)
                await self.send(text_data=json.dumps({
                    'checkedPercentage': 100,
                    'messageFound': True,
                    'messages': [message]
                }))
            except StopIteration:
                break

            index += 1

    async def disconnect(self, close_code):
        pass


# Пример генератора для теста отображений
# def mail_receiving(email, password):
#     messages = [
#         {"subject": "Subject 1", "sender": "sender1@example.com",
#          "date": "2023-07-10", "shortDescription": "Description 1"},
#         {"subject": "Subject 2", "sender": "sender2@example.com",
#          "date": "2023-07-11", "shortDescription": "Description 2"},
#         {"subject": "Subject 3", "sender": "sender3@example.com",
#          "date": "2023-07-12", "shortDescription": "Description 3"}
#     ]
#     for message in messages:
#         yield message
