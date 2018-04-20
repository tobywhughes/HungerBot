import discord
import time
import asyncio
import sys
import threading

from tinydb import TinyDB, Query

client = discord.Client()
db = TinyDB('db.json')

last_time = time.time()

@client.event
async def on_ready():
    print('READY')

@client.event
async def on_message(message):
    global last_time
    if time.time() - last_time > 10:
        await nickname_check()
        last_time = time.time()
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
                    await set_nickname(timestamp, author, command_list[0], command_list[1])
                else:
                    await client.send_message(message.channel, 'FORMAT: `h!start d/h goal completed`.\nd is for days and h is for hours\nEXAMPLE: `h!start d 3 1`')
            else:
                await client.send_message(message.channel, 'Already started. Please type h!stop first.')
        if command_text == 'stop':
            if db.search(Query().user == author.id) != []:
                db.remove(Query().user == author.id)
                await client.change_nickname(author, None)
            else:
                await client.send_message(message.channel, 'Not started. Please type h!start first.')

async def set_nickname(timestamp, author, type, goal):
    name = author.name
    current_time = time.time()
    diff = 0
    append = ''
    if type == 'h':
        diff = (current_time - timestamp) // 3600
        append = ' Hours'
    elif type == 'd':
        diff = (current_time - timestamp) // 86400
        append = ' Days'

    nickname = name + ' ' + str(int(diff)) + '/' + str(goal) + append
    await client.change_nickname(author, nickname)

async def nickname_check():
    print(time.ctime())
    for entry in db.all():
        user = await client.get_user_info(entry['user'])
        print(user.name)

if __name__ == '__main__':
    if '--run' in sys.argv:
        token = ''
        with open('token.key') as file:
            token = file.read()
        client.run(token)
        