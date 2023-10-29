import discord
import wavelink
from discord.ext import commands

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.current_track = None
        self.queue = []
        self.vc = None
        self.music_channel = None

    @commands.Cog.listener()
    async def on_wavelink_track_start(self, payload: wavelink.TrackEventPayload):
        self.current_track = payload.track

        trackEmbed = discord.Embed(
            title="Now Playing",
            color=0xb50000,
            description=f"**Track Title:** {payload.track.title}\n**Singer:** {payload.track.author}"
        )

        await self.music_channel.send(embed=trackEmbed, delete_after=5)


    @commands.Cog.listener()
    async def on_wavelink_track_end(self, payload: wavelink.TrackEventPayload):
        await self.play_next()

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if member == self.bot.user:
            if before.channel and not after.channel:
                embedDisconnected = discord.Embed(
                    description="I've been disconnected, hope to serve you again soon!",
                    color=0xb50000
                )
                
                await self.music_channel.send(embed=embedDisconnected)

                self.music_channel = None
                for queue in self.queue:
                    self.queue.pop(0)

    async def play_next(self):
        if self.queue:
            track = self.queue.pop(0)
            await self.vc.play(track)
        else:
            embedNoTracks = discord.Embed(
                description="There's no more tracks on the queue.\nAdd more to start playing again!",
                color=0xb50000
            )

            await self.music_channel.send(embed=embedNoTracks)

    @commands.command()
    async def join(self, ctx):
        if self.music_channel is None:
            self.music_channel = ctx.channel
        else:
            pass

        channel = ctx.author.voice.channel
        if channel:
            self.vc = await channel.connect(cls=wavelink.Player)
            await ctx.send(f"Joined {channel.mention}")
        else:
            await ctx.send("You are not in a voice channel.")

    @commands.command()
    async def leave(self, ctx):
        # Check if the bot is in a voice channel
        if ctx.voice_client is not None:
            # Disconnect from the current voice channel
            await ctx.voice_client.disconnect()

            if self.vc and self.vc.is_connected():
                await self.vc.stop()
                await self.vc.disconnect()
                self.music_channel = None
                await ctx.send("That's sad! Hoping to serve you again!")
        else:
            pass

    @commands.command()
    async def add(self, ctx, *title):
        await ctx.message.delete()
        if self.music_channel is None:
            self.music_channel = ctx.channel
        elif ctx.channel != self.music_channel:
            await ctx.send("This is not the music channel.")
            return

        query = " ".join(title)
        tracks = await wavelink.YouTubeMusicTrack.search(query)

        if not tracks:
            await ctx.send(f"I searched for {query}, but I found nothing.")
        else:
            track = tracks[0]
            self.queue.append(track)
            embedTrack = discord.Embed(
                title="Added To Queue",
                description=f"Track Title: {track.title}\nSinger: {track.author}",
                color=0xb50000
            )
            embedTrack.set_thumbnail(url=track.thumbnail)
            await ctx.send(embed=embedTrack, delete_after=5)

            if not self.vc.is_playing():
                await self.play_next(track)

    @commands.command()
    async def play(self, ctx, *query):
        await ctx.message.delete()
        tracks = await wavelink.YouTubeMusicTrack.search(" ".join(query))
        if ctx.author.voice.channel:
            if self.music_channel is None:
                self.music_channel = ctx.channel

            channel = ctx.author.voice.channel
            if self.vc is None or not self.vc.is_connected():
                self.vc = await channel.connect(cls=wavelink.Player)
                await ctx.send(f"Joined {channel.mention}")
            
            # Check if there's a currently playing track
            if not self.vc.is_playing():
                if not tracks:
                    await self.music_channel.send(f"I searched for {' '.join(query)}, but I found nothing.")
                else:
                    track = tracks[0]
                    self.current_track = track
                    await self.vc.play(self.current_track)
            else:
                if not tracks:
                    await self.music_channel.send(f"I searched for {' '.join(query)}, but I found nothing.")
                else:
                    track = tracks[0]
                    self.queue.append(track)
                    embedTrack = discord.Embed(
                        title="Added To Queue",
                        description=f"Track Title: {track.title}\nSinger: {track.author}",
                        color=0xb50000
                    )
                    embedTrack.set_thumbnail(url=track.thumbnail)
                    await ctx.send(embed=embedTrack, delete_after=5)
        else:
            await ctx.send("You are not in a voice channel.")

    @commands.command()
    async def queue(self, ctx):
        queue_list = []
        if self.current_track:
            queue_list.append(f"**Currently Playing: {self.current_track.title} - {self.current_track.author}**")

        if self.queue:
            queue_list.extend([f"{index + 1}. {track.title} - {track.author}" for index, track in enumerate(self.queue)])

        if not queue_list:
            await ctx.send("The queue is currently empty.")
        else:
            embedQueue = discord.Embed(
                description="\n".join(queue_list),
                color=0xb50000
            )

            embedQueue.set_author(name="Queue Manager")

            await ctx.send(embed=embedQueue)

    @commands.command()
    async def skip(self, ctx):
        if self.music_channel is None:
            self.music_channel == ctx.channel
        elif ctx.channel == self.music_channel:
            if not self.vc.is_playing():
                await ctx.send("Currently not playing any tracks")
            elif not self.queue:
                await ctx.send("Queue is empty. Add more songs!")
            else:
                track = self.queue.pop(0)
                await self.vc.play(track)
        else:
            await ctx.send("This is not the music channel.")

    @commands.command()
    async def stop(self, ctx):
        if self.music_channel is None:
            self.music_channel == ctx.channel
        elif ctx.channel == self.music_channel:
            if self.vc and self.vc.is_playing():
                await self.vc.stop()
            else:
                await ctx.send("Not playing anything.")
        else:
            await ctx.send("This is not the music channel.")

async def setup(bot):
    await bot.add_cog(Music(bot))