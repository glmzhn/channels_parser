from pyrogram import Client
import os
import random
from pyrogram import raw
import asyncio

filepath = os.path.abspath(__file__)
proxy_dir = filepath.replace("\\main.py", "\\proxy")
cur_dir = filepath.replace('\\main.py', '')
sessions_dir = os.path.join(os.path.dirname(filepath), 'sessions')

with open(f'{proxy_dir}/' + 'proxy.txt', 'r') as fl:
    proxy_list = fl.read().split('\n')

sessions = []

for files in os.listdir(sessions_dir):
    if files.endswith(".sessions"):
        files = files.split('.')
        sessions.append(files[0])

cur_proxy = random.choice(proxy_list)


with open(f'{cur_dir}/' + 'keywords.txt', 'r', encoding='utf-8') as fl:
    keywords = fl.read().split('\n')

with open(f'{cur_dir}/' + 'count_of_channels.txt', 'r', encoding='utf-8') as fl:
    times = fl.read()

app = Client(sessions[0], workdir=sessions_dir)


async def search():
    with open('result.txt', 'wt', encoding='utf-8') as file:
        for i in keywords:
            result = await app.invoke(raw.functions.contacts.Search(q=i, limit=int(times)))

            for chat in result.chats:
                if chat.username:
                    print(chat.username)
                    file.write(chat.username + '\n')
                else:
                    print(f"Channel {chat.title} hasn't got username")


if __name__ == "__main__":
    app.start()
    asyncio.get_event_loop().run_until_complete(search())
    app.stop()
