import discord
import time
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
    author = message.author
    format_flag = True

    if message.content[:2] == 'h!':
        command_text = message.content[2:].lower()
        if command_text[:5] == 'start':
            if db.search(Query().user == author.id) == []:
                timestamp = time.time()
                command_list = command_text.split(' ')[1:]

                if command_list[0] != 'd' and command_list[0] != 'h':
                    format_flag = False

                if not command_list[1].isdigit() or not command_list[2].isdigit():
                    format_flag = False

                if len(command_list) == 3 and format_flag:
                    if command_list[0] == 'd':
                        timestamp -= 86400 * int(command_list[2])
                    elif command_list[0] == 'h':
                        timestamp -= 3600 * int(command_list[2])
                    db.insert({'user': author.id, 'start': str(timestamp), 'type': command_list[0], 'goal': command_list[1]})
                else:
                    await client.send_message(message.channel, 'FORMAT: `h!start d/h goal completed`.\nd is for days and h is for hours\nEXAMPLE: `h!start d 3 1`')
            else:
                await client.send_message(message.channel, 'Already started. Please type h!stop first.')
        if command_text == 'stop':
            if db.search(Query().user == author.id) != []:
                db.remove(Query().user == author.id)
            else:
                await client.send_message(message.channel, 'Not started. Please type h!start first.')

if __name__ == '__main__':
    if '--run' in sys.argv:
        token = ''
        with open('token.key') as file:
            token = file.read()
        client.run(token)