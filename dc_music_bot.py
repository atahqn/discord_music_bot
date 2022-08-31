from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import discord
import time
from discord.ext import commands
import youtube_dl
import asyncio
from random import choice
TOKEN = "" #api_key
youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

players ={}

Bot = commands.Bot(command_prefix='--')
@Bot.command(pass_context=True)
async def join(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        await ctx.send("çeldum")
        await channel.connect()
    else:
        await ctx.send('Ne? Ses kanalına gir anlamıyorum')
@Bot.command(pass_context=True)
async def leave(ctx):
    if (ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("İyi, ben kaçtım o zaman")
    else:
        await ctx.send('Ne? Ses kanalına gir anlamıyorum')

@Bot.command(name='p',help='This command enables user to play the song prompted')
async def p(ctx,*args):
    msg = " ".join(args)
    path = "C:\Program Files\Google\Chrome\Application\chromedriver.exe"
    driver = webdriver.Chrome(path)
    driver.get('https://www.youtube.com/')
    time.sleep(1)
    search = driver.find_element_by_xpath("/html/body/ytd-app/div[1]/div/ytd-masthead/div[3]/div[2]/ytd-searchbox/form/div[1]/div[1]/input")
    search.send_keys(msg)
    search.send_keys(Keys.RETURN)
    time.sleep(1)
    res = driver.find_element_by_xpath("/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[1]/div[1]/div/div[1]/div/h3/a/yt-formatted-string")
    time.sleep(1)
    print(res.text)
    res.click()
    time.sleep(1)
    url = driver.current_url
    print(url)
    driver.close()

    server = ctx.message.guild
    voice_channel = server.voice_client

    async with ctx.typing():
        player = await YTDLSource.from_url(url, loop=Bot.loop)
        voice_channel.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

    await ctx.send('**Şuan çalan:** {}'.format(player.title))

@Bot.command(name='stop', help='This command stops the music and makes the bot leave the voice channel')
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    await ctx.send("Beni durdurursanız çıkarım.")
    await voice_client.disconnect()
@Bot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.channels, name='genel')
    await channel.send('OOO kral hoşgeldin')
    await channel.send("`--help` ile komutlara ulaşabilirsin")
@Bot.event
async def on_ready():
    print("Selamun aleykum")
status = ["Berkay'ın hayatıyla","Alper'in hayatıyla"]
@Bot.command(name='change_status',help='This command changes the status of the bot')
async def change_status(ctx):
    await Bot.change_presence(activity=discord.Game(choice(status)))
Bot.run(TOKEN)
