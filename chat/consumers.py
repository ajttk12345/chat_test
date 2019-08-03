#-*- coding: utf-8 -*-
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
import json
import sys

groups = {}

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        url_info = self.scope['url_route']['kwargs']
        self.room_group_name = url_info['room_name']
        #global user_name
        user_name = url_info['user_name']

        #['room_name']['user_name']
        #print('aa-=-=-==-===================a\n\n\n')

        print(self.room_group_name, user_name)
        
        global groups
        if self.room_group_name in groups:
            if groups[self.room_group_name] is 1:
                groups[self.room_group_name] = 2
            else:
                print('다참')
                sys.exit()
        else:
            groups[self.room_group_name] = 1

            #cnt = self.groups
            #print(cnt)

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )
        await self.accept()
        print(groups)

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        global groups
        groups[self.room_group_name] -= 1

        if groups[self.room_group_name] is 0:
            del groups[self.room_group_name]
            await self.close()
        
        print('out')
        print(groups)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        userName = text_data_json['userName']
        _type = text_data_json['type']
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'userName': userName,
                'type': _type,
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        userName = event['userName']
        _type = event['type']
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'userName': userName,
            'type': _type,
            'message': message
        }))