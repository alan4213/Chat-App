import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message, User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if not self.scope['user'].is_authenticated:
            await self.close()
            return
        
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_content = data.get('message', '').strip()
        receiver_id = data.get('receiver_id')
        message_type = data.get('type', 'message')

        if message_type == 'typing':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'typing_indicator',
                    'sender_id': self.scope['user'].id
                }
            )
        elif message_type == 'delete':
            message_id = data.get('message_id')
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'delete_message',
                    'message_id': message_id
                }
            )
        elif message_type == 'mark_read':
            await self.mark_messages_read(receiver_id)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'read_status',
                    'sender_id': self.scope['user'].id
                }
            )
        elif message_content and receiver_id:
            message = await self.save_message(self.scope['user'].id, receiver_id, message_content)
            
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message_content,
                    'sender_id': self.scope['user'].id,
                    'sender_username': self.scope['user'].username,
                    'message_id': message.id,
                    'is_read': message.is_read
                }
            )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'message',
            'message': event['message'],
            'sender_id': event['sender_id'],
            'sender_username': event['sender_username'],
            'message_id': event['message_id'],
            'is_read': event['is_read']
        }))

    async def read_status(self, event):
        await self.send(text_data=json.dumps({
            'type': 'read_status',
            'sender_id': event['sender_id']
        }))

    async def typing_indicator(self, event):
        await self.send(text_data=json.dumps({
            'type': 'typing',
            'sender_id': event['sender_id']
        }))

    async def delete_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'delete',
            'message_id': event['message_id']
        }))

    @database_sync_to_async
    def save_message(self, sender_id, receiver_id, content):
        sender = User.objects.get(id=sender_id)
        receiver = User.objects.get(id=receiver_id)
        return Message.objects.create(sender=sender, receiver=receiver, content=content)

    @database_sync_to_async
    def mark_messages_read(self, sender_id):
        Message.objects.filter(
            sender_id=sender_id,
            receiver_id=self.scope['user'].id,
            is_read=False
        ).update(is_read=True)
