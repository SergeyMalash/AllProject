import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from anonymous.models import AnonUser, AnonDialog, AnonMessages


class AnonymousChatConsumer(AsyncWebsocketConsumer):

    def __init__(self):
        super().__init__()
        self.message = None
        self.group_name = None
        self.my_user = None
        self.other_user = None
        self.dialog = None

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        if self.my_user:
            await self.remove_user_from_search(self.channel_name)
            if self.group_name:
                await self.channel_layer.group_discard(
                    self.group_name,
                    self.channel_name
                )
                await self.close_dialog()

    async def receive(self, text_data, **kwargs):
        message = json.loads(text_data)
        if message['type'] == 'start_search':
            await self.search_start(json.loads(message['content']))
        elif message['type'] == 'cancel_search':
            await self.remove_user_from_search(self.channel_name)
        elif message['type'] == 'message_to_dialog':
            await self.receive_message_from_dialog(message['content']['message'])
        elif message['type'] == 'close_dialog':
            await self.close_dialog()
        else:
            print('pass')

    async def search_start(self, search_params):
        user = await self.create_user(self.channel_name, search_params['my_age'], search_params['my_gender'])
        find_user = await self.find_user(user, search_params['other_age'], search_params['other_gender'])
        if find_user:
            dialog_id = await self.create_dialog(user, find_user)
            await self.channel_layer.group_add(
                dialog_id,
                self.channel_name
            )
            await self.channel_layer.group_add(
                dialog_id,
                find_user.channel_name
            )

            await self.channel_layer.group_send(
                dialog_id,
                {
                    'type': 'search_complete',
                    'content': dialog_id,
                }
            )

    async def close_dialog(self):
        await self.close_dialog_in_db(self.group_name)

        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'close_dialog_message',
                'content': 'close_dialog'
            }
        )

    async def close_dialog_message(self, event):
        self.group_name = None
        self.other_user = None

        await self.send(text_data=json.dumps({
            'type': 'close_dialog',
        }))

    async def search_complete(self, event):
        self.group_name = event['content']

        await self.send(text_data=json.dumps({
            'type': 'search_complete',
            'group_name': self.group_name,
            'my_channel': self.channel_name,
        }))

    async def receive_message_from_dialog(self, message_text):
        # await self.check_existing_dialog()

        self.message = await self.save_message(message_text)

        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'new_message',
                'content': message_text,
            }
        )

    async def check_existing_dialog(self):
        if AnonDialog.objects.filter():
            pass

    async def new_message(self, event):
        message = event['content']
        print(self.message)
        await self.send(text_data=json.dumps({
            'type': 'new_message',
            'message': message,
            'owner': 'true' if self.message else 'false'
        }))
        self.message = None

    @database_sync_to_async
    def close_dialog_in_db(self, dialog_id):
        dialog = AnonDialog.objects.get(id=str(dialog_id))
        dialog.is_closed = True
        dialog.save()

    @database_sync_to_async
    def remove_user_from_search(self, channel_name):
        try:
            anon_user = AnonUser.objects.get(channel_name=channel_name)
            anon_user.is_available = False
            anon_user.save()
        except AnonUser.DoesNotExist:
            pass

    @database_sync_to_async
    def create_user(self, channel_name, age, gender):
        my_user, created = AnonUser.objects.get_or_create(age=age, gender=gender, channel_name=channel_name)
        my_user.is_available = True
        my_user.save(update_fields=['is_available'])
        self.my_user = my_user
        return my_user

    @database_sync_to_async
    def save_message(self, message_text):

        def get_dialog(self, group_id):
            self.dialog = AnonDialog.objects.get(id=int(group_id))
            return self.dialog

        message = AnonMessages.objects.create(
            text=message_text,
            dialog=self.dialog if self.dialog else get_dialog(self, self.group_name),
            user=self.my_user
        )
        print(message)
        self.dialog.messages.add(message)
        return message

    @database_sync_to_async
    def find_user(self, user, age, gender):
        find_user = AnonUser.objects. \
            filter(age=age, gender=gender, is_available=True). \
            exclude(channel_name=user.channel_name).first()
        if find_user:
            find_user.is_available = False
            find_user.save(update_fields=['is_available'])
            user.is_available = False
            user.save(update_fields=['is_available'])
            self.other_user = find_user
        return find_user

    @database_sync_to_async
    def create_dialog(self, user1, user2):
        dialog = AnonDialog.objects.create()
        dialog.users.add(user1, user2)
        return str(dialog.id)

# from datetime import datetime
# from channels.generic.http import AsyncHttpConsumer
#
#
# class ServerSentEventsConsumer(AsyncHttpConsumer):
#     async def handle(self, body):
#         await self.send_headers(headers=[
#             (b"Cache-Control", b"no-cache"),
#             (b"Content-Type", b"text/event-stream"),
#             (b"Transfer-Encoding", b"chunked"),
#             (b'Access-Control-Allow-Origin', b'*')
#         ])
#         while True:
#             payload = "data: %s\n\n" % datetime.now().isoformat()
#             await self.send_body(payload.encode("utf-8"), more_body=True)
#             await asyncio.sleep(1)
