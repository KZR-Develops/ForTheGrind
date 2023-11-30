import asyncio
import datetime
import json
import re
import time
from aiohttp import request
import discord
import wavelink
from discord.ext import commands


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = []
        self.queue_list = []
        self.vc = None
        self.music_channel = None
        self.volume = 100
        self.idleTime = 0
        self.inactive = False

        self.bot.loop.create_task(self.checkStatus())

    def is_playlist_link(self, text):
        # Convert the input text to a string if it's a tuple
        if isinstance(text, tuple):
            text = str(text[0])

        # Define regular expression patterns for common playlist URLs
        playlist_patterns = [
            # YouTube playlist
            r'^https?://(?:www\.)?youtube\.com/playlist\?.*',

            # YouTube Music playlist
            r'^https?://music\.youtube\.com/playlist\?.*',
            
            # Spotify playlist
            r'^https?://(?:www\.)?spotify\.com/playlist/.*',
            
            # SoundCloud playlist
            r'^https?://soundcloud\.com/.*?/sets/.*'
        ]

        # Check if the text matches any of the playlist patterns
        for pattern in playlist_patterns:
            if re.match(pattern, text):
                return True

        # If no match is found, it's not a playlist link
        return False

    async def checkStatus(self):
        while True:
            try:
                if self.vc:
                    if not self.vc.is_connected():
                        self.idleTime = 0
                    else:
                        if self.vc.is_playing():
                            self.idleTime = 0
                        elif self.vc.is_paused():
                            currentTime = time.time()
                            elapsedPaused = currentTime - self.pauseTime
                            
                            if round(elapsedPaused) >= 180:
                                mchannel = self.bot.get_channel(self.music_channel)
                                self.inactive = True
                                await self.vc.stop()
                                await self.vc.disconnect()
                                idleEmbed = discord.Embed(
                                    description="I've been paused for more than 3 minutes. I'll just see you later!",
                                    color=0xb50000
                                )

                                await mchannel.send(embed=idleEmbed)
                        elif not self.vc.is_playing() and not self.vc.is_paused():
                            currentTime = time.time()
                            elapsedIdle = currentTime - self.idleTime

                            if round(elapsedIdle) >= 180:
                                mchannel = self.bot.get_channel(self.music_channel)
                                self.inactive = True
                                await self.vc.stop()
                                await self.vc.disconnect()
                                idleEmbed = discord.Embed(
                                    description="I've been idle for more than 3 minutes. I'll just see you later!",
                                    color=0xb50000
                                )

                                await mchannel.send(embed=idleEmbed)

            except Exception as e:
                print(e)

            await asyncio.sleep(10)

    async def play_next(self, track=None):
        mchannel = self.bot.get_channel(self.music_channel)
        self.idleTime = 0

        if self.vc.queue:
            track = self.vc.queue.pop()

        if track:
            await self.vc.play(track)
        elif not self.vc.queue and self.vc and not self.vc.is_playing():
            # No more tracks in the queue and not currently playing
            self.idleTime = time.time()
            embedNoTracks = discord.Embed(
                description="There's no more tracks on the queue. Add more to start playing again!",
                color=0xB50000,
            )
            await mchannel.send(embed=embedNoTracks, delete_after=120)

     # # # Events Listener # # #
    @commands.Cog.listener()
    async def on_wavelink_track_start(self, payload: wavelink.TrackEventPayload):
        mchannel = self.bot.get_channel(self.music_channel)
        self.inactive = False

        trackEmbed = discord.Embed(
            color=0xB50000,
            description=f"[{payload.track.title} - {payload.track.author}]({payload.track.uri})",
        )
        trackEmbed.set_author(name="Currently Playing")
        await mchannel.send(embed=trackEmbed)
        self.idleTime = 0
        

    @commands.Cog.listener()
    async def on_wavelink_track_end(self, payload: wavelink.TrackEventPayload):
        mchannel = self.bot.get_channel(self.music_channel)
        self.pauseTime = 0

        if payload.reason == "FINISHED":
            await self.play_next()
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
                self.idleTime = 0
                self.queue = []
                self.queue_list = []

            elif (
                member == self.bot.user
                and before.channel is None
                and after.channel is not None
            ):
                self.idleTime = time.time()
                self.inactive = True


        except Exception as e:
            pass

    @commands.command(aliases=['summon'])
    async def join(self, ctx):
        self.idleTime = time.time()
        if self.music_channel is None:
            self.music_channel = ctx.channel.id
        else:
            if self.music_channel is not None and not self.vc.is_playing():
                await self.vc.stop()
                await self.vc.disconnect()

        channel = ctx.author.voice.channel
        if channel:
            self.vc: wavelink.Player = await channel.connect(cls=wavelink.Player)
            joinEmbed = discord.Embed(
                description=f"I have been summoned in {channel.mention}!",
                color=0xB50000,
            )
            await ctx.send(embed=joinEmbed)
            return self.vc
        else:
            errorEmbed = discord.Embed(
                description=f"You are not on a voice channel! Join one and try again.",
                color=0xB50000,
            )
            await ctx.send(embed=errorEmbed)

    @commands.command(aliases=['disconnect'])
    async def leave(self, ctx):
        mchannel = self.bot.get_channel(self.music_channel)

        if self.music_channel is ctx.channel.id:
            if ctx.voice_client is not None:
                if self.vc and self.vc.is_connected():
                    await self.vc.stop()
                    await self.vc.disconnect()
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
                    f"{i + 1}. [{track.title} - {track.author}]({track.uri})\n"
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
                    self.vc.queue.put(chosen_track)

                    embedTrack = discord.Embed(
                        description=f"[{chosen_track.title} - {chosen_track.author}]({chosen_track.uri})",
                        color=0xB50000,
                    )
                    embedTrack.set_author(name="Added To Queue")
                    embedTrack.set_thumbnail(url=chosen_track.thumbnail)
                    await ctx.send(embed=embedTrack)

                    if not self.vc.is_playing():
                        await self.play_next(chosen_track)
                else:
                    await ctx.send(
                        "Invalid choice. Please select a number from the list."
                    )
            except asyncio.TimeoutError:
                await ctx.send("You took too long to make a choice.")

    @commands.command(aliases=['p'])
    async def play(self, ctx, *title):
        self.idleTime = 0
        query = " ".join(title)
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
                self.vc: wavelink.Player = await channel.connect(cls=wavelink.Player)
                joinEmbed = discord.Embed(
                    description=f"I have been summoned on {channel.mention}",
                    color=0xB50000,
                )
                await ctx.send(embed=joinEmbed)

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
                        description += f"{i + 1}. [{track.title} - {track.author}]({track.uri})\n"

                    # Create an embedded message with the description
                    embedSearchResults = discord.Embed(
                        title="Search Results",
                        description=description,
                        color=0xB50000,
                    )

                    embedSearchResults.set_footer(text="To choose a song from the list, please send the number of the chosen song.")
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
                            self.vc.queue.put(chosen_track)

                            if not self.vc.is_playing():
                                await self.play_next(self.vc.queue.pop())
                            else:
                                embedTrack = discord.Embed(
                                    description=f"[{chosen_track.title} - {chosen_track.author}]({chosen_track.uri})",
                                    color=0xB50000,
                                )
                                embedTrack.set_author(name="Added To Queue")
                                embedTrack.set_thumbnail(url=chosen_track.thumbnail)
                                await ctx.send(embed=embedTrack)
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
                        description += f"{i + 1}. [{track.title} - {track.author}]({track.uri})\n"

                    # Create an embedded message with the description
                    embedSearchResults = discord.Embed(
                        title="Search Results",
                        description=description,
                        color=0xB50000,
                    )

                    embedSearchResults.set_footer(text="To choose a song from the list, please send the number of the chosen song.")
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
                            self.vc.queue.put(chosen_track)

                            if not self.vc.is_playing():
                                await self.play_next(self.vc.queue.pop())
                            else:
                                embedTrack = discord.Embed(
                                    description=f"[{chosen_track.title} - {chosen_track.author}]({chosen_track.uri})",
                                    color=0xB50000,
                                )
                                embedTrack.set_author(name="Added To Queue")
                                embedTrack.set_thumbnail(url=chosen_track.thumbnail)
                                await ctx.send(embed=embedTrack)
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
        # Check if the bot is connected to a voice channel and is currently playing
        if self.vc is not None:
            if self.vc.queue is None:
                queue_embed = discord.Embed(
                    description="There is no tracks in the queue.",
                    color=0xb50000
                )
                
            else:
                if self.vc and self.vc.is_connected() and self.vc.current:
                    current_track = f"Currently Playing: [{self.vc.current.title} - {self.vc.current.author}]({self.vc.current.uri})\n"
                else:
                    current_track = "No track is currently playing.\n"

                # Generate a formatted list of tracks in the queue
                queue_list = [f"{index}. [{track.title} - {track.author}]({track.uri})" for index, track in enumerate(self.vc.queue, start=1)]

                # Check if there are more tracks in the queue
                if len(self.vc.queue) > 10:
                    remaining_tracks = len(self.vc.queue) - 10
                    queue_list.append(f"and {remaining_tracks} more track(s) in the queue.")

                # Combine the current track and the queue list
                queue_description = current_track + "\nWhat's playing next?"+ "\n".join(queue_list)

                # Create and send the embed
                queue_embed = discord.Embed(
                    description=queue_description,
                    color=0xB50000
                )

            queue_embed.set_author(name="Queue Manager")
            queue_embed.set_footer(text="To add songs use ftg.add <song> or ftg.play <song>")

            await ctx.send(embed=queue_embed)
        else:
            queue_embed = discord.Embed(
                    description="I'm currently not on my player state. Join a voice channel then summon me.",
                    color=0xB50000
                )

            queue_embed.set_author(name="Queue Manager")
            queue_embed.set_footer(text="Try ftg.join while you're on a voice channel to summon me.")

            await ctx.send(embed=queue_embed)
    @commands.command()
    async def qremove(self, ctx, track_number: int):
        if self.vc.queue:
            if 1 <= track_number <= len(self.vc.queue):
                # Subtract 1 from track_number to get the correct index in the list
                index_to_remove = track_number - 1
                removed_track = self.vc.queue.pop(index_to_remove)
                queueEmbed = discord.Embed(
                    description=f"Removed track {track_number}: [{removed_track.title} - {removed_track.author}]({removed_track.uri}) from the queue.",
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
        elif self.music_channel == ctx.channel.id:
            if self.vc and self.vc.is_playing() or self.vc.is_paused():
                if self.vc.queue:
                    track = self.vc.queue.pop()
                    await self.vc.play(track)
                else:
                    # No more tracks in the queue, let the play_next handle it
                    pass
            else:
                # Either no tracks playing or not connected
                errorEmbed = discord.Embed(
                    description="I'm currently not playing any song.",
                    color=0xB50000
                )
                await ctx.send(embed=errorEmbed)
        else:
            # Not the music channel
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
            self.pauseTime = time.time()
        else:
            await ctx.send("Nothing is currently playing to pause.")

    @commands.command()
    async def resume(self, ctx):
        if self.vc.is_paused():
            await self.vc.resume()
            self.pauseTime = 0
            await ctx.send("Playback resumed.")
        else:
            await ctx.send("Playback is not currently paused.")

    @commands.command()
    async def stop(self, ctx):
        if self.music_channel is None:
            self.music_channel = ctx.channel.id
        elif self.music_channel is ctx.channel.id:
            if self.vc and self.vc.is_playing() or self.vc.is_paused():
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
                if level <= 100:
                    await self.vc.set_volume(level)
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
                    description=f"Current volume is set to {self.vc.volume}%.",
                    color=0xB50000,
                )
                await ctx.send(embed=volumeEmbed)
            else:
                # Inform the user that the bot is not in a voice channel
                errorEmbed = discord.Embed(
                    description=f"I'm currently not on a voice channel.", color=0xB50000
                )
                await ctx.send(embed=volumeEmbed)


async def setup(bot):
    await bot.add_cog(Music(bot))