from telethon import TelegramClient, events, sync
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
from time import sleep
import os

api_id = 1337
api_hash = 'YOUR API HASH'
groupname = 'YOUR GROUP NAME'
client = TelegramClient('userlist_update', api_id, api_hash)
try:
	client.start()
	dialogs = client.get_dialogs()
	group = client.get_entity(groupname)
	offset = 0
	limit = 100
	all_participants = []

	while True:
		participants = client(GetParticipantsRequest(group, ChannelParticipantsSearch(''), offset, limit, hash=0))
		if not participants.users:
			break
		all_participants.extend(participants.users)
		offset += len(participants.users)
finally:
	if(os.path.isfile("/path/to/user/list")):
		os.remove("/path/to/user/list")

	with open("/path/to/user/list", "w+") as f:
		for user in all_participants:
			writeString = user.username + "\n"
			f.write(writeString)
	f.close()
	client.disconnect()
