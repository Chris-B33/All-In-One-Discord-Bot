# My Discord Bot
This bot was created with the intention to take many helpful functions from other Discord Bots and wrap them all into one Bot.

## Functions
### Server Creation
Add to a server before adding any channels and this bot can create
the whole server for you! Choose your desired size (1. Small, 2. Medium, 3. Big) and
the bot will create voice channels, text channels and roles for you! It will automatically assign
itself and any other added bots their own role as well as an admin role for you!

Try a!help server for more info.

### TTS and Music Playing
This bot will take a query and look for the closest song matching the query on Youtube then play
it back in your voice channel for you to hear!
This bot can also take what you say in a text channel and say it in a voice channel!

Try a!help music or a!help TTS for more info.

## Dependencies
### Discord.py with Voice Support
pip install -U discord.py[voice]

### YoutubeDL for finding songs
pip install youtube_dl

### pyttsx3 for TTS functions
pip install pyttsx3
