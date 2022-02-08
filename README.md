# Wi-Fi Tree Discord Bot

This bot is designed for users of the Discord server "The Wi-Fi Tree". The bot's function is to play short sound clips on command when in a voice channel. The bot will join the caller's voice channel, play the selected clip, and leave the voice channel.

### Goals (Most to Least Important)
1. Be able to play an mp3 file from a set repository given a command in a Discord channel
2. Allow server members to upload their own mp3 files to a public online repository via Discord channel chat
3. Allow Discord server members in a voice channel to invoke Discord's "Slash" commands to invoke the soundboard bot with UI elements 

## Commands:
- play [selection]: Bot joins the caller's voice channel and plays a clip selection. "selection" can either be a specific clip name, or an option such as "random" to play a random clip.
- stop: Bot stops playing any sound clip currently being played.
- upload-clip [file attachment]: Uploads clip to the drive where the bot's sound clip repository is
- help: Displays info on bot functionality and commands

## Optional/Future Commands:
- Pause: Bot pauses current sound clip. If play is used after pause, previous clip's progress will be overwritten
- Resume: Bot resumes current sound clip. If play is used after pause, previous clip's progress will be overwritten