import asyncio
import datetime
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
        self.volume = None
        self.last_song_played_time = None
        self.inactivity_checker = self.bot.loop.create_task(self.check_inactivity())

    async def check_inactivity(self):
        while True:
            current_time = datetime.datetime.now()
            elapsed_time = current_time - self.last_song_played_time
            if elapsed_time.total_seconds() > 180:
                # Bot has been inactive for 3 minutes, so disconnect from the voice channel
                await self.bot.voice_client.disconnect()

                if self.vc and self.vc.is_connected():
                    await self.vc.stop()
                    await self.vc.disconnect()
                    self.music_channel = None
                    await self.music_channel.send("I've been inactive for 3 minutes, I'll be disconnecting now. Bye!")
                break
            await asyncio.sleep(60)  # Check every 60 seconds

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
        print(payload.reason)
        if payload.reason == 'FINISHED':
            await self.play_next()  # Track finished, play the next one
        elif payload.reason == 'STOPPED':
            await self.play_next()  # Track manually stopped, play the next one
        elif payload.reason == 'REPLACED':
            await self.play_next()  # Track replaced, play the next one
        elif payload.reason == 'LOAD_FAILED':
            embedError = discord.Embed(
                    description="Loading of the track failed for some reason.",
                    color=0xb50000
                )
            await self.music_channel.send(embed=embedError)
            # Track loading failed, attempt to reload it and place it at the front of the queue
            if payload.track in self.queue:
                self.queue.remove(payload.track)  # Remove the failed track from the queue
            try:
                reloaded_track = await wavelink.YouTubeTrack.search(payload.track.title)
                track = reloaded_track[0]
                if track:
                    self.queue.insert(0, track)  # Place the reloaded track at the front of the queue
                await self.play_next()  # Play the next track in the updated queue
            except Exception:
                reloaded_track = await wavelink.SoundCloudTrack.search(payload.track.title)
                track = reloaded_track[0]
                if track:
                    self.queue.insert(0, track)  # Place the reloaded track at the front of the queue
                await self.play_next()  # Play the next track in the updated queue
        elif payload.reason == 'CLEANUP':
            embedError = discord.Embed(
                    description="Indicates that the cleanup process is occurring.",
                    color=0xb50000
                )
            await self.music_channel.send(embed=embedError)
            pass  # Handle cleanup as needed
        elif payload.reason == 'BOT_DISCONNECTED':
            embedError = discord.Embed(
                    description="The bot was disconnected from the voice channel.",
                    color=0xb50000
                )
            await self.music_channel.send(embed=embedError)
            pass  # Handle bot disconnection as needed
        elif payload.reason == 'BOT_ERROR':
            embedError = discord.Embed(
                    description="An error occurred in the bot's audio processing.",
                    color=0xb50000
                )
            await self.music_channel.send(embed=embedError)
            pass  # Handle bot error as needed

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
                self.queue.clear()  # Clear the queue on disconnection

    async def play_next(self, track=None):
        if not track and self.queue:
            track = self.queue.pop(0)
        if track:
            await self.vc.play(track)
        else:
            embedNoTracks = discord.Embed(
                description="There's no more tracks on the queue.\nAdd more to start playing again!",
                color=0xb50000
            )

            await self.music_channel.send(embed=embedNoTracks)
            self.last_song_played_time = datetime.datetime.now()

    @commands.command()
    async def join(self, ctx):
        if self.volume is None:
            self.volume = 100
            await self.set_volume(100)
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
        if ctx.voice_client is not None:
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
        if self.volume is None:
            self.volume = 100
            await self.set_volume(100)
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
        if self.volume is None:
            self.volume = 100
            await self.set_volume(100)
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
        max_tracks_to_display = 10  # Maximum number of tracks to display

        # Initialize an empty list to store the queue list
        queue_list = []

        if self.current_track:
            queue_list.append(f"**Currently Playing: {self.current_track.title} - {self.current_track.author}**")

        if self.queue:
            # Take the first 10 tracks and hide the rest
            displayed_queue = self.queue[:max_tracks_to_display]

            queue_list.extend([f"{index + 1}. {track.title} - {track.author}" for index, track in enumerate(displayed_queue)])

        embedQueue = discord.Embed(
            color=0xb50000
        )
        embedQueue.set_author(name="Queue Manager")
        embedQueue.description = "\n".join(queue_list)

        if len(self.queue) > max_tracks_to_display:
            remaining_tracks = len(self.queue) - max_tracks_to_display
            embedQueue.set_footer(text=f"and {remaining_tracks} more track(s) in the queue.")

        await ctx.send(embed=embedQueue)
    
    @commands.command()
    async def qremove(self, ctx, track_number: int):
        if self.queue:
            if 1 <= track_number <= len(self.queue):
                # Subtract 1 from track_number to get the correct index in the list
                index_to_remove = track_number - 1
                removed_track = self.queue.pop(index_to_remove)
                await ctx.send(f"Removed track {track_number}: {removed_track.title} - {removed_track.author} from the queue.")
            else:
                await ctx.send("Invalid track number. Please provide a valid number from the queue.")
        else:
            await ctx.send("The queue is currently empty.")


    @commands.command()
    async def skip(self, ctx):
        if self.music_channel is None:
            self.music_channel = ctx.channel
        elif ctx.channel == self.music_channel:
            if self.vc.is_playing():
                if not self.queue:
                    await ctx.send("Queue is empty. Add more songs!")
                else:
                    track = self.queue.pop(0)
                    await self.vc.play(track)
            else:
                await ctx.send("Currently not playing any tracks")
        else:
            await ctx.send("This is not the music channel.")

    @commands.command()
    async def pause(self, ctx):
        if self.vc.is_playing():
            await self.vc.pause()
            await ctx.send("Playback paused.")
        else:
            await ctx.send("Nothing is currently playing to pause.")

    @commands.command()
    async def resume(self, ctx):
        if self.vc.is_paused():
            await self.vc.resume()
            await ctx.send("Playback resumed.")
        else:
            await ctx.send("Playback is not currently paused.")

    @commands.command()
    async def stop(self, ctx):
        if self.music_channel is None:
            self.music_channel = ctx.channel
        elif ctx.channel == self.music_channel:
            if self.vc and self.vc.is_playing():
                await self.vc.stop()
            else:
                await ctx.send("Not playing anything.")
        else:
            await ctx.send("This is not the music channel.")

    @commands.command()
    async def volume(self, ctx, level: int = None):
        if level is not None:
            if self.vc is not None and self.vc.is_connected():
                if 0 <= level <= 100:
                    # Set the volume level
                    self.volume = level
                    await self.set_volume(level)
                    await ctx.send(f"Volume set to {level}%")
                else:
                    # Inform the user that the volume level must be between 0 and 100
                    await ctx.send("Volume level must be between 0 and 100.")
            else:
                # Inform the user that the bot is not currently in a voice channel
                await ctx.send("I'm not currently in a voice channel.")
        else:
            if self.vc is not None:
                # Get and send the current volume amount
                await ctx.send(f"Current volume is set to {self.volume}%")
            else:
                # Inform the user that the bot is not in a voice channel
                await ctx.send("I'm not currently in a voice channel.")


    # Add this method to your `Music` class
    async def set_volume(self, level):
        if self.vc is not None:
            await self.vc.set_volume(level)

async def setup(bot):
    await bot.add_cog(Music(bot))