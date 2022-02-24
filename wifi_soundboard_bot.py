import discord
from discord import FFmpegPCMAudio
import nacl
from discord.ext import commands
from stayin_alive import keep_alive
import os

'''
Wi-Fi Tree Discord Bot

This bot is designed for users of the Discord server "The Wi-Fi Tree". The bot's function is to play short sound clips on command when in a voice channel. The bot will join the caller's voice channel, play the selected clip, and leave the voice channel.
'''

bot = commands.Bot(command_prefix='!')
secret_token = os.environ['TOKEN']

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.command()
async def join(ctx, timeout=30.0, reconnect=False):
  if not ctx.message.author.voice:
    await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
    return
  else:
    channel = ctx.message.author.voice.channel
  await channel.connect()

@bot.command()
async def leave(ctx):
  voice_client = ctx.message.guild.voice_client
  if voice_client.is_connected():
    await voice_client.disconnect()
  else:
    await ctx.send("The bot is not connected to a voice channel.")

@bot.command(name='play', help='Plays the specified clip')
async def play(ctx):
  # try:
  #   server = ctx.message.guild
  #   voice_channel = server.voice_client

  #   async with ctx.typing():
      
  # # await ctx.channel.send('Playing clip')
  voice_client = ctx.message.guild.voice_client

  audio_source = FFmpegPCMAudio('watch_your_profanity.mp3')
  if voice_client.is_connected() and not voice_client.is_playing():
    voice_client.play(audio_source, after=None)
  else:
    if not voice_client.is_connected():
      await ctx.send("Can't play audio, the bot is not connected to a voice channel.")
    elif voice_client.is_playing():
      await ctx.send("Bot is already playing a sound clip. Wait your turn!")
  


@bot.command()
async def ping(ctx):
  await ctx.channel.send("pong")

# keep_alive() # run flask server to keep bot alive
bot.run(secret_token)
