import discord
import asyncio
import sys

from tinydb import TinyDB, Query

client = discord.Client()
db = TinyDB('db.json')

@client.event
async def on_ready():
    print('TEST')
    print(client.user.name)

@client.event
async def on_message(message):
    if message.content[:2] == 'h!':
        command_text = message.content[2:].lower()
        if command_text == 'start':
            pass

if __name__ == '__main__':
    if '--run' in sys.argv:
        token = ''
        with open('token.auth') as file:
            token = file.read()
        client.run(token)