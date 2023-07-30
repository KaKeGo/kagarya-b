import asyncio
import json

from channels.generic.websocket import AsyncWebsocketConsumer


class MyWebSocketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass
    
    async def receive(self, text_data):
        data = json.loads(text_data)
        if data.get('type') == 'user_auth_check':
            user = self.scope['user']
            if user.is_authenticated:
                await self.send_message({
                    'type': 'user_auth_check_response',
                    'is_authenticated': True,
                    'user': {
                        'username': user.username,
                        'email': user.email,
                    }
                })
            else:
                await self.send_message({
                    'type': 'user_auth_check_response',
                    'is_authenticated': False,
                })
    
    async def send_message(self, data):
        await self.send(text_data=json.dumps(data))