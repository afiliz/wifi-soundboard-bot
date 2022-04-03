import os
import discord
import nacl
import requests

from replit import db
from discord import FFmpegPCMAudio
from discord.ext import commands
from stayin_alive import keep_alive

'''
Wi-Fi Tree Discord Bot

This bot is designed for users of the Discord server "The Wi-Fi Tree". The bot's function is to play short sound clips on command when in a voice channel. The bot will join the caller's voice channel, play the selected clip, and leave the voice channel.
'''

bot = commands.Bot(command_prefix='!')
secret_token = os.environ['TOKEN']

'''
Helper Functions
'''
# Given user input, gets clip file
def get_song_clip(user_input):
  file_name = ""

  if len(user_input) == 1:
    return user_input[0].replace(' ','_').lower() + '.mp3'

  for i, word in enumerate(user_input):
    if i == len(user_input) - 1:
      file_name += word.replace('"','').lower()
      file_name += '.mp3'
      break
    else:
      file_name += word.replace('"','').lower()
      file_name += '_'

  return file_name

'''
Bot Commands/Functions
'''

# Notifies console that bot is ready to take commands after login
@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

# !join: have bot join the user's voice channel as a voice client
@bot.command()
async def join(ctx, timeout=30.0, reconnect=False):
  if not ctx.message.author.voice:
    await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
    return
  else:
    channel = ctx.message.author.voice.channel
  await channel.connect()

# !leave: have bot leave user's voice channel
@bot.command()
async def leave(ctx):
  voice_client = ctx.message.guild.voice_client
  if voice_client.is_connected():
    await voice_client.disconnect()
  else:
    await ctx.send("The bot is not connected to a voice channel.")

# !play: have bot play specified clip
# Format: !play [clip name]
# Clip name can be upper/lower case and can use spaces
@bot.command(name='play', help='Plays the specified clip')
async def play(ctx, *clip_name):
  voice_client = ctx.message.guild.voice_client
  source_name = get_song_clip(clip_name)
  file_path = ''

  # look through each category folder for clip's file path
  dir_path = os.path.dirname(os.path.realpath(__file__))
  for root, dirs, files in os.walk(dir_path):
    for file in files:
        if str(file) == source_name:
          file_path = root + '/' + source_name
  
  audio_source = FFmpegPCMAudio(file_path)
  if audio_source is None:
    await ctx.send("Clip name specified is invalid.")

  # make sure bot can play (has to be in voice channel and not playing already)
  if voice_client.is_connected() and not voice_client.is_playing():
    voice_client.play(audio_source, after=None)
  else:
    if not voice_client.is_connected():
      await join(ctx)
    elif voice_client.is_playing():
      await ctx.send("Bot is already playing a sound clip. Wait your turn!")

# !upload-clip: have bot upload sound clip attached to message to clip directory
@bot.command(name='upload', help='Uploads the attached sound clip to the clip directory')
async def upload(ctx, *clip_cat):
  clip_url = ctx.message.attachments[0].url
  
  print("URL: " + str(clip_url))
  if clip_url[-3:] != 'mp3':
    await ctx.send("The attachment was not a mp3 file. Please upload a valid sound clip.")
  
  if clip_url[0:26] == 'https://cdn.discordapp.com':
    clip_file_name = clip_url.split('/')[-1:][0]
    # clip_name = clip_file_name[:len(clip_file_name) - 4]
    
    clip = requests.get(clip_url)
    path ='sound_clips'
    if clip_cat != None:
      path += ('/' + str(clip_cat[0]))
    
    if not os.path.exists(path):
      os.makedirs(path)

    print(str(path + '/' + clip_file_name))

    with open(path + '/' + clip_file_name, 'wb') as output_clip:
      output_clip.write(clip.content)

# keep_alive() # run flask server to keep bot alive
bot.run(secret_token)
