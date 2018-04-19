import discord
import asyncio
import sys

client = discord.Client()

@client.event
async def on_ready():
    print('TEST')
    print(client.user.name)

@client.event
async def on_message(message):
    print(message.content)


token = ''
with open('token.auth') as file:
    token = file.read()

client.run(token)