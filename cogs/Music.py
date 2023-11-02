import asyncio
import datetime
import time
import discord
import wavelink
from discord.ext import commands


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.current_track = None
        self.queue = []
        self.queue_list = []
        self.vc = None
        self.music_channel = None
        self.volume = 100
        self.last_song_played_time = time.time()
        self.inactive = False

        self.bot.loop.create_task(self.checkStatus())

    async def checkStatus(self):
        while True:
            try:
                if self.vc is not None and self.vc.is_connected():
                    currentTime = time.time()
                    elapsedTime = currentTime - self.last_song_played_time
                    if self.music_channel:
                        mchannel = self.bot.get_channel(self.music_channel)

                    if not self.vc.is_playing():
                        if elapsedTime >= 180:
                            self.inactive = True
                            await self.vc.disconnect()
                            embedInactivity = discord.Embed(
                                description="I've been inactive for more than 3 minutes, I'll be leaving now.",
                                color=0xB50000,
                            )
                            await mchannel.send(embed=embedInactivity)
                            self.inactive = False
                            self.last_song_played_time = None
                        else:
                            pass
                    else:
                        pass
                else:
                    pass
            except Exception as e:
                print(e)

            await asyncio.sleep(20)

    @commands.Cog.listener()
    async def on_wavelink_track_start(self, payload: wavelink.TrackEventPayload):
        mchannel = self.bot.get_channel(self.music_channel)
        self.current_track = payload.track

        trackEmbed = discord.Embed(
            color=0xB50000,
            description=f"Track Title: [{payload.track.title}]({payload.track.uri}) - Singer: {payload.track.author}",
        )
        trackEmbed.set_author(name="Now Playing")
        await mchannel.send(embed=trackEmbed)

    @commands.Cog.listener()
    async def on_wavelink_track_end(self, payload: wavelink.TrackEventPayload):
        mchannel = self.bot.get_channel(self.music_channel)

        if payload.reason == "FINISHED":
            await self.play_next()  # Track finished, play the next one
        elif payload.reason == "STOPPED":
            await self.play_next()  # Track manually stopped, play the next one
        elif payload.reason == "REPLACED":
            await self.play_next()  # Track replaced, play the next one
        elif payload.reason == "LOAD_FAILED":
            embedError = discord.Embed(
                description="Loading of the track failed for some reason.",
                color=0xB50000,
            )
            await mchannel.send(embed=embedError)
            pass  # Handle cleanup as needed
        elif payload.reason == "BOT_DISCONNECTED":
            embedError = discord.Embed(
                description="The bot was disconnected from the voice channel.",
                color=0xB50000,
            )
            await mchannel.send(embed=embedError)
            pass  # Handle bot disconnection as needed
        elif payload.reason == "BOT_ERROR":
            embedError = discord.Embed(
                description="An error occurred in the bot's audio processing.",
                color=0xB50000,
            )
            await mchannel.send(embed=embedError)
            pass  # Handle bot error as needed

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        try:
            if (
                member == self.bot.user
                and before.channel is not None
                and after.channel is None
            ):
                mchannel = self.bot.get_channel(self.music_channel)
                if self.inactive == False:
                    # This code will trigger only when the bot is disconnected
                    embedDisconnected = discord.Embed(
                        description="I've been disconnected, hope to serve you again soon!",
                        color=0xB50000,
                    )

                    await mchannel.send(embed=embedDisconnected)

                self.music_channel = None
                self.last_song_played_time = None
                self.queue = []
                self.queue_list = []

        except Exception as e:
            pass

    def is_valid_link(input_str):
        if input_str.startswith("http") or input_str.startswith("www."):
            return True
        else:
            return False

    async def handle_link(self, ctx, link):
        if ctx.author.voice.channel:
            if self.music_channel is None:
                self.music_channel = ctx.channel.id
            elif self.music_channel is not ctx.channel.id:
                embedError = discord.Embed(
                    description=f"This is not the music channel. Go to <#{self.music_channel}>",
                    color=0xB50000,
                )
                await ctx.send(embed=embedError)
                return

            channel = ctx.author.voice.channel
            mchannel = self.bot.get_channel(self.music_channel)

            if self.vc is None or not self.vc.is_connected():
                self.vc = await channel.connect(cls=wavelink.Player)
                joinEmbed = discord.Embed(
                    description=f"I have been summoned on {channel.mention}",
                    color=0xB50000,
                )
                await ctx.send(embed=joinEmbed)
                self.volume = 100
                await self.set_volume(100)

            # Check if there's a currently playing track
            if not self.vc.is_playing():
                # Load and play the link immediately
                track = await wavelink.YouTubeMusicTrack.build(link)
                await self.play_next(track)
            else:
                # Add the link to the queue
                track = await wavelink.YouTubeMusicTrack.build(link)
                self.queue.append(track)
                embedTrack = discord.Embed(
                    description=f"Track Title: [{track.title}]({track.uri}) - Singer: {track.author}",
                    color=0xB50000,
                )
                embedTrack.set_author(name="Added To Queue")
                embedTrack.set_thumbnail(url=track.thumbnail)
                await ctx.send(embed=embedTrack, delete_after=5)

    async def play_next(self, track=None):
        mchannel = self.bot.get_channel(self.music_channel)
        if not track and self.queue:
            track = self.queue.pop(0)
        if track:
            await self.vc.play(track)
            self.queue.pop(0)
        else:
            self.last_song_played_time = time.time()
            embedNoTracks = discord.Embed(
                description="There's no more tracks on the queue.\nAdd more to start playing again!",
                color=0xB50000,
            )

            await mchannel.send(embed=embedNoTracks, delete_after=120)

    @commands.command()
    async def join(self, ctx):
        self.last_song_played_time = time.time()

        self.volume = 100
        await self.set_volume(100)
        if self.music_channel is None:
            self.music_channel = ctx.channel.id
        else:
            pass

        channel = ctx.author.voice.channel
        if channel:
            self.vc = await channel.connect(cls=wavelink.Player)
            joinEmbed = discord.Embed(
                description=f"I have been summoned in {channel.mention}!",
                color=0xB50000,
            )
            await ctx.send(embed=joinEmbed)
        else:
            errorEmbed = discord.Embed(
                description=f"You are not on a voice channel! Join one and try again.",
                color=0xB50000,
            )
            await ctx.send(embed=errorEmbed)

    @commands.command()
    async def leave(self, ctx):
        mchannel = self.bot.get_channel(self.music_channel)

        if self.music_channel is ctx.channel.id:
            if ctx.voice_client is not None:
                if self.vc and self.vc.is_connected():
                    await self.vc.stop()
                    await self.vc.disconnect()
                    self.music_channel = None
                    self.current_track = None  # Reset the current track
                    self.queue = []  # Clear the queue
                    self.queue_list = []  # Clear the queue list
                    await mchannel.send("That's sad! Hoping to serve you again!")
            else:
                pass
        else:
            errorEmbed = discord.Embed(
                description=f"You are not on a voice channel! Join one and try again.",
                color=0xB50000,
            )
            await ctx.send(embed=errorEmbed)

    @commands.command()
    async def add(self, ctx, *title):
        self.volume = 100
        await self.set_volume(100)
        await ctx.message.delete()
        if ctx.author.voice.channel:
            if self.music_channel is None:
                self.music_channel = ctx.channel.id
            elif self.music_channel != ctx.channel:
                errorEmbed = discord.Embed(
                    description=f"This is not the music channel. Go to <#{self.music_channel}>",
                    color=0xB50000,
                )

                await ctx.send(embed=errorEmbed)

            channel = ctx.author.voice.channel
            if self.vc is None or not self.vc.is_connected():
                self.vc = await channel.connect(cls=wavelink.Player)
                joinEmbed = discord.Embed(
                    description=f"I have been summoned on {channel.mention}",
                    color=0xB50000,
                )
                await ctx.send(embed=joinEmbed)
                self.volume = 100
                await self.set_volume(100)

        query = " ".join(title)
        tracks = await wavelink.YouTubeTrack.search(query)

        if not tracks:
            await ctx.send(f"I searched for {query}, but I found nothing.")
        else:
            num_results = min(
                5, len(tracks)
            )  # Get up to 5 search results or all available results

            # Create a description string to display the search results
            description = "Please choose a track to add to the queue or play:\n"

            for i, track in enumerate(tracks[:num_results]):
                description += (
                    f"{i + 1}. [{track.title}]({track.uri}) - Singer: {track.author}\n"
                )

            # Create an embedded message with the description
            embedSearchResults = discord.Embed(
                title="Search Results", description=description, color=0xB50000
            )

            await ctx.send(embed=embedSearchResults)

            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel

            try:
                response = await ctx.bot.wait_for("message", check=check, timeout=30)
                choice = int(response.content)

                if 1 <= choice <= num_results:
                    chosen_track = tracks[choice - 1]
                    self.queue.append(chosen_track)

                    embedTrack = discord.Embed(
                        description=f"Track Title: [{chosen_track.title}]({chosen_track.uri})\nSinger: {chosen_track.author}",
                        color=0xB50000,
                    )
                    embedTrack.set_author(name="Added To Queue")
                    embedTrack.set_thumbnail(url=chosen_track.thumbnail)
                    await ctx.send(embed=embedTrack, delete_after=5)

                    if not self.vc.is_playing():
                        await self.play_next(chosen_track)
                else:
                    await ctx.send(
                        "Invalid choice. Please select a number from the list."
                    )
            except asyncio.TimeoutError:
                await ctx.send("You took too long to make a choice.")

    @commands.command()
    async def play(self, ctx, *title):
        await ctx.message.delete()

        query = " ".join(title)

        # Check if the input is a valid link (e.g., YouTube link)
        if self.is_valid_link(query):
            # Handle link playback or queueing
            await self.handle_link(ctx, query)
        else:
            # Perform a search for the track
            tracks = await wavelink.YouTubeMusicTrack.search(query)

            if ctx.author.voice.channel:
                if self.music_channel is None:
                    self.music_channel = ctx.channel.id
                elif self.music_channel is not ctx.channel.id:
                    embedError = discord.Embed(
                        description=f"This is not the music channel. Go to <#{self.music_channel}>",
                        color=0xB50000,
                    )
                    await ctx.send(embed=embedError)
                    return

                channel = ctx.author.voice.channel
                mchannel = self.bot.get_channel(self.music_channel)

                if self.vc is None or not self.vc.is_connected():
                    self.vc = await channel.connect(cls=wavelink.Player)
                    joinEmbed = discord.Embed(
                        description=f"I have been summoned on {channel.mention}",
                        color=0xB50000,
                    )
                    await ctx.send(embed=joinEmbed)
                    self.volume = 100
                    await self.set_volume(100)

                # Check if there's a currently playing track
                if not self.vc.is_playing():
                    if not tracks:
                        await mchannel.send(
                            f"I searched for {query}, but I found nothing."
                        )
                    else:
                        num_results = min(
                            5, len(tracks)
                        )  # Get up to 5 search results or all available results

                        # Create a description string to display the search results
                        description = "Please choose a track to play:\n"

                        for i, track in enumerate(tracks[:num_results]):
                            description += f"{i + 1}. [{track.title}]({track.uri}) - Singer: {track.author}\n"

                        # Create an embedded message with the description
                        embedSearchResults = discord.Embed(
                            title="Search Results",
                            description=description,
                            color=0xB50000,
                        )

                        await ctx.send(embed=embedSearchResults)

                        def check(m):
                            return m.author == ctx.author and m.channel == ctx.channel

                        try:
                            response = await ctx.bot.wait_for(
                                "message", check=check, timeout=30
                            )
                            choice = int(response.content)

                            if 1 <= choice <= num_results:
                                chosen_track = tracks[choice - 1]
                                self.queue.append(chosen_track)

                                if not self.vc.is_playing():
                                    await self.play_next(chosen_track)
                                else:
                                    embedTrack = discord.Embed(
                                        description=f"Track Title: [{chosen_track.title}]({chosen_track.uri}) - Singer: {chosen_track.author}",
                                        color=0xB50000,
                                    )
                                    embedTrack.set_author(name="Added To Queue")
                                    embedTrack.set_thumbnail(url=chosen_track.thumbnail)
                                    await ctx.send(embed=embedTrack, delete_after=5)
                            else:
                                await ctx.send(
                                    "Invalid choice. Please select a number from the list."
                                )
                        except asyncio.TimeoutError:
                            await ctx.send("You took too long to make a choice")
                else:
                    if not tracks:
                        await mchannel.send(
                            f"I searched for {query}, but I found nothing."
                        )
                    else:
                        num_results = min(
                            5, len(tracks)
                        )  # Get up to 5 search results or all available results

                        # Create a description string to display the search results
                        description = "Please choose a track to play:\n"

                        for i, track in enumerate(tracks[:num_results]):
                            description += f"{i + 1}. [{track.title}]({track.uri}) - Singer: {track.author}\n"

                        # Create an embedded message with the description
                        embedSearchResults = discord.Embed(
                            title="Search Results",
                            description=description,
                            color=0xB50000,
                        )

                        await ctx.send(embed=embedSearchResults, delete_after=30)

                        def check(m):
                            return m.author == ctx.author and m.channel == ctx.channel

                        try:
                            response = await ctx.bot.wait_for(
                                "message", check=check, timeout=30
                            )
                            choice = int(response.content)

                            if 1 <= choice <= num_results:
                                chosen_track = tracks[choice - 1]
                                self.queue.append(chosen_track)

                                if not self.vc.is_playing():
                                    await self.play_next(chosen_track)
                                else:
                                    embedTrack = discord.Embed(
                                        description=f"Track Title: [{chosen_track.title}]({chosen_track.uri}) - Singer: {chosen_track.author}",
                                        color=0xB50000,
                                    )
                                    embedTrack.set_author(name="Added To Queue")
                                    embedTrack.set_thumbnail(url=chosen_track.thumbnail)
                                    await ctx.send(embed=embedTrack, delete_after=5)
                            else:
                                await ctx.send(
                                    "Invalid choice. Please select a number from the list."
                                )
                        except asyncio.TimeoutError:
                            await ctx.send("You took too long to make a choice.")
            else:
                errorEmbed = discord.Embed(
                    description=f"You are not on a voice channel! Join one and try again.",
                    color=0xB50000,
                )
                await ctx.send(embed=errorEmbed)

    @commands.command()
    async def queue(self, ctx):
        if self.vc and self.vc.is_connected():
            max_tracks_to_display = 10  # Maximum number of tracks to display

            self.queue_list = []

            if self.current_track:
                self.queue_list.append(
                    f"[Currently Playing: {self.current_track.title} - {self.current_track.author}]({self.current_track.uri})"
                )
            if self.queue:
                # Take the first 10 tracks and hide the rest
                displayed_queue = self.queue[:max_tracks_to_display]

                self.queue_list.extend(
                    [
                        f"{index + 1}. [{track.title}]({track.uri}) - {track.author}"
                        for index, track in enumerate(displayed_queue)
                    ]
                )

            embedQueue = discord.Embed(color=0xB50000)
            embedQueue.set_author(name="Queue Manager")
            embedQueue.description = "\n".join(self.queue_list)

            if len(self.queue) > max_tracks_to_display:
                remaining_tracks = len(self.queue) - max_tracks_to_display
                embedQueue.set_footer(
                    text=f"and {remaining_tracks} more track(s) in the queue."
                )
            else:
                embedQueue.set_footer(
                    text="You can add more songs using (ftg.add <Title/Song>)"
                )

            await ctx.send(embed=embedQueue)
        else:
            embedQueue = discord.Embed(
                description="I'm not on my music player state, there are no songs on queue.",
                color=0xB50000,
            )
            embedQueue.set_author(name="Queue Manager")
            embedQueue.set_footer(
                text="You can add songs using to the queue by using (ftg.add <Title/Song>)"
            )

            await ctx.send(embed=embedQueue)

    @commands.command()
    async def qremove(self, ctx, track_number: int):
        if self.queue:
            if 1 <= track_number <= len(self.queue):
                # Subtract 1 from track_number to get the correct index in the list
                index_to_remove = track_number - 1
                removed_track = self.queue.pop(index_to_remove)
                queueEmbed = discord.Embed(
                    description=f"Removed track {track_number}: {removed_track.title} - {removed_track.author} from the queue.",
                    color=0xB50000,
                )
                await ctx.send(embed=queueEmbed)
            else:
                errorEmbed = discord.Embed(
                    description=f"Invalid track number! Try again.", color=0xB50000
                )
                await ctx.send(embed=errorEmbed)
        else:
            errorEmbed = discord.Embed(
                description=f"There are no songs on queue add songs by using ftg.add <song>",
                color=0xB50000,
            )
            await ctx.send(embed=errorEmbed)

    @commands.command()
    async def skip(self, ctx):
        if self.music_channel is None:
            self.music_channel = ctx.channel.id
        elif self.music_channel is ctx.channel.id:
            if self.vc.is_playing():
                if not self.queue:
                    errorEmbed = discord.Embed(
                        description=f"There are no more songs on queue, add more by using ftg.add <song>",
                        color=0xB50000,
                    )
                    await ctx.send(embed=errorEmbed)
                else:
                    track = self.queue.pop(0)
                    await self.vc.play(track)
            else:
                errorEmbed = discord.Embed(
                    description=f"I'm currently not playing any song.", color=0xB50000
                )
                await ctx.send(embed=errorEmbed)
        else:
            errorEmbed = discord.Embed(
                description=f"This is not the music channel. Go to <#{self.music_channel}>",
                color=0xB50000,
            )
            await ctx.send(embed=errorEmbed)

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
            self.music_channel = ctx.channel.id
        elif self.music_channel is ctx.channel.id:
            if self.vc and self.vc.is_playing():
                await self.vc.stop()
            else:
                errorEmbed = discord.Embed(
                    description=f"I'm currently not playing any song.", color=0xB50000
                )
                await ctx.send(embed=errorEmbed)
        else:
            errorEmbed = discord.Embed(
                description=f"This is not the music channel. Go to <#{self.music_channel}>",
                color=0xB50000,
            )
            await ctx.send(embed=errorEmbed)

    @commands.command()
    async def volume(self, ctx, level: int = None):
        if level is not None:
            if self.vc is not None and self.vc.is_connected():
                if 0 <= level <= 100:
                    # Set the volume level
                    self.volume = level
                    await self.set_volume(level)
                    volumeEmbed = discord.Embed(
                        description=f"I've set my volume to {level}%.", color=0xB50000
                    )
                    await ctx.send(embed=volumeEmbed)
                else:
                    # Inform the user that the volume level must be between 0 and 100
                    volumeEmbed = discord.Embed(
                        description=f"Volume must be only between 0% and 100%.",
                        color=0xB50000,
                    )
                    await ctx.send(embed=volumeEmbed)
            else:
                # Inform the user that the bot is not currently in a voice channel
                errorEmbed = discord.Embed(
                    description=f"I'm currently not on a voice channel.", color=0xB50000
                )
                await ctx.send(embed=volumeEmbed)
        else:
            if self.vc is not None:
                # Get and send the current volume amount
                volumeEmbed = discord.Embed(
                    description=f"Current volume is set to {self.volume}%.",
                    color=0xB50000,
                )
                await ctx.send(embed=volumeEmbed)
            else:
                # Inform the user that the bot is not in a voice channel
                errorEmbed = discord.Embed(
                    description=f"I'm currently not on a voice channel.", color=0xB50000
                )
                await ctx.send(embed=volumeEmbed)

    # Add this method to your `Music` class
    async def set_volume(self, level):
        if self.vc is not None:
            await self.vc.set_volume(level)


async def setup(bot):
    await bot.add_cog(Music(bot))
