import discord
import youtube_dl
from discord.ext import commands

bot = commands.Bot(command_prefix='!')

@bot.command()
async def play(ctx, url: str):
    if ctx.author.voice is None:
        await ctx.send("You must be in a voice channel to use this command.")
        return

    channel = ctx.author.voice.channel
    await channel.connect()

    server = ctx.message.guild
    voice_channel = server.voice_client

    if 'youtube.com' in url:
        ytdl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
            'quiet': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192'
            }]
        }

        with youtube_dl.YoutubeDL(ytdl_opts) as ytdl:
            info = ytdl.extract_info(url, download=False)
            url = info['url']

    source = await discord.FFmpegOpusAudio.from_probe(url)

    if not voice_channel.is_playing():
        voice_channel.play(source)
    else:
        await ctx.send("The bot is already playing a song.")

@bot.command()
async def leave(ctx):
    if ctx.voice_client is not None:
        await ctx.voice_client.disconnect()
        await ctx.send("Disconnected from the voice channel.")
    else:
        await ctx.send("The bot is not connected to a voice channel.")

bot.run('')
