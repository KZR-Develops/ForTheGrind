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
        trackEmbed = discord.Embed(
            title="Now Playing",
            color=0xb50000,
            description=f"Track Title: {payload.track.title}\nSinger: {payload.track.author}"
        )

        await self.music_channel.send(embed=trackEmbed)

    @commands.Cog.listener()
    async def on_wavelink_track_end(self, payload: wavelink.TrackEventPayload):
        await self.play_next()


    async def play_next(self):
        if self.queue:
            track = self.queue.pop(0)
            await self.vc.play(track)
        else:
            embedNoTracks = discord.Embed(
                description="No more tracks on queue. Add more to start playing again!",
                color=0xb50000
            )

            await self.music_channel.send(embed=embedNoTracks)
            # await ctx.send("Queue is empty. Add more songs!")

    @commands.command()
    async def join(self, ctx):
        if self.music_channel is None:
            self.music_channel = ctx.channel
        else:
            pass

        channel = ctx.author.voice.channel
        if channel:
            self.vc = await channel.connect(cls=wavelink.Player)
            await ctx.send(f"Joined {channel.name}")
        else:
            await ctx.send("You are not in a voice channel.")

    @commands.command()
    async def leave(self, ctx):
        await ctx.message.delete()
        if ctx.channel == self.music_channel:
            if self.vc:
                await self.vc.disconnect()
            else:
                await ctx.send("Not connected to a voice channel.")

    @commands.command()
    async def add(self, ctx, *title):
        await ctx.message.delete()
        if self.music_channel is None:
            self.music_channel == ctx.channel
        elif ctx.channel == self.music_channel:
            query = " ".join(title)
            tracks = await wavelink.YouTubeMusicTrack.search(query)
            if not tracks:
                await ctx.send(f"I searched for {query}, but I found nothing.")
            else:
                track = tracks[0]
                self.queue.append(track)
                embedTrack = discord.Embed(
                    title="Added To Queue",
                    description=f"Track Title: {track.title}\nSinger: {track.author}\nDuration: {track.duration}",
                    color=0xb50000
                )
                embedTrack.set_thumbnail(url=track.thumbnail)
                await ctx.send(embed=embedTrack, delete_after=5)
                if not self.vc.is_playing():
                    await self.play_next(track)
        else:
            await ctx.send("This is not the music channel.")

    @commands.command()
    async def play(self, ctx, *query):
        await ctx.message.delete()
        if self.music_channel is None:
            self.music_channel == ctx.channel
        elif ctx.channel == self.music_channel:
            if not self.queue:
                tracks = await wavelink.YouTubeMusicTrack.search(" ".join(query))
                if not tracks:
                    await self.music_channel.send(f"I searched for {' '.join(query)}, but I found nothing.")
                else:
                    track = tracks[0]
                    self.queue.append(track)
                    self.current_track = track

                    if not self.vc:
                        channel = ctx.author.voice.channel
                        if channel:
                            self.vc = await channel.connect(cls=wavelink.Player)

                    if not self.vc.is_playing():
                        await self.vc.play(self.current_track)
                        embedTrack = discord.Embed(
                            title="Added To Queue",
                            description=f"Track Title: {track.title}\nSinger: {track.author}\nDuration: {track.duration}",
                            color=0xb50000
                        )
                        embedTrack.set_thumbnail(url=track.thumbnail)
                        await self.music_channel.send(embed=embedTrack, delete_after=3)
                    else:
                        self.queue.append(track)
                        embedTrack = discord.Embed(
                            title="Added To Queue",
                            description=f"Track Title: {track.title}\nSinger: {track.author}\nDuration: {track.duration}",
                            color=0xb50000
                        )
                        embedTrack.set_thumbnail(url=track.thumbnail)
                        await self.music_channel.send(embed=embedTrack, delete_after=3)
            else:
                while self.vc and not self.vc.is_playing():
                    await self.play_next()
        else:
            await ctx.send("Not the music channel..")

    @commands.command()
    async def skip(self, ctx):
        await ctx.message.delete()
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
        await ctx.message.delete()
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