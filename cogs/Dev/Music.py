import discord
from discord.ext import commands
import yt_dlp

class MusicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.yt_dl = yt_dlp.YoutubeDL()

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice and ctx.author.voice.channel:
            self.voice_channel = await ctx.author.voice.channel.connect()
        else:
            await ctx.send("You are not in a voice channel.")

    @commands.command()
    async def play(self, ctx, url):
        if not self.voice_channel:
            if ctx.author.voice and ctx.author.voice.channel:
                self.voice_channel = await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not in a voice channel. Use `join` command first.")
                return

        info = self.yt_dl.extract_info(url, download=False)
        url = info['formats'][0]['url'] if 'formats' in info and info['formats'] else None

        if url:
            self.voice_channel.stop()
            FFMPEG_OPTIONS = {
                'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                'options': '-vn',
            }
            self.voice_channel.play(discord.FFmpegPCMAudio(url, **FFMPEG_OPTIONS))

    @commands.command()
    async def stop(self, ctx):
        voice_channel = ctx.author.voice.channel
        voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)

        if voice_client and voice_client.is_connected():
            await voice_client.disconnect()

async def setup(bot):
    await bot.add_cog(MusicCog(bot))