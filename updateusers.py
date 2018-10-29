from telethon import TelegramClient, events, sync
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
from time import sleep
import os

#736474925:AAEKWsWHYz3QmHN6AZPTSc2b6UoREY26ZTI
#736474925:AAEKWsWHYz3QmHN6AZPTSc2b6UoREY26ZTI

# These example values won't work. You must get your own api_id and
# api_hash from https://my.telegram.org, under API Development.
api_id = 503337
api_hash = 'b8f30e5aa88d3ed046bdf2ab128f988c'
groupname = 'https://t.me/joinchat/G7DhT0jQUZPViOXZWDUMAw'
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
	if(os.path.isfile("/home/roswell/telegramusers.txt")):
		os.remove("/home/roswell/telegramusers.txt")

	with open("/home/roswell/telegramusers.txt", "w+") as f:
		for user in all_participants:
			writeString = user.username + "\n"
			f.write(writeString)
	f.close()
	client.disconnect()
