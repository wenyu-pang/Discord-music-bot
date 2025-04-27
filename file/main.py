import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
import json
import yt_dlp
from collections import deque
song_queue = deque()

# Enable all necessary intents
intents = discord.Intents.default()
intents.guilds = True    # Ensure guild-related events work
intents.message_content = True # if you not turn on bot didn't get any message from  the end user 
# Define bot with command prefix and intents
client = commands.Bot(command_prefix='!', intents=intents)


def get_youtube_audio(url):
    ydl_opts = {
        'format': 'bestaudio/best',# 获取最佳可用音频质量
        'extractaudio': True,# 仅提取音频（忽略视频）
        'audioformat': 'mp3',# 将音频转换为 MP3 格式
        'noplaylist': True,# 确保仅处理单个视频（而不是播放列表）
        'quiet': True,# 抑制不必要的输出（保持日志最少）
        'default_search': 'ytsearch',# 如果提供的是搜索词而不是 URL，则在 YouTube 上搜索
        'outtmpl': 'audio.mp3',# 提取音频的临时文件名
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False) # Extract video/audio info but don't download
        print(info.keys())  # Debugging: See all available keys
        if 'entries' in info:
            info = info['entries'][0]  # Get the first video in the playlist

        if 'url' in info:
            return info['url']
        elif 'formats' in info:
            return info['formats'][0]['url']  # Try getting URL from formats
    return None

    

@client.event
async def on_ready():
    print("The bot is ready for use")
    print("------------------------")
    
 #repeat what you said   
@client.command()
async def test(ctx,arg):# arg is the meassge you want bot to repeat
    await ctx.send(arg)

#-------------------------------------------------    
@client.command()
async def hello(ctx):
    await ctx.send("hello,I am Bensan 小弟")

#-------------------------------------------------    

@client.command()
async def join(ctx):
    if ctx.author.voice:  # Check if user is in a voice channel
        channel = ctx.author.voice.channel  # Get the channel
        author = ctx.author #who call the bot out 
        voic = await channel.connect()  # Bot joins the channel
        #source =FFmpegPCMAudio('W.mp3')
        #player=voic.play(source)
        await ctx.send(f"Bensan 小弟 Joined {channel.name} ✅")
    else:
        await ctx.send("You not in any voice chanel so I can't play the song.")
@client.command()
async def leave(ctx):
    if ctx.voice_client:  # Check if bot is in a voice channel
        await ctx.voice_client.disconnect()# and then bot will left the chanel
        await ctx.send("Left the voice channel ✅")#and then bot will send a message
    else:
        await ctx.send("Bensan 小弟 not in any voice channel! 🚫")#if user not in any channel bot send a message do in not thing

#pause the voic
#-----------------------------------------------------------------------------------------------------------

@client.command()
async def pause(ctx):
    voice=discord.utils.get(client.voice_clients,guild=ctx.guild)#now the bot connect the channel any voic list 
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("Sorry you don't have any sound to playing now , so you can not pause any thing.")
#let the song being resume
@client .command()
async def resume(ctx):
    voice=discord.utils.get(client.voice_clients,guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("At this time there was no song was pause.")
        
@client.command()
async def stop(ctx):
    voice=discord.utils.get(client.voice_clients,guild=ctx.guild)
    voice.stop()


@client.command()
async def play(ctx,url):
    #Check If the Bot Is Connected to a Voice Channel if not bot will be join the voice channel
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if not voice or not voice.is_connected():
        await ctx.invoke(join)
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    song_queue.append(url)  # Add song to queue
    await ctx.send(f"🎵 Added to queue: {url}")
        # If not currently playing, start playing
    if not voice.is_playing():
        await play_next(ctx)

    

async def play_next(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if song_queue:
        url = song_queue.popleft()  # Get the first song in queue
        audio_url = get_youtube_audio(url)
        #从 YouTube 获取直接音频流 URL。
        ffmpeg_options = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn'
        }
    #使用 FFmpeg 转换和传输 YouTube 音频。
        voice.play(FFmpegPCMAudio(audio_url, **ffmpeg_options))
        await ctx.send(f"🎶 Fetching audio from {url}...")
        await ctx.send("🎵 Now playing!")
    else:
        await ctx.send("There is no more song in the list.")

@client.command()
async def skip(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing:
        voice.stop()
        await ctx.send("Skip to the next song.")
        await play_next(ctx)
    else:
        await ctx.send("Sorry there was no more songs in the list.")
        
        
@client.command()
async def clear(ctx):
    song_queue.clear()
    await ctx.send("Cleared all the sogs in the list.")

@client.command()
async def queue(ctx):
    """Display the current song queue"""
    if song_queue:
        queue_list = "\n".join([f"{i+1}. {song}" for i, song in enumerate(song_queue)])
        await ctx.send(f"Current List:\n{queue_list}")
    else:
        await ctx.send("Lists is empty!")


#@client.command()
#async def play(ctx,arg):
    #if ctx.author.voice:
    #voice=ctx.guild.voice_client
    #source =FFmpegPCMAudio(arg)
    #player=voice.play(source)
    
    
client.run('MTMzOTAzMDM3NjYwMDk2MTA2NQ.GeCRVx.cm3mStPVUgJNrGN52kOkQudBZgoEbA2rGVAco8')