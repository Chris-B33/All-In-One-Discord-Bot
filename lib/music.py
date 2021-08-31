import discord
from discord.ext import commands
from youtube_dl import YoutubeDL


class Music(commands.Cog):

    def __init__(self, b):
        self.bot = b

        self.is_playing = False

        self.music_queue = []
        self.YDL_OPTIONS = {"format": "bestaudio", "noplaylist": "true"}
        self.FFMPEG_OPTIONS = {"before_options": "-reconnect 1 -reconnect_delay_max 5", "options": "-vn"}

        self.vc = ""

    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
            except Exception:
                return False

        return {'source': info['formats'][0]['url'], 'title': info['title']}

    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            # get the first url
            m_url = self.music_queue[0][0]['source']

            # remove the first element as you are currently playing it
            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    async def play_music(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]['source']

            # try to connect to voice channel if you are not already connected

            if self.vc == "" or not self.vc.is_connected() or not self.vc:
                self.vc = await self.music_queue[0][1].connect()
            else:
                await self.vc.move_to(self.music_queue[0][1])

            print(self.music_queue)
            # remove the first element as you are currently playing it
            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    @commands.command(
        name="play",
        help="Joins author's channel and searches for and plays song from given arguments"
    )
    async def play_song(self, ctx, *args):
        query = " ".join(args)

        voice_channel = ctx.author.voice.channel
        if voice_channel is None:
            # you need to be connected so that the bot knows where to go
            await ctx.send("Connect to a voice channel!")
        else:
            song = self.search_yt(query)
            if type(song) == type(True):
                await ctx.send(
                    "Could not download the song. Incorrect format try another keyword. This could be due to playlist or a livestream format.")
            else:
                await ctx.send("Song added to the queue")
                self.music_queue.append([song, voice_channel])

                if not self.is_playing:
                    await self.play_music()

    @commands.command(
        name="playskip",
        help="Skips current song and plays new song"
    )
    async def playskip(self, ctx, *args):
        query = " ".join(args)
        song = self.search_yt(query)

        if self.music_queue:
            self.music_queue.insert(1, song)
            await self.skip_song(ctx)
        else:
            self.music_queue.append(song)
            await self.play_music()

    @commands.command(
        name="queue",
        help="Displays the current songs in queue"
    )
    async def queue(self, ctx):
        retval = ""
        for i in range(0, len(self.music_queue)):
            retval += self.music_queue[i][0]['title'] + "\n"

        if retval != "":
            await ctx.send(retval)
        else:
            await ctx.send("No music in queue")

    @commands.command(
        name="skip",
        help="Skips the current song being played"
    )
    async def skip_song(self, ctx):
        if self.vc != "" and self.vc:
            self.vc.stop()
            await self.play_music()

    @commands.command(
        name="join",
        help="Joins the author's voice channel"
    )
    async def join_channel(self, ctx):
        channel = ctx.author.voice.channel
        if not ctx.voice_client:
            return await channel.connect()

    @commands.command(
        name="leave",
        help="Leaves current connected voice channel"
    )
    async def leave_channel(self, ctx):
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
        else:
            await ctx.send("I'm not connected to anything?")