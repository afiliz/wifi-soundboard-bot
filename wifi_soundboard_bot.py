import discord
import os

'''
Wi-Fi Tree Discord Bot

This bot is designed for users of the Discord server "The Wi-Fi Tree". The bot's function is to play short sound clips on command when in a voice channel. The bot will join the caller's voice channel, play the selected clip, and leave the voice channel.

Commands:
- play [selection]: Bot joins the caller's voice channel and plays a clip selection. "selection" can either be a specific clip name, or an option such as "random" to play a random clip.
- stop: Bot stops playing any sound clip currently being played.
- upload-clip [file attachment]: Uploads clip to the drive where the bot's sound clip repository is
- help: Displays info on bot functionality and commands

Optional/Future Commands:
- Pause: Bot pauses current sound clip. If play is used after pause, previous clip's progress will be overwritten
- Resume: Bot resumes current sound clip. If play is used after pause, previous clip's progress will be overwritten
'''

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

@client.event()
async def connect(ctx, timeout=30.0, reconnect=False):
    channel = ctx.author.voice.channel
    await channel.connect()

@client.event()
async def leave(ctx):
    await ctx.voice_client.disconnect()

client.run(os.getenv('TOKEN'))
