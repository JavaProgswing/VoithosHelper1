from __future__ import unicode_literals
from keep_alive import keep_alive
import asyncio
from googleapiclient import discovery
import dbl
import validators
import random
import os
import re
import psutil
import discord
import datetime
import contextlib
import io
import pytz
import requests
from discord import Color,Webhook, AsyncWebhookAdapter
import aiohttp
from discord.ext import commands,tasks
from discord.ext.commands import bot
from discord.ext.commands import Greedy
from googlesearch import search
import logging
import json
#from discord.ext.commands.bot import when_mentioned_or
from discord.ext.commands import BucketType
import youtube_dl
from discord_slash import SlashCommand
from mcstatus import MinecraftServer
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from io import BytesIO
from youtubesearchpython import VideosSearch
from googletrans import Translator
translator = Translator()
# Suppress noise about console usage from errors
maintenancemodestatus=False
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
    'no_warnings': False,
    'default_search': 'auto',
    'source_address':
    '0.0.0.0'  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {'options': '-vn'}

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
        data = await loop.run_in_executor(
            None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options),
                   data=data)


logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
exemptspam=[]
prefixlist=[]
antilink=[]
async def get_prefix(client, message):
  if message.guild:
    try:
      return prefixlist[prefixlist.index(message.guild.id)+1]
    except:
      prefixlist.append(message.guild.id)
      prefixlist.append("!")
      return prefixlist[prefixlist.index(message.guild.id)+1]
  else:
    return "!"

client = commands.Bot(command_prefix=get_prefix,case_insensitive=True)
slash = SlashCommand(client, sync_commands=True)
API_KEY = 'AIzaSyB7O6SC44ARFgK8HjdOYbsXnZ6wY9QiSsQ'
service = discovery.build('commentanalyzer', 'v1alpha1', developerKey=API_KEY)
randomjava = [
    "The original name for Java was Oak. It was eventually changed to Java by Sun's marketing department when Sun lawyers found that there was already a computer company registered as Oak. But a legend has it that Gosling and his gang of programmers went out to the local cafe to discuss names and ended up naming it Java. ",
    'James Gosling was working at Sun Labs, around 1992. Gosling and his team was building a set-top box and started by "cleaning up" C++ and wound up with a new language and runtime. Thus, Java or Oak came into being.',
    'Though many would argue that Java is all time favourite among developers, it is the second most popular programming language after C. Java is ranked second in popularity among programming languages.',
    'Currently, about 3 billion mobile phones are working in Java, as well as 125 million TV sets and each Blu-Ray player. This language is continually ranked first in the rankings of software developers as the best choice of programming languages.',
    'Java is free from the concept of Pointer as adding pointers to Java language would compromise security and the robustness, making this language more complex.',
    'In Java, The meaning of Final keyword is not final. It has different meanings in java. It can be Final class, Final method, Final field or Final variable.',
    'Java is used by 95% of the enterprises as their primary language. It is much more than C and the other languages.',
    'A Java developer’s median salary is $83, 975.00. It pays to be a Java developer.',
    'Today, Java rationally runs on more than 1 billion as the Android operating system of Google uses Java APIs.',
    'In one year Java gets downloaded one billion times.'
]
randompython = [
    'This name ‘Python’ is extracted from a British comedy series, “Monty Python’s Flying Circus”. It is not named a snake. It is said that this was the favorite series of its inventor Guido Van Rossum. He named it Python because it is short, mysterious and unique.',
    'Tim Peters wrote an interesting poem about Python which highlights some of the python facts. It is popular as “The Zen of Python”. This poem is beautifully composed. You can get this poem if you write import this in your python compiler.',
    'In Python, there can be multiple comparisons at once. It is able to check multiple conditions at the same time. While in other programming languages, you can not program a chain of comparison operators. The comparison operators can be chained randomly. It does not have to follow a particular order of operators.',
    'Python offers a feature to return multiple values using function. It returns the value as a tuple. While it is not possible with other languages such as Java, C, etc.',
    'Python relies on an interpreter. Unlike other programming languages, it does not need a compiler. The code is stored in a .pyc file. This file acts as a dynamic engine for Python eliminating the need of any compiler.',
    'In Python, every program is done by reference. It does not support pointer.',
    'Python has incorporated the variants of C and Java such as CPython, Jython, etc. The C variant is CPython, to give Python the glimpse benefits of C language. It is because CPython is beneficial in terms of performance, as it has both a compiler and an interpreter. The Java variant of Python is Jython. It drops the highlighting feature of Java such as productivity.',
    'It another interesting fact about Python. It allows you to easily unpack a list or dictionary of all the functions you have used in your program. You can unpack a list by using * and dictionary by using **.',
    'Unlike other languages, Python is the only language that can use else within for a loop. This will be true only when the loop exists naturally and do not break in between.',
    'One can use an “else” clause with a “for” loop in Python. It’s a special type of syntax that executes only if the for loop exits naturally, without any break statements.',
    'Function Argument Unpacking is another awesome feature of Python. One can unpack a list or a dictionary as function arguments using * and ** respectively. This is commonly known as the Splat operator. ',
    ' Want to find the index inside a for loop? Wrap an iterable with ‘enumerate’ and it will yield the item along with its index',
    'One can chain comparison operators in Python answer= 1<x<10 is executable in Python.',
    'We can’t define Infinities right? But wait! Not for Python. . E.g : p_infinity  , n_infinity',
    'Instead of building a list with a loop, one can build it more concisely with a list comprehension. See this code for more understanding.',
    'Finally, Python’s special Slice Operator. It is a way to get items from lists, as well as change them',
    "Python vs java is a common comparsion . Python is dynamically coded and Java is staticly coded . So Java is much faster than python . Java can't do everything that python can , its vice-versa too ."
]
randomlist = randomjava + randompython
userprivilleged=[]
botowners = ["488643992628494347", "625265223250608138"]
bot.cooldownvar = commands.CooldownMapping.from_cooldown(
    2.0, 1.0, commands.BucketType.user)
channelone = None
backupserver=None
@client.event
async def on_command_error(ctx, error):
    global channelone
    errordata=error
    if isinstance(error, commands.CommandInvokeError):
      error = error.original
    if isinstance(error,commands.CommandNotFound):
      return
    if isinstance(error, commands.CheckAnyFailure):
      errordata=error.errors[0]
    if isinstance(error, discord.Forbidden):
        errordata=f" Oops something went wrong while executing the command ."
    if isinstance(error, commands.BotMissingPermissions):
        errordata=f" I do not have the{error.missing_perms[0]} permission ."
    if isinstance(error, commands.MissingPermissions):
        errordata=f" You are lacking the {error.missing_perms[0]} permission ."
    if isinstance(error,commands.MissingRequiredArgument):
        errordata=f" Oops looks like you forgot to put the {str(error.param.name)} in the {ctx.command} command ."
    if isinstance(error,commands.BadArgument):
        errordata=f" Oops looks like provided the wrong arguments in the {ctx.command} command ."     
    if isinstance(error,commands.CommandOnCooldown):
        errordata=f" Seems like you tried this {ctx.command} command recently , try again in {error.retry_after} seconds."     
    embedone = discord.Embed(title=f"Error occured ",description=errordata,color=Color.dark_red())
    embederror = discord.Embed(title=f"Error occured {type(error)}",description=f"**{error}**",color=Color.dark_red())
    if ctx.guild:
        embederror.add_field(name=(f" Guild: {ctx.guild}"),value="\u200b",inline=False)
        embederror.add_field(name=(f" Channel: {ctx.channel.name}"),value="\u200b",inline=False)
        embederror.add_field(name=(f" Member: {ctx.author.mention}"),value="\u200b",inline=False)
        embederror.add_field(name=(f" Message: {ctx.message.content}"),value="\u200b",inline=False)
    else:

        embederror.add_field(name=(" DM Channel "),value="\u200b",inline=False)
        embederror.add_field(name=(f" Member: {ctx.author.mention}"),value="\u200b",inline=False)
        embederror.add_field(name=(f" Message: {ctx.message.content}"),value="\u200b",inline=False)
        embedone = discord.Embed(title="",color=Color.dark_red())
        embedone.add_field(name=" Command error ",value= errordata,inline=False)
    if not isinstance(error, commands.errors.CommandError):
      await channelone.send(embed=embederror)

    await ctx.channel.send(embed=embedone)

class TopGG(commands.Cog):
    """Handles interactions with the top.gg API"""

    def __init__(self, bot):
        self.bot = bot
        self.token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjgwNTAzMDY2MjE4Mzg0NTkxOSIsImJvdCI6dHJ1ZSwiaWF0IjoxNjE2NTEzMzI4fQ.2Ds8_hdV3b5wA8nTPIkNRDaCrH4T2pjupIZPvIMSNL0' # set this to your DBL token
        self.dblpy = dbl.DBLClient(self.bot, self.token, autopost=True) # Autopost will post your guild count every 30 minutes

    async def on_guild_post():
        print("Server count posted successfully")


client.add_cog(TopGG(client))
def convertwords(lst):
    return ' '.join(lst).split()
async def call_background_task(ctx,textchannel,message:str):
    messagecontrol=await textchannel.send(f" This is a message to inform that live status for ip {message} was added in this channel , delete this message to stop live server status (every 30 minutes) .")
    controlid=messagecontrol.id
    while True:
        controlmsg=textchannel.get_partial_message(controlid)
        if controlmsg == None:
          await textchannel.send("The **control message** has been deleted , stopping live server status .")
          break
        cmd = client.get_command("mcservercheck")
        prevmessageid=await cmd(ctx,message)
        await asyncio.sleep(1800)
        ipmsg=textchannel.get_partial_message(prevmessageid)
        try:
          await ipmsg.delete()
        except:
          await textchannel.send(" I don't have `manage messages` permission to delete messages .")
          return
@tasks.loop(seconds=30)
async def saveantilink():
  global antilink
  with open("antilink.txt", "w") as f:
    for links in antilink:
        f.write(str(links) +"\n")

@tasks.loop(seconds=30)
async def saveexemptspam():
  global exemptspam
  with open("exemptspam.txt", "w") as f:
    for channelid in exemptspam:
        f.write(str(channelid) +"\n")
@tasks.loop(seconds=120)
async def saveprefix():
  global prefixlist
  with open("prefixes.txt", "w") as f:
    for prefix in prefixlist:
        f.write(str(prefix) +"\n")
def uservoted(member:discord.Member):
    link = f"https://top.gg/api/bots/805030662183845919/check?userId={member.id}"
    headerstoken={"authorization":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjgwNTAzMDY2MjE4Mzg0NTkxOSIsImJvdCI6dHJ1ZSwiaWF0IjoxNjE2NTEzMzI4fQ.2Ds8_hdV3b5wA8nTPIkNRDaCrH4T2pjupIZPvIMSNL0"}
    f= requests.get(link,headers=headerstoken)
    ftext=f.text
    #print(ftext)
    myfile=json.loads(ftext)
    votereceived=False
    if myfile['voted']>=1:
      votereceived=True
    return votereceived
def voted_on_topgg():
    def predicate(ctx):
      link=f"https://top.gg/api/bots/805030662183845919/check?userId={ctx.author.id}"
      headerstoken={"authorization":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjgwNTAzMDY2MjE4Mzg0NTkxOSIsImJvdCI6dHJ1ZSwiaWF0IjoxNjE2NTEzMzI4fQ.2Ds8_hdV3b5wA8nTPIkNRDaCrH4T2pjupIZPvIMSNL0"}
      f= requests.get(link,headers=headerstoken)
      ftext=f.text
      #print(ftext)
      myfile=json.loads(ftext)
      votereceived=False
      if myfile['voted']>=1:
        votereceived=True
    return commands.check(predicate)

def is_bot_staff():
    def predicate(ctx):
        is_staff = False
        for i in botowners:
            if str(ctx.author.id) == i:
                is_staff = True
        return is_staff

    return commands.check(predicate)


def is_guild_owner():
    def predicate(ctx):
        return (ctx.guild is not None and ctx.guild.owner_id == ctx.author.id
                )

    return commands.check(predicate)
def checkstaff(member):
    is_staff=False
    for i in botowners:
        if str(member.id) == i:
            is_staff = True
            break
    return is_staff

def checkprivilleged(member):
    is_privilleged=False
    for i in userprivilleged:
      if str(member.id) == i:
        is_privilleged = True
        break
    return is_privilleged 
def convert(time):
    pos = ["s", "m", "h", "d"]

    time_dict = {"s": 1, "m": 60, "h": 3600, "d": 3600 * 24}

    unit = time[-1]

    if unit not in pos:
        return -1
    try:
        val = int(time[:-1])
    except:
        return -2

    return val * time_dict[unit]
def validurl(theurl):
  isvalid=False
  try:
     isvalid=validators.url(theurl)
  except:
    pass
  return isvalid
class MyHelp(commands.HelpCommand):
    def get_command_signature(self, command):
      defcommandusage=command.usage
      if defcommandusage==None:
        defcommandusage="command-name"
      #print(str(command.description))
      return '%s%s %s' % (self.clean_prefix, command.qualified_name,defcommandusage)
    async def send_command_help(self, command):
        embed = discord.Embed(title=command.qualified_name+" command .")
        embed.add_field(name=self.get_command_signature(command), value=command.description)
        alias = command.aliases
        if alias:
            embed.add_field(name="Aliases", value=", ".join(alias), inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)


    async def send_bot_help(self, mapping):
        copychannel=self.get_destination()
        embedone = discord.Embed(title="\u200b",description=f"Use {self.clean_prefix}help command-name to gain more information about that command :smiley:",
                                 color=Color.blue())

        for cog, commandloop in mapping.items():
            filtered = await self.filter_commands(commandloop, sort=True)
            command_signatures = [
                self.get_command_signature(c) for c in filtered
            ]

            if command_signatures:
                cog_name = getattr(cog, "qualified_name", ":white_small_square:No Category")

                commandname=cog_name
                if commandname=="Moderation":
                  commandname=":hammer:"+commandname
                elif commandname=="MinecraftFun":
                  commandname="<:grass:825355420604039219>"+commandname
                elif commandname=="Fun":
                  commandname=":trophy:"+commandname
                elif commandname=="Giveaways":
                  commandname=":slot_machine:"+commandname
                elif commandname=="Support":
                  commandname=":tools:"+commandname
                elif commandname=="Music":
                  commandname=":headphones:"+commandname
                elif commandname=="CustomCommands":
                  commandname=":writing_hand: "+commandname
                  
                embedone.add_field(name=commandname,
                                   value="\n".join(command_signatures),
                                   inline=False)
                 

        channel = self.get_destination()
        embedone.add_field(name=":link:About",value="""This bot is developed by <@488643992628494347>, based on discord.py\n
Please visit https://top.gg/bot/805030662183845919 to submit ideas or bugs.""")
        embedone.set_author(name="Commands help",icon_url="https://cdn.discordapp.com/avatars/805030662183845919/70fee8581891e9a810da60944dc486ba.webp?size=128")
        embedone.set_footer(text="Version 1.10 by JavaCoder12",icon_url="https://cdn.discordapp.com/avatars/488643992628494347/e50ae57d9e8880e6acfbc2b444000fa1.webp?size=128")
        try:
          await channel.send(embed=embedone)
        except:
          await channel.send(" I don't have Embed Link permission in this channel to send embed responses .")


client.help_command = MyHelp()


class VoithosInfo(commands.Cog):
    @commands.command(aliases=["info"],brief='This command provides the bot information.', description='This command provides the bot information.',usage="")
    async def botinfo(self, ctx):
      embedVar = discord.Embed(title=f"{client.user}",
                                  description=" ",
                                  color=0x00ff00)
      embedVar.add_field(name='CPU usage ', value=f"{psutil.cpu_percent(1)}%",inline=False)
      embedVar.add_field(name='RAM usage ', value=f"{psutil.virtual_memory()[2]}%",inline=False)
      embedVar.add_field(name="Author",value=" This bot is made by <@625265223250608138> and <@488643992628494347> .",inline=False)
      embedVar.add_field(name="Information",value="""An all-in-one moderation bot coded in python with a punishments system, entertainment facts and profane message filter.""",inline=False)
      embedVar.add_field(name="Websites",value="https://top.gg/bot/805030662183845919",inline=False)
      embedVar.set_thumbnail(url="https://cdn.discordapp.com/avatars/805030662183845919/70fee8581891e9a810da60944dc486ba.webp?size=128")
      embedVar.set_author(name="JavaCoder", icon_url="https://cdn.discordapp.com/avatars/488643992628494347/e50ae57d9e8880e6acfbc2b444000fa1.webp?size=128")
      await ctx.reply(embed=embedVar)

client.add_cog(VoithosInfo(client))
class Moderation(commands.Cog):
    @commands.command(brief='This command resets all channels into a custom format/template.', description='This command resets all channels into a custom format/template and can only be used by administrators .',usage="template url(not necessary)")
    
    @commands.check_any(is_bot_staff(),
                        commands.has_permissions(administrator=True))
    async def settemplate(self, ctx,copytemplate=None):
        if copytemplate==None:
          template=await client.fetch_template("https://discord.new/reSxNdysEDe8")
        else:
          template=await client.fetch_template(copytemplate)
        for channel in ctx.guild.channels:
            if channel == ctx.channel:
                continue
            try:
                await channel.delete()
                await ctx.channel.send(f" Successfully deleted {channel.name}")
            except:
                await ctx.send(
                    f" Please delete {channel.name} on your own , unable to delete channel . "
                )
        botrole=ctx.me.top_role
        for role in ctx.guild.roles:
            try:
              if not botrole==role:
                await role.delete()
                await ctx.channel.send(f" Successfully deleted {role.name}")
            except:
                await ctx.send(
                    f" Please delete {role.name} on your own , unable to delete role . "
                )
        await ctx.send(
            f" Please delete {botrole.name} on your own , unable to delete role . "
        )        
        for recoveryrole in template.source_guild.roles:
          try:
            await ctx.guild.create_role(name=recoveryrole.name,permissions=recoveryrole.permissions,colour=recoveryrole.colour,mentionable=recoveryrole.mentionable,hoist=recoveryrole.hoist)
          except:
            await ctx.send(f" I couldn't create {recoveryrole.name} with {recoveryrole.permissions} and {recoveryrole.colour} colour .")
        copycategory=None
        for recoverycategory in template.source_guild.by_category():
          try:
            copyname=recoverycategory[0].name
          except:
            copyname="General"
          copycategory=await ctx.guild.create_category(copyname)
          for copychannel in recoverycategory[1]:
            if copychannel.type==discord.ChannelType.text:
              await copycategory.create_text_channel(copychannel.name)
            elif copychannel.type==discord.ChannelType.voice:
              await copycategory.create_voice_channel(copychannel.name)          
        await ctx.channel.delete()
    @commands.command(brief='This command checks for links in certain channels.', description='This command checks for links in certain channel and can be used by members having manage_messages permission',usage="#channel")
    @commands.check_any(is_bot_staff(), 
                        commands.has_permissions(manage_messages=True))
    async def enableantilink(self, ctx ,channel:discord.TextChannel=None):
      global antilink
      if channel==None:
        channel=ctx.channel
      if channel.id in antilink:
        raise commands.CommandError("This channel is already being checked for links .")
        return
      else:
        antilink.append(channel.id)
        await ctx.send("Successfully enabled anti-link in this channel .")
    @commands.command(brief='This command disables checking for links in certain channels.', description='This command disables checking for links in certain channel and can be used by members having manage_messages permission',usage="#channel")
    @commands.check_any(is_bot_staff(), 
                        commands.has_permissions(manage_messages=True))
    async def disableantilink(self, ctx ,channel:discord.TextChannel=None): 
      global antilink
      if channel==None:
        channel=ctx.channel    
      if not channel.id in antilink:
        raise commands.CommandError("This channel is not being checked for links .")
        return
      else:
        antilink.remove(channel.id)
        await ctx.send("Successfully disabled anti-link in this channel .")

    @commands.command(brief='This command sets slowmode delay to a certain channel.', description='This command sets slowmode delay to a certain channel and can be used by members having manage messages permission',usage="delay")
    @commands.check_any(is_bot_staff(), 
                        commands.has_permissions(manage_messages=True))
    async def setslowmode(self, ctx ,delay:int): 
      try:
        await ctx.channel.edit(slowmode_delay=delay)
        await ctx.send(f" Successfully set slowmode of {ctx.channel.name} to {delay} seconds .")
      except:
        raise commands.CommandError(" I do not have `manage_channels` permission to set slowmode to this channel ")
    @commands.command(brief='This command stops checking spam in a certain channel.', description='This command stops checking for spam in a certain channel.',usage="#channel")
    @commands.check_any(is_bot_staff(), 
                        commands.has_permissions(manage_messages=True))
    async def disableantispam(self, ctx ,channel:discord.TextChannel=None):    
      global exemptspam
      if channel==None:
        channel=ctx.channel
      if channel.id in exemptspam:
        raise commands.CommandError("This channel is already not being checked for further spamming .")
        return
      exemptspam.append(channel.id)
      await ctx.send(f"{channel.name} will not be checked for message spamming ." )
    @commands.command(brief='This command enables checking spam in a certain channel.', description='This command enables checking spam in a certain channel..',usage="#channel")
    @commands.check_any(is_bot_staff(), 
                        commands.has_permissions(manage_messages=True))
    async def enableantispam(self, ctx ,channel:discord.TextChannel=None):    
      global exemptspam
      if channel==None:
        channel=ctx.channel
      try:
        exemptspam.remove(channel.id)
      except:
        raise commands.CommandError("This channel is already checked for further spamming .")
        return
      await ctx.send(f"{channel.name} will be checked for message spamming ." )
    @commands.command(brief='This command clears given number of messages from the same channel.', description='This command clears given number of messages from the same channel and can be used by members having manage messages permission.',usage="number reason")
    @commands.check_any(is_bot_staff(), 
                        commands.has_permissions(manage_messages=True))
    async def purge(self, ctx, numberstr,*, reason=None):
        if reason == None:
            reason = "no reason provided ."
        if numberstr =="all" or numberstr=="everything":
            textchannelcloned=await ctx.channel.clone(reason=reason)
            await ctx.channel.delete(reason=reason)
            await textchannelcloned.send(f"""{ctx.author.mention} has purged all messages for {reason}""")
            return
        try:
            number=int(numberstr)
        except:
            raise commands.CommandError(" Enter a valid number to purge messages .")
            return
        try:
            await ctx.channel.purge(limit=number)
        except:
            raise commands.CommandError("I do not have `manage messages` permissions to delete messages .")
            return
        await ctx.channel.send(f"""{ctx.author.mention} has purged {number} messages for {reason}""")

    @commands.command(brief='This command prevents users from viewing any channels on the server.', description='This command prevents users from viewing any channels on the server and can be used by members having manage roles permission.',usage="@member time reason")
    @commands.check_any(is_bot_staff(), commands.has_permissions(manage_roles=True))
    async def blacklist(self, ctx, member: discord.Member,timenum=None,*, reason=None):
        if reason == None:
            reason = "no reason provided ."
        if member == client.user:
            raise commands.CommandError("I could not blacklist myself .")
            return
        blacklistrole = discord.utils.get(ctx.guild.roles, name='blacklisted')
        for role in member.roles:
            if role != ctx.guild.default_role:
                if blacklistrole == role:
                    await ctx.channel.send(f"{member.mention} is already blacklisted ."
                                           )
                    return
        blacklistedusers = open("blacklisted.txt", "a")  # append mode
        for role in member.roles:
            if role != ctx.guild.default_role:
                blacklistedusers.write(
                    f"{ctx.guild.id},{member.id},{role.id}.")
                await member.remove_roles(role)

        blacklistrole = discord.utils.get(ctx.guild.roles, name='blacklisted')
        if blacklistrole == None:
            perms = discord.Permissions(send_messages=False,
                                        read_messages=False)
            await ctx.guild.create_role(name='blacklisted', permissions=perms)
            blacklistrole = discord.utils.get(ctx.guild.roles,
                                              name='blacklisted')
            for channelloop in ctx.guild.channels:
                if channelloop.type == discord.ChannelType.text:
                    await channelloop.set_permissions(blacklistrole,
                                                      read_messages=False,
                                                      send_messages=False)

        blacklistrole = discord.utils.get(ctx.guild.roles, name='blacklisted')
        for perm in blacklistrole.permissions:
            permstr = str(perm).replace("(", "")
            permstr = permstr.replace(")", "")
            permlist = permstr.split(",")
            if 'send_messages' in permlist[0] and bool(permlist[1]) == True:
                perms = discord.Permissions(send_messages=False,
                                            read_messages=False)
        for channelloop in ctx.guild.channels:
            if channelloop.type == discord.ChannelType.text:
                await channelloop.set_permissions(blacklistrole,
                                                  read_messages=False,
                                                  send_messages=False)
        blacklistrole = discord.utils.get(ctx.guild.roles,
                                                  name='blacklisted')

        await member.add_roles(blacklistrole)
        try:
            await member.send(f""" You were blacklisted by {ctx.author.mention} in {ctx.guild.name} for {reason} """)
            ##print(f"Successfully dmed users!")
        except:
          pass
        cmd = client.get_command("silentwarn")
        try:
          await cmd(ctx,member,reason=(
            f" {member.mention} was successfully blacklisted by {ctx.author.mention} for {reason} "
        ))
        except:
          pass
        await ctx.channel.send(
            f" {member.mention} was successfully blacklisted by {ctx.author.mention} for {reason} "
        )
        if not timenum==None:
          convertedtime = convert(timenum)
          if convertedtime == -1:
              try:
                  await ctx.channel.purge(limit=count)
              except:
                  await ctx.send(
                      "I do not have `manage messages` permissions to delete messages ."
                  )
                  
              raise commands.CommandError(
                  "You didn't answer with a proper unit. Use (s|m|h|d) next time!"
              )

              return
          elif convertedtime == -2:
              try:
                  await ctx.channel.purge(limit=count)
              except:
                  await ctx.send("I do not have `manage messages` permissions to delete messages .")
                  
              raise commands.CommandError(
                  "The time must be an integer. Please enter an integer next time."
              )
              return
          await asyncio.sleep(convertedtime)
          cmd = client.get_command("unblacklist")
          try:
            await cmd( ctx,member,
                      reason=f"having elapsed {timenum} .")
            return
          except:
              messagesent=await ctx.send(f" I don't have enough permissions to unblacklist {ctx.author.mention} .")
              await asyncio.sleep(5)
              await messagesent.delete()
    @commands.command(brief='This command allows users to view any channel on the server.', description='This command allows users to view any channel on the server and can be used by members having manage roles permission.',usage="@member reason")
    @commands.check_any(is_bot_staff(), 
                        commands.has_permissions(manage_roles=True))
    async def unblacklist(self,
                          ctx,
                          blacklistedmember: discord.Member,*,
                          reason=None):
        blacklistrole = discord.utils.get(ctx.guild.roles, name='blacklisted')
        if blacklistrole == None:
            perms = discord.Permissions(send_messages=False,
                                        read_messages=True)
            await ctx.guild.create_role(name='blacklisted', permissions=perms)
        blacklistrole = discord.utils.get(ctx.guild.roles, name='blacklisted')
        checkrole = False
        for role in blacklistedmember.roles:
            if role != ctx.guild.default_role:
                if blacklistrole == role:
                    checkrole = True
        if not checkrole:
            await ctx.channel.send(f" {blacklistedmember.mention} is not blacklisted .")
                                   
            return
        if reason == None:
            reason = "no reason provided ."
        blacklistrole = discord.utils.get(ctx.guild.roles, name='blacklisted')
        await blacklistedmember.remove_roles(blacklistrole)
        blacklistdusers = open("blacklisted.txt", "r")
        userstring = blacklistdusers.read()
        userlist = userstring.split(".")
        ##print(userlist)
        filestring = ''
        for user in userlist:
            userdetails = user.split(",")
            if userdetails[0] == '':
                break
            if int(userdetails[0]) == ctx.guild.id:
                member = ctx.guild.get_member(int(userdetails[1]))
                role = ctx.guild.get_role(int(userdetails[2]))
                await member.add_roles(role)
            else:
                filestring += f"{userdetails[0]},{userdetails[1]},{userdetails[2]}."
        remainingblacklistdusers = open("blacklisted.txt", "w")
        remainingblacklistdusers.write(filestring)
        try:
            await blacklistedmember.send(f""" You were unblacklisted by {ctx.author.mention} in {ctx.guild.name} for {reason} """)
            ##print(f"Successfully dmed users!")
        except:
          pass
        cmd = client.get_command("silentwarn")
        try:
          await cmd(ctx,blacklistedmember,reason=(
            f""" {blacklistedmember.mention} was successfully unblacklisted by {ctx.author.mention} for {reason} """
        ))
        except:
          pass
        await ctx.channel.send(
            f""" {blacklistedmember.mention} was successfully unblacklisted by {ctx.author.mention} for {reason} """
        )
    @commands.command(brief='This command warns users for a given reason provided.', description='This command warns users for a given reason provided and can be used by bot staff.',usage="@member reason")
    @commands.check_any(is_bot_staff())
    async def silentwarn(self, ctx, member: discord.Member,*, reason=None):
      if reason == None:
        reason="no reason provided ."
      warneduserreason = open(f"{ctx.guild.id}_{member.id}.txt", "a")  
      warneduserreason.write(reason+"\n")
      warneduserreason.close()
    @commands.command(brief='This command warns users for a given reason provided.', description='This command warns users for a given reason provided and can be used by members having manage messages permission')
    @commands.check_any(is_bot_staff(),
                        commands.has_permissions(manage_roles=True))
    async def warn(self, ctx, member: discord.Member,*, reason=None):
      if reason == None:
        reason="no reason provided ."
      await ctx.send(f" {member.mention} was warned by {ctx.author.mention} for {reason} .")
      warneduserreason = open(f"{ctx.guild.id}_{member.id}.txt", "a")  
      warneduserreason.write(reason+"\n")
      warneduserreason.close()
    @commands.command(aliases=['punishments'],brief='This command shows user warnings in the guild .', description='This command shows user warnings in the guild and can be used by  all users. ',usage="@member")
    @commands.check_any(is_bot_staff())
    async def warnings(self, ctx, member: discord.Member):
      filename=f"{ctx.guild.id}_{member.id}.txt"
      file_exists = os.path.isfile(filename) 
      if not file_exists:
        filecreate= open(filename, "w")
        filecreate.close()
      await ctx.send(f" {member.mention} warnings in {ctx.guild.name} are : ")
      count=1
      with open(filename, "r+") as file1:
        try:
          allwarnings=(file1.read())
          singlewarning=allwarnings.splitlines()
          for i in singlewarning:
            await ctx.send(f"{count}) {i}")
            count=count+1
        except:
          pass
    @commands.command(brief='This command (mutes)prevents user from sending messages in any channel .', description='This command (mutes)prevents user from sending messages in any channel and can be used by users having manage roles permission.',usage="@member time reason")
    @commands.check_any(is_bot_staff(), 
                        commands.has_permissions(manage_roles=True))
    async def mute(self, ctx, member: discord.Member,timenum=None,*, reason=None):
        if reason == None:
            reason = "no reason provided ."
        if member == client.user:
            raise commands.CommandError("I could not mute myself .")
            return
        muterole = discord.utils.get(ctx.guild.roles, name='muted')
        for role in member.roles:
            if role != ctx.guild.default_role:
                if muterole == role:
                    await ctx.channel.send(f"{member.mention} is already muted .")
                    return
        muterole = discord.utils.get(ctx.guild.roles, name='muted')
        if muterole == None:
            perms = discord.Permissions(send_messages=False)
            await ctx.guild.create_role(name='muted', permissions=perms)

        muterole = discord.utils.get(ctx.guild.roles, name='muted')
        for perm in muterole.permissions:
            permstr = str(perm).replace("(", "")
            permstr = permstr.replace(")", "")
            permlist = permstr.split(",")
            if 'send_messages' in permlist[0] and bool(permlist[1]) == True:
                perms = discord.Permissions(send_messages=False,
                                            read_messages=True)

        for channelloop in ctx.guild.channels:
            if channelloop.type == discord.ChannelType.text:
                await channelloop.set_permissions(muterole,read_messages=None,send_messages=False)


        muterole = discord.utils.get(ctx.guild.roles, name='muted')

        mutedusers = open("muted.txt", "a")  # append mode
        for role in member.roles:
            if role != ctx.guild.default_role:
                await member.remove_roles(role)
                mutedusers.write(f"{ctx.guild.id},{member.id},{role.id}.")


        await member.add_roles(muterole)
        try:
            await member.send(f""" You were muted by {ctx.author.mention} in {ctx.guild.name} for {reason} """)
            ##print(f"Successfully dmed users!")
        except:
          pass
        cmd = client.get_command("silentwarn")
        try:
          await cmd(ctx,member,reason=(
            f" {member.mention} was successfully muted by {ctx.author.mention} for {reason} "
        ))
        except:
          pass
        await ctx.channel.send(
            f" {member.mention} was successfully muted by {ctx.author.mention} for {reason} "
        )
        if not timenum==None:
          convertedtime = convert(timenum)
          if convertedtime == -1:
              try:
                  await ctx.channel.purge(limit=count)
              except:
                  await ctx.send(
                      "I do not have `manage messages` permissions to delete messages ."
                  )
                  
              raise commands.CommandError(
                  "You didn't answer with a proper unit. Use (s|m|h|d) next time!"
              )

              return
          elif convertedtime == -2:
              try:
                  await ctx.channel.purge(limit=count)
              except:
                  await ctx.send("I do not have `manage messages` permissions to delete messages .")
                  
              raise commands.CommandError(
                  "The time must be an integer. Please enter an integer next time."
              )
              return
          await asyncio.sleep(convertedtime)
          cmd = client.get_command("unmute")
          try:
            await cmd( ctx,member,
                      reason=f"having elapsed {timenum} .")
            return
          except:
              messagesent=await ctx.send(f" I don't have enough permissions to unmute {ctx.author.mention} .")
              await asyncio.sleep(5)
              await messagesent.delete()

    @commands.command(brief='This command (unmutes)allows user to send messages in any channel .', description='This command (unmutes)allows user to send messages in any channel and can be used by users having manage roles permission.',usage="@member reason")
    @commands.check_any(is_bot_staff(), 
                        commands.has_permissions(manage_roles=True))
    async def unmute(self, ctx, mutedmember: discord.Member,*, reason=None):

        muterole = discord.utils.get(ctx.guild.roles, name='muted')
        if muterole == None:
            perms = discord.Permissions(send_messages=False,
                                        read_messages=True)
            await ctx.guild.create_role(name='muted', permissions=perms)
        muterole = discord.utils.get(ctx.guild.roles, name='muted')
        checkrole = False
        for role in mutedmember.roles:
            if role != ctx.guild.default_role:
                if muterole == role:
                    checkrole = True
        if not checkrole:
            await ctx.channel.send(f" {mutedmember.mention} is not muted .")
            return
        if reason == None:
            reason = "no reason provided ."
        muterole = discord.utils.get(ctx.guild.roles, name='muted')
        await mutedmember.remove_roles(muterole)
        mutedusers = open("muted.txt", "r")
        userstring = mutedusers.read()
        userlist = userstring.split(".")
        ##print(userlist)
        filestring = ''
        for user in userlist:
            userdetails = user.split(",")
            if userdetails[0] == '':
                break
            if int(userdetails[0]) == ctx.guild.id:
                role = ctx.guild.get_role(int(userdetails[2]))
                await mutedmember.add_roles(role)
            else:
                filestring += f"{userdetails[0]},{userdetails[1]},{userdetails[2]}."
        remainingmutedusers = open("muted.txt", "w")
        remainingmutedusers.write(filestring)
        try:
            await mutedmember.send(f""" You were unmuted by {ctx.author.mention} in {ctx.guild.name} for {reason} """)
            ##print(f"Successfully dmed users!")
        except:
          pass
        cmd = client.get_command("silentwarn")
        try:
          await cmd(ctx,mutedmember,reason=(
            f""" {mutedmember.mention} was successfully unmuted by {ctx.author.mention} for {reason} """
        ))
        except:
          pass
        await ctx.channel.send(
            f""" {mutedmember.mention} was successfully unmuted by {ctx.author.mention} for {reason} """
        )

    @commands.command(brief='This command unbans user from the guild .', description='This command unbans user from the guild and can be used by users having ban members permission.',usage="@member reason")
    @commands.check_any(is_bot_staff(),
                        commands.has_permissions(ban_members=True))
    async def unban(self, ctx, member: discord.User,*, reason=None):
        if member == None or member == ctx.author:
            raise commands.CommandError(
                " You cannot apply ban/unban actions to your own account .")
            return
        if reason == None:
            reason = "being forgiven ."
        message = f"You have been unbanned from {ctx.guild.name} for {reason}"
        ##print(f"Unsuccessfully DMed users, try again later.")
        try:
            await ctx.guild.unban(member, reason=reason)
        except:
            raise commands.CommandError(f"I do not have ban members permissions or I am not high enough in role hierarchy to unban {member} .")
            return
        try:
            await member.send(message)
            ##print(f"Successfully dmed users!")
        except:
            await ctx.send(
                f"{member.mention} couldn't be direct messaged about the server unban ")
        cmd = client.get_command("silentwarn")
        try:
          await cmd(ctx,member,reason=(
            f"{member.mention} was unbanned from {ctx.guild.name} by {ctx.author.mention} for {reason}"
        ))
        except:
          pass
        await ctx.channel.send(
            f"{member.mention} was unbanned from {ctx.guild.name} by {ctx.author.mention} for {reason}"
        )

    @commands.command(brief='This command bans user from the guild .', description='This command bans user from the guild and can be used by users having ban members permission.',usage="@member reason")
    @commands.check_any(is_bot_staff(), 
                        commands.has_permissions(ban_members=True))
    async def ban(self, ctx, member: discord.User,*, reason=None):
        if member == None or member == ctx.message.author:
            raise commands.CommandError(" You cannot apply ban/unban actions to your own account .")
            return
        if reason == None:
            reason = "being a jerk!"
        message = f"You have been banned from {ctx.guild.name} for {reason}"

        ##print(f"Unsuccessfully DMed users, try again later.")
        try:
            await ctx.guild.ban(member, reason=reason)
        except:
            raise commands.CommandError(f"I do not have ban members permissions or I am not high enough in role hierarchy to ban {member} .")
            return
        try:
            await member.send(message)
            ##print(f"Successfully dmed users!")
        except:
            await ctx.send(
                f"{member.mention} couldn't be direct messaged about the server ban ")
        cmd = client.get_command("silentwarn")
        try:
          await cmd(ctx,member,reason=(
            f"{member.mention} was banned from {ctx.guild.name} by {ctx.author.mention} for {reason}"
        ))
        except:
          pass
        await ctx.channel.send(
            f"{member.mention} was banned from {ctx.guild.name} by {ctx.author.mention} for {reason}"
        )

    @commands.command(brief='This command kicks user from the guild .', description='This command kicks user from the guild and can be used by users having kick members permission.',usage="@member reason")
    @commands.check_any(is_bot_staff(), 
                        commands.has_permissions(kick_members=True))
    async def kick(self, ctx, member: discord.User,*, reason=None):
        if member == None or member == ctx.message.author:
            raise commands.CommandError(" You cannot kick your own account from this guild.")
            return

        if reason == None:
            reason = "being a jerk!"
        message = f"You have been kicked from {ctx.guild.name} for {reason}"

        ##print(f"Unsuccessfully DMed users, try again later.")
        try:
            await ctx.guild.kick(member, reason=reason)
        except:
            raise commands.CommandError(f"I do not have ban members permissions or I am not high enough in role hierarchy to kick {member} .")
        try:
            await member.send(message)
            ##print(f"Successfully dmed users!")
        except:
            await ctx.send(
                f"{member.mention} couldn't be direct messaged about the server kick ")
        cmd = client.get_command("silentwarn")
        try:
          await cmd(ctx,member,reason=(
            f"{member.mention} was kicked from {ctx.guild.name} by {ctx.author.mention} for {reason}"
        ))
        except:
          pass
        await ctx.channel.send(
            f"{member.mention} was kicked from {ctx.guild.name} by {ctx.author.mention} for {reason}"
        )


client.add_cog(Moderation(client))
class MinecraftFun(commands.Cog):
    #cool
    @commands.cooldown(1,30,BucketType.user)
    @commands.command(brief='This command shows the mined inventory items.', description='This command shows the mined inventory items of the user.',usage="")
    async def inventory(self,ctx):
      file1 = open(f"{ctx.author.id}_mine.txt", "w")
      file1.close()
      inventory = open(f"{ctx.author.id}_mine.txt", "r")
      invstring = inventory.read()
      itemslist = invstring.split(",")
      embedOne = discord.Embed(title=f"{ctx.author.name}",
                            description="Inventory",           color=Color.green())
      
      for item in itemslist:
        if item == '':
          break
        embedOne.add_field(name=item,value="\u200b",inline=False)
      await ctx.send(embed=embedOne)    

    @commands.command(brief='This command is used to mine items.', description='This command is used to mine items and store it in inventory.',usage="")   
    async def mine(self,ctx):
      """
      mobappearlist=["mine","mine","mine","mob"]
      mobappearchances=[20,20,30,30]
      mobappearlist=random.choices(mobappearlist,mobappearchances,k=1)
      mobappearresult=mobappearlist[0]
      if mobappearresult=="mob":
        minecraftmobs=["Zombie","Skeleton","Creeper"]

        creeperdamage=[10,15,0,5,0]
        skeletondamage=[2,3,4,5,0]
        zombiedamage=[2.5,3,4.5,0]
        selectedmob=random.choice(minecraftmobs)
        embedOne = discord.Embed(title=f"{ctx.author.name}",
                            description=f"A wild {selectedmob} appeared !",           color=Color.red())
        embedOne.add_field(name=f"Pvp the {selectedmob} by typing `f`.",value="\u200b",inline=False)
        await ctx.send(embed=embedOne)
        pvpmember_health=25
        mob_health=20
        pvpmember=ctx.author
        def check(m):
          nonlocal pvpmember,selectedmob,creeperdamage,zombiedamage,skeletondamage,pvpmember_health,mob_health
          if pvpmember==m.author:
            strengthlist=[1,2,3]
            randomdamage=random.choice(strengthlist)
            client.loop.create_task( ctx.channel.send(f"{pvpmember.mention} dealt {randomdamage} to {selectedmob} ."))
            mob_health-=randomdamage
            if mob_health<=0:
              client.loop.create_task( ctx.channel.send(f"{pvpmember.mention} defeated the {selectedmob} "))
              return True
            if selectedmob=="Zombie":
              damagedealt=random.choice(zombiedamage)
            if selectedmob=="Creeper":
              damagedealt=random.choice(creeperdamage)
            if selectedmob=="Skeleton":
              damagedealt=random.choice(skeletondamage)
            pvpmember_health-=damagedealt
            client.loop.create_task( ctx.channel.send(f" **{selectedmob}** dealt {damagedealt} to {pvpmember.mention} ."))
            if pvpmember_health<=0:
              client.loop.create_task( ctx.channel.send(f" **{pvpmember.mention}** was defeated by the mob {selectedmob} ."))
              return True        
            player_health=""
            for i in range(int(pvpmember_health/2)):
              player_health+=":heart:"
            client.loop.create_task( ctx.channel.send(f" {pvpmember.mention} health : {player_health} "))
            
          return False
        msg = await client.wait_for('message', check=check,timeout=120)
        return
      """

      blocks=["Clay","Coal","Diamond","Gold","Gravel","Ice","Iron","Sand","Stone","Grass"]
      blockemojilist=["<:clay:825355418083655740>","<:coal:825355417802375188>","<:diamond:825355417717833729>","<:gold:825355419420983317>","<:gravel:825355419030781994>","<:ice:825355417621626890>","<:iron:825355419140227082>","<:sand:825355420080144406>","<:stone:825355417810632704>","<:grass:825355420604039219>"]
      chance = [13,8,5,8,13,10,7,7,14,15]

      results = random.choices(blocks,chance,k=1)
      embedOne = discord.Embed(title=f"Blocks mined",
                            description=f"\u200b",           color=Color.green())
      embedOne.add_field(name=f"{(blockemojilist[blocks.index(results[0])])} {results[0]}",value="\u200b",inline=False)
      await ctx.send(embed=embedOne)
      file1 = open(f"{ctx.author.id}_mine.txt", "w")
      file1.close()
      file1 = open(f"{ctx.author.id}_mine.txt", "a")
      file1.write(results[0]+",")
      file1.close()

    @commands.cooldown(1,30,BucketType.user)
    @commands.command(brief='This command is used to generate terrain (similar to minecraft).', description='This command is used to generate terrain (similar to minecraft).',usage="number")
    async def generateterrain(self,ctx,number=8):
      blocks=["clay","coal","diamond","gold","gravel","ice","iron","sand","stone","dirt","grass","water","air"]
      blockemojilist=["<:clay:825355418083655740>","<:coal:825355417802375188>","<:diamond:825355417717833729>","<:gold:825355419420983317>","<:gravel:825355419030781994>","<:ice:825355417621626890>","<:iron:825355419140227082>","<:sand:825355420080144406>","<:stone:825355417810632704>","<:dirt:825364586991583272>","<:grass:825355420604039219>","<:water:825366913966276618>","<:air:825368135863500822>"]
      surfaceblocks=["water","grass","sand","air"]
      surfacechance=[30,40,20,10]
      chance = [13,15,5,13,11,0,9,0,19,15,0,0,0]
      belowblocks="<:bedrock:825370647869259848>"
      belowlist=""
      results = random.choices(blocks,chance,k=number*number)
      sumloop=0
      for i in range(0,number): 
        blockemojis=""
        for j in range(number):
          #print(sumloop)
          chosenblock=results[sumloop]
          if sumloop<=number:
            chosenlist=random.choices(surfaceblocks,surfacechance,k=1)
            chosenblock=chosenlist[0]
          blockemojis+=f"{blockemojilist[blocks.index(chosenblock)]}"
          #print(blockemojis)
          sumloop+=1
        await ctx.send(blockemojis)
      for i in range(number):
        belowlist+=belowblocks
      await ctx.send(belowlist)
        
    @commands.cooldown(1,30,BucketType.user)
    @commands.command(brief='This command is used to fight other users (minecraft pvp mechanics).', description='This command is used to fight other users (minecraft pvp mechanics).',usage="@member")
    async def pvp(self,ctx,member:discord.Member):
      if member==ctx.author:
        await ctx.channel.send(" Trying to battle yourself will only have major consequences !")
        return
        
      orechoice=["Netherite","Diamond","Iron","Leather"]
      swordchoice=["Netherite","Diamond","Iron","Stone","Gold","Wood"]
      armorresist=[85.0,75.0,60.0,28.0]
      swordattack=[12.0,10.0,9.0,8.0,6.0,5.0]
      memberone=ctx.author
      membertwo=member
      messagereact=await ctx.channel.send(f'React with that 👍 reaction in 60 seconds, {member.mention} to start the pvp match !')
      await messagereact.add_reaction("👍")
      escapelist=["ran away like a coward .","was scared of a terrible defeat .","didn't know how to fight ."," escaped in the midst of a battle .",f"was too weak for battling {ctx.author.mention} .",f"was scared of fighting {ctx.author.mention} ."]
      def check(reaction, user):
        return user == member and str(reaction.emoji) == '👍'

      try:
        reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)

      except asyncio.TimeoutError:
        await ctx.channel.send(f'{member} {random.choice(escapelist)}')
        return
      else:
          await ctx.reply('Let the battle preparations take place !')
      try:
        await ctx.channel.edit(slowmode_delay=1)
      except:
        raise commands.CommandError(" I do not have `manage_channels` permission to set slowmode to this channel ")
      memberone_healthpoint=30+random.randint(-10,10)
      memberone_armor=random.choice(orechoice)
      memberone_armor_resist=armorresist[orechoice.index(memberone_armor)]
      memberone_sword=random.choice(swordchoice)
      memberone_sword_attack=swordattack[swordchoice.index(memberone_sword)]
      membertwo_healthpoint=30+random.randint(-10,10)
      membertwo_armor=random.choice(orechoice)
      membertwo_armor_resist=armorresist[orechoice.index(membertwo_armor)]
      membertwo_sword=random.choice(swordchoice)
      membertwo_sword_attack=swordattack[swordchoice.index(membertwo_sword)]
      await ctx.channel.send(f" {ctx.author.mention}({memberone_healthpoint} Hitpoints) prepared a {memberone_armor} armor and a {memberone_sword} sword to obliterate {member} .")
      await ctx.channel.send(f" {member.mention}({membertwo_healthpoint} Hitpoints) prepared a {membertwo_armor} armor and a {membertwo_sword} sword to obliterate {ctx.author.mention} .")
      await ctx.channel.send(f'(No spamming)👍 Let the battle commence between {member.mention} and {ctx.author.mention} .') 
      await ctx.channel.send(' Type `f` to fight with sword and `d` to defend . `(NOTE: This is instantaneous and the member to obliterate other wins !)`' )
      memberone_resistance=False
      membertwo_resistance=False
      memberone_resistances=0
      memberone_critical=0
      memberone_strong=0
      memberone_weak=0
      membertwo_resistances=0
      membertwo_critical=0
      membertwo_strong=0
      membertwo_weak=0      
      def check(m):
        user=m.author
        message=m.content
        nonlocal memberone,membertwo,memberone_healthpoint,membertwo_healthpoint,memberone_armor_resist,memberone_sword_attack,membertwo_armor_resist,membertwo_sword_attack,memberone_resistance,membertwo_resistance,memberone_resistances,memberone_critical,memberone_strong,memberone_weak,membertwo_resistances,membertwo_critical,membertwo_strong,membertwo_weak
        if message=='f' or message=='d':
          attack=['weak','strong','critical']
          attackdamage=[0.5,1.5,2.0]
          winmessage=[" was shot by "," was slain by "," was pummeled by "," drowned whilst trying to escape "," was blown up by "," hit the ground too hard whilst trying to escape "," was squashed by a falling anvil whilst fighting "," was squashed by a falling block whilst fighting "," was skewered by a falling stalactite whilst fighting "," walked into fire whilst fighting "," was burnt to a crisp whilst fighting "," went off with a bang due to a firework fired by "," tried to swim in lava to escape "," was struck by lightning whilst fighting ","walked into danger zone due to "," was killed by magic whilst trying to escape "," was frozen to death by "," was fireballed by "," didn't want to live in the same world as "," was impaled by "," was killed trying to hurt "," was poked to death by a sweet berry bush whilst trying to escape "," withered away whilst fighting "]
          if user==memberone:
            if message=='f':

              attackchoice=random.choice(attack)
              if attackchoice=="weak":
                memberone_weak+=1
              if attackchoice=="strong":
                memberone_strong+=1
              if attackchoice=="critical":
                memberone_critical+=1
              attackvalue=attackdamage[attack.index(attackchoice)]
              armorresistvalue=100.0-membertwo_armor_resist
              damagevalue=(armorresistvalue/100.0)*(memberone_sword_attack*attackvalue)
              if membertwo_resistance:
                client.loop.create_task( ctx.channel.send(f" The shield protected {membertwo.mention} from {(0.4*damagevalue)} hitpoints ."))
                damagevalue*=0.6
                membertwo_resistance=False
              client.loop.create_task( ctx.channel.send(f"{memberone.mention} dealt {damagevalue} to {membertwo.mention} with a {attackchoice} hit."))
              membertwo_healthpoint-=damagevalue           
              player_health=""
              for i in range(int(membertwo_healthpoint)):
                player_health+=":heart:"
              client.loop.create_task( ctx.channel.send(f" {membertwo.mention} health : {player_health} ."))
              
              if membertwo_healthpoint<=0.0:
                client.loop.create_task( ctx.channel.send(f" {membertwo.mention}{random.choice(winmessage)}{memberone.mention} ."))
                return True
            elif message=='d':
              memberone_resistances+=1
              client.loop.create_task( ctx.channel.send(f" {memberone.mention} has equipped the shield ."))
              memberone_resistance=True
          if user==membertwo:
            if message=='f':
              attackchoice=random.choice(attack)
              if attackchoice=="weak":
                membertwo_weak+=1
              if attackchoice=="strong":
                membertwo_strong+=1
              if attackchoice=="critical":
                membertwo_critical+=1
              attackvalue=attackdamage[attack.index(attackchoice)]
              armorresistvalue=100.0-memberone_armor_resist
              damagevalue=(armorresistvalue/100)*(membertwo_sword_attack*attackvalue)
              if memberone_resistance:
                client.loop.create_task( ctx.channel.send(f" The shield protected {memberone.mention} from {(0.4*damagevalue)} hitpoints ."))
                damagevalue*=0.6
                memberone_resistance=False
              client.loop.create_task( ctx.channel.send(f"{membertwo.mention} dealt {damagevalue} to {memberone.mention} with a {attackchoice} hit."))

              memberone_healthpoint-=damagevalue
              player_health=""
              for i in range(int(memberone_healthpoint)):
                player_health+=":heart:"
              client.loop.create_task( ctx.channel.send(f" {memberone.mention} health : {player_health} ."))
              
              if memberone_healthpoint<=0.0:
                client.loop.create_task( ctx.channel.send(f" {memberone.mention}{random.choice(winmessage)}{membertwo.mention} ."))
                return True
            elif message=='d':
              memberone_resistances+=1
              client.loop.create_task( ctx.channel.send(f" {membertwo.mention} has equipped the shield ."))      
              membertwo_resistance=True
        return False    
                
      msg = await client.wait_for('message', check=check,timeout=120)
      embedOne = discord.Embed(title="Battle results",
                            description=f"{memberone.name} and {membertwo.name}",
                            color=Color.green())
      embedOne.add_field(name=f"{memberone.name} ",value=f"{memberone_armor} Armor({memberone_armor_resist}% resistance) ,{memberone_sword} Sword({memberone_sword_attack} attack damage) .",inline=False)
      embedOne.add_field(name=(f"{memberone.name} Battle Stats "),value=f"Shield used: {memberone_resistances} , Critical damage : {memberone_critical} , Strong damage : {memberone_strong} , Weak Damage : {memberone_weak} .",inline=False)
      embedOne.add_field(name=f"{membertwo.name} ",value=f"{membertwo_armor} Armor({membertwo_armor_resist}% resistance) ,{membertwo_sword} Sword({membertwo_sword_attack} attack damage) .",inline=False)
      embedOne.add_field(name=(f"{membertwo.name} Battle Stats "),value=f"Shield used: {membertwo_resistances} , Critical damage : {membertwo_critical} , Strong damage : {membertwo_strong} , Weak Damage : {membertwo_weak} .",inline=False)
      if memberone_healthpoint<=0:
        embedOne.add_field(name=f"Winner {membertwo.name}",value=f"Health: {membertwo_healthpoint}",inline=True)
      elif membertwo_healthpoint<=0: 
        embedOne.add_field(name=f"Winner {memberone.name}",value=f"Health: {memberone_healthpoint}",inline=True)
      else:
        embedOne.add_field(name=f"Match Tied",value=f"{memberone_healthpoint}",inline=True)
      await ctx.send(embed=embedOne)
    @commands.cooldown(1,30,BucketType.user)
    @commands.command(brief='This command is used to fight other users with sound effects(minecraft pvp mechanics).', description='This command is used to fight other users with sound effects(minecraft pvp mechanics).',usage="@member")
    async def soundpvp(self,ctx,member:discord.Member):
      if member==ctx.author:
        await ctx.channel.send(" Trying to battle yourself will only have major consequences !")
        return
        
      orechoice=["Netherite","Diamond","Iron","Leather"]
      swordchoice=["Netherite","Diamond","Iron","Stone","Gold","Wood"]
      armorresist=[85.0,75.0,60.0,28.0]
      swordattack=[12.0,10.0,9.0,8.0,6.0,5.0]
      memberone=ctx.author
      membertwo=member
      messagereact=await ctx.send(f'React with that 👍 reaction in 60 seconds, {member.mention} to start the pvp match !')
      await messagereact.add_reaction("👍")
      escapelist=["ran away like a coward .","was scared of a terrible defeat .","didn't know how to fight ."," escaped in the midst of a battle .",f"was too weak for battling {ctx.author.mention} .",f"was scared of fighting {ctx.author.mention} ."]
      def check(reaction, user):
        return user == member and str(reaction.emoji) == '👍'

      try:
        reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)

      except asyncio.TimeoutError:
        await ctx.channel.send(f'{member} {random.choice(escapelist)}')
        return
      else:
          await ctx.reply('Let the battle preparations take place !')
      try:
        await ctx.channel.edit(slowmode_delay=1)
      except:
        raise commands.CommandError(" I do not have `manage_channels` permission to set slowmode to this channel ")

      memberone_healthpoint=30+random.randint(-10,10)
      memberone_armor=random.choice(orechoice)
      memberone_armor_resist=armorresist[orechoice.index(memberone_armor)]
      memberone_sword=random.choice(swordchoice)
      memberone_sword_attack=swordattack[swordchoice.index(memberone_sword)]
      membertwo_healthpoint=30+random.randint(-10,10)
      membertwo_armor=random.choice(orechoice)
      membertwo_armor_resist=armorresist[orechoice.index(membertwo_armor)]
      membertwo_sword=random.choice(swordchoice)
      membertwo_sword_attack=swordattack[swordchoice.index(membertwo_sword)]
      await ctx.channel.send(f" {ctx.author.mention}({memberone_healthpoint} Hitpoints) prepared a {memberone_armor} armor and a {memberone_sword} sword to obliterate {member} .")
      await ctx.channel.send(f" {member.mention}({membertwo_healthpoint} Hitpoints) prepared a {membertwo_armor} armor and a {membertwo_sword} sword to obliterate {ctx.author.mention} .")
      await ctx.channel.send(f'(No spamming)👍 Let the battle commence between {member.mention} and {ctx.author.mention} .') 
      await ctx.channel.send(' Type `f` to fight with sword and `d` to defend . `(NOTE: This is instantaneous and the member to obliterate other wins !)`' )
      voicechannel=ctx.voice_client
      voicechannel.play(discord.FFmpegPCMAudio("Random_levelup.ogg"))
      memberone_resistance=False
      membertwo_resistance=False
      memberone_resistances=0
      memberone_critical=0
      memberone_strong=0
      memberone_weak=0
      membertwo_resistances=0
      membertwo_critical=0
      membertwo_strong=0
      membertwo_weak=0      
      def check(m):
        user=m.author
        message=m.content
        nonlocal memberone,membertwo,memberone_healthpoint,membertwo_healthpoint,memberone_armor_resist,memberone_sword_attack,membertwo_armor_resist,membertwo_sword_attack,memberone_resistance,membertwo_resistance,voicechannel,memberone_resistances,memberone_critical,memberone_strong,memberone_weak,membertwo_resistances,membertwo_critical,membertwo_strong,membertwo_weak
        if message=='f' or message=='d':
          attack=['weak','strong','critical']
          attackdamage=[0.5,1.5,2.0]
          winmessage=[" was shot by "," was slain by "," was pummeled by "," drowned whilst trying to escape "," was blown up by "," hit the ground too hard whilst trying to escape "," was squashed by a falling anvil whilst fighting "," was squashed by a falling block whilst fighting "," was skewered by a falling stalactite whilst fighting "," walked into fire whilst fighting "," was burnt to a crisp whilst fighting "," went off with a bang due to a firework fired by "," tried to swim in lava to escape "," was struck by lightning whilst fighting ","walked into danger zone due to "," was killed by magic whilst trying to escape "," was frozen to death by "," was fireballed by "," didn't want to live in the same world as "," was impaled by "," was killed trying to hurt "," was poked to death by a sweet berry bush whilst trying to escape "," withered away whilst fighting "]
          if user==memberone:
            if message=='f':

              attackchoice=random.choice(attack)
              if voicechannel.is_playing():
                  voicechannel.stop()
              if attackchoice=="weak":
                memberone_weak+=1
                voicechannel.play(discord.FFmpegPCMAudio("Weak_attack1.ogg"))
              if attackchoice=="strong":
                memberone_strong+=1
                voicechannel.play(discord.FFmpegPCMAudio("Strong_attack1.ogg"))
              if attackchoice=="critical":
                memberone_critical+=1
                voicechannel.play(discord.FFmpegPCMAudio("Critical_attack1.ogg"))
              attackvalue=attackdamage[attack.index(attackchoice)]
              armorresistvalue=100.0-membertwo_armor_resist
              damagevalue=(armorresistvalue/100.0)*(memberone_sword_attack*attackvalue)
              if membertwo_resistance:
                client.loop.create_task( ctx.channel.send(f" The shield protected {membertwo.mention} from {(0.4*damagevalue)} hitpoints ."))
                damagevalue*=0.6
                membertwo_resistance=False
              client.loop.create_task( ctx.channel.send(f"{memberone.mention} dealt {damagevalue} to {membertwo.mention} with a {attackchoice} hit."))
              membertwo_healthpoint-=damagevalue  
              player_health=""
              for i in range(int(membertwo_healthpoint)):
                player_health+=":heart:"
              client.loop.create_task( ctx.channel.send(f" {membertwo.mention} health : {player_health} ."))         
              
              if membertwo_healthpoint<=0.0:
                client.loop.create_task( ctx.channel.send(f" {membertwo.mention}{random.choice(winmessage)}{memberone.mention} ."))
                if voicechannel.is_playing():
                  voicechannel.stop()
                voicechannel.play(discord.FFmpegPCMAudio("Player_hurt1.ogg"))
                return True
            elif message=='d':
              memberone_resistances+=1
              client.loop.create_task( ctx.channel.send(f" {memberone.mention} has equipped the shield ."))
              memberone_resistance=True
              if voicechannel.is_playing():
                voicechannel.stop()
              voicechannel.play(discord.FFmpegPCMAudio("Shield_block5.ogg"))
          if user==membertwo:
            if message=='f':
              attackchoice=random.choice(attack)
              if voicechannel.is_playing():
                voicechannel.stop()
              if attackchoice=="weak":
                membertwo_weak+=1
                voicechannel.play(discord.FFmpegPCMAudio("Weak_attack1.ogg"))
              if attackchoice=="strong":
                membertwo_strong+=1
                voicechannel.play(discord.FFmpegPCMAudio("Strong_attack1.ogg"))
              if attackchoice=="critical":
                membertwo_critical+=1
                voicechannel.play(discord.FFmpegPCMAudio("Critical_attack1.ogg"))
              attackvalue=attackdamage[attack.index(attackchoice)]
              armorresistvalue=100.0-memberone_armor_resist
              damagevalue=(armorresistvalue/100)*(membertwo_sword_attack*attackvalue)
              if memberone_resistance:
                client.loop.create_task( ctx.channel.send(f" The shield protected {memberone.mention} from {(0.4*damagevalue)} hitpoints ."))
                damagevalue*=0.6
                memberone_resistance=False
              client.loop.create_task( ctx.channel.send(f"{membertwo.mention} dealt {damagevalue} to {memberone.mention} with a {attackchoice} hit."))

              memberone_healthpoint-=damagevalue
              player_health=""
              for i in range(int(memberone_healthpoint)):
                player_health+=":heart:"
              client.loop.create_task( ctx.channel.send(f" {memberone.mention} health : {player_health} ."))
              if memberone_healthpoint<=0.0:
                client.loop.create_task( ctx.channel.send(f" {memberone.mention}{random.choice(winmessage)}{membertwo.mention} ."))
                if voicechannel.is_playing():
                  voicechannel.stop()
                voicechannel.play(discord.FFmpegPCMAudio("Player_hurt1.ogg"))
                return True
            elif message=='d':
              memberone_resistances+=1
              client.loop.create_task( ctx.channel.send(f" {membertwo.mention} has equipped the shield ."))      
              membertwo_resistance=True
              if voicechannel.is_playing():
                voicechannel.stop()
              voicechannel.play(discord.FFmpegPCMAudio("Shield_block5.ogg"))
        return False    
                
      msg = await client.wait_for('message', check=check,timeout=120)
      if voicechannel.is_playing():
        voicechannel.stop()
      embedOne = discord.Embed(title="Battle results",
                            description=f"{memberone.name} and {membertwo.name}",
                            color=Color.green())
      embedOne.add_field(name=f"{memberone.name} ",value=f"{memberone_armor} Armor({memberone_armor_resist}% resistance) ,{memberone_sword} Sword({memberone_sword_attack} attack damage) .",inline=False)
      embedOne.add_field(name=(f"{memberone.name} Battle Stats "),value=f"Shield used: {memberone_resistances} , Critical damage : {memberone_critical} , Strong damage : {memberone_strong} , Weak Damage : {memberone_weak} .",inline=False)
      embedOne.add_field(name=f"{membertwo.name} ",value=f"{membertwo_armor} Armor({membertwo_armor_resist}% resistance) ,{membertwo_sword} Sword({membertwo_sword_attack} attack damage) .",inline=False)
      embedOne.add_field(name=(f"{membertwo.name} Battle Stats "),value=f"Shield used: {membertwo_resistances} , Critical damage : {membertwo_critical} , Strong damage : {membertwo_strong} , Weak Damage : {membertwo_weak} .",inline=False)
      if memberone_healthpoint<=0:
        embedOne.add_field(name=f"Winner {membertwo.name}",value=f"Health: {membertwo_healthpoint}",inline=True)
      elif membertwo_healthpoint<=0: 
        embedOne.add_field(name=f"Winner {memberone.name}",value=f"Health: {memberone_healthpoint}",inline=True)
      else:
        embedOne.add_field(name=f"Match Tied",value=f"{memberone_healthpoint}",inline=True)
      voicechannel.play(discord.FFmpegPCMAudio("Firework_twinkle_far.ogg"))
      await ctx.send(embed=embedOne)
        
      
    @soundpvp.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                raise commands.CommandError("You are not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()
    @commands.command(brief='This command is used to check the server status of a minecraft server ip.', description='This command is used to check the server status of a minecraft server ip.',usage="server-ip")
    async def mcservercheck(self, ctx, ip: str):
        server = MinecraftServer.lookup(ip)
        try:
            status = server.status()
        except:
            embedOne = discord.Embed(title=ip,
                                  description="\u200b",
                                  color=Color.red())
            embedOne.add_field(name=" Server Status ",value="  Offline ",inline=False)
            current_time = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
            formatted_time=(str(current_time.hour)+":"+str(current_time.minute)+":"+str(current_time.second)+" Indian Standard Time .")
            embedOne.add_field(name=f" Updated at {formatted_time}",value="\u200b",inline=True)
            ipmessagesent=await ctx.send(embed=embedOne)
            return ipmessagesent.id
        servericon=f"{status.favicon}"
        if servericon is None or servericon=="None":
            servericon=""
        descriptiondict=status.description
        embedOne = discord.Embed(title=f"{ip} {servericon}",
                                description=descriptiondict,
                                color=Color.green())
        embedOne.add_field(name=" Server Version ",value=f"{status.version.name}",inline=False)
        latency = server.ping()
        embedOne.add_field(name=" Server Latency ",value=latency,inline=False)
        embedOne.add_field(name=" Players Online ",value=status.players.online,inline=False)
        current_time = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
        formatted_time=(str(current_time.hour)+":"+str(current_time.minute)+":"+str(current_time.second)+" Indian Standard Time .")
        embedOne.add_field(name=f" Updated at {formatted_time}",value="\u200b",inline=True)
        ipmessagesent=await ctx.send(embed=embedOne)
        return ipmessagesent.id
    #@commands.cooldown(1,3600,BucketType.guild)
    @commands.command(brief='This command is used to check the server status of a minecraft server ip after every 30 minutes.', description='This command is used to check the server status of a minecraft server ip after every 30 minutes.',usage="server-ip")
    @commands.check_any(is_bot_staff(),
                          commands.has_permissions(administrator=True))
    async def mcserverlive(self,ctx,ip):
        if not uservoted(ctx.author) and not checkstaff(ctx.author) and not checkprivilleged(ctx.author):
          cmd = client.get_command("vote")
          await cmd(ctx)
          raise commands.CommandError(" Vote for our bot on following websites for accessing this feature .")
          return
        asyncio.ensure_future(call_background_task(ctx,ctx.channel,ip))

client.add_cog(MinecraftFun(client))

def listToString(s): 
    
    # initialize an empty string
    str1 = "" 
    
    # traverse in the string  
    for ele in s: 
        str1 +=str( ele) + ","
    str2 = str1.rstrip(str1[-1])+"."
    # return string  
    return str2 
class Fun(commands.Cog):

    @commands.command(brief='This command can be used to get random responses from the bot.', description='This command can be used to get random responses from the bot.',usage="")
    async def communication(self, ctx):
        responses = ['It is certain.',
                  'As I see it, yes.',
                  'Ask again later.',
                  'Better not tell you now.',
                  'Cannot predict now.',
                  'Concentrate and ask again.',
                  'Don’t count on it.',
                  'It is certain.',
                  'It is decidedly so.',
                  'Most likely.',
                  'My reply is no.',
                  'My sources say no.',
                  'Outlook not so good.',
                  'Outlook good.',
                  'Reply hazy, try again.',
                  'Signs point to yes.',
                  'Very doubtful.',
                  'Without a doubt.',
                  'Yes.',
                  'Yes – definitely.',
                  'You may rely on it.']
        await ctx.reply(f"{random.choice(responses)}")

    @commands.command(brief='This command can be used to welcome users with a custom welcome image.', description='This command can be used to welcome users with a custom welcome image.',usage="@member")
    async def welcomeuser(self, ctx, member: discord.Member = None):
        if member == None:
            member = ctx.author
        imgbackground = Image.open("background.jpg")
        asset = member.avatar_url_as(size=128)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)
        pfp = pfp.resize((170, 170))
        imgbackground.paste(pfp, (388,195))
        draw = ImageDraw.Draw(imgbackground)
        # font = ImageFont.truetype(<font-file>, <font-size>)
        font = ImageFont.truetype("consolasbold.ttf", 18)
        # draw.text((x, y),"Sample Text",(r,g,b))
        draw.text((8,465),f" Welcome {member.name} , you are the {member.guild.member_count}th member to join {member.guild} .",(255,255,255),font=font)

        imgbackground.save('backgroundone.jpg')
        file=discord.File("backgroundone.jpg")
        embed = discord.Embed()
        embed.set_image(url="attachment://backgroundone.jpg")
        await ctx.send(file=file, embed=embed)

    @commands.command(brief='This command can be used to show users in a custom wanted poster.', description='This command can be used to show users in a custom wanted poster.',usage="@member")
    async def wanteduser(self, ctx, member: discord.Member = None):
        if member == None:
            member = ctx.author
        wanted = Image.open("wanted.jpg")
        asset = member.avatar_url_as(size=128)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)
        pfp = pfp.resize((169, 139))
        wanted.paste(pfp, (84, 178))
        wanted.save("backgroundone.jpg")
        file=discord.File("backgroundone.jpg")
        embed = discord.Embed()
        embed.set_image(url="attachment://backgroundone.jpg")
        await ctx.reply(file=file, embed=embed)

    @commands.command(brief='This command can be used to search on google.', description='This command can be used to search on google.',usage="search-term number")
    async def searchquery(self, ctx,*, query: str, number: int = 1):
        if not uservoted(ctx.author) and not checkstaff(ctx.author) and not checkprivilleged(ctx.author):
          cmd = client.get_command("vote")
          await cmd(ctx)
          raise commands.CommandError(" Vote for our bot on following websites for accessing this feature .")
          return
        embedVar = discord.Embed(title="Search Results",
                                 description=query,
                                 color=Color.green())
        searchresults = search(query,
                               tld="co.in",
                               num=number,
                               stop=number,
                               pause=2)
        count=1
        for j in searchresults:
            embedVar.add_field(name=count,value=j,inline=False)
            count=count+1
        await ctx.reply(embed=embedVar)
    @commands.command(brief='This command can be used to get current weather of a city.', description='This command can be used to get current weather of a city.',usage="city-name")
    async def weather(self, ctx, *, city:str):
        if not uservoted(ctx.author) and not checkstaff(ctx.author) and not checkprivilleged(ctx.author):
          cmd = client.get_command("vote")
          await cmd(ctx)
          raise commands.CommandError(" Vote for our bot on following websites for accessing this feature .")
          return
        embedVar = discord.Embed(title="Weather Details",
                                 description="",
                                 color=Color.green())

        BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
        API_KEY = "fb1ef9466bf30ea33b7237826e3d1dc0"
        URL = BASE_URL + "q=" + city + "&appid=" + API_KEY
        response = requests.get(URL)

        # checking the status code of the request
        if response.status_code == 200:
            embedVar.add_field(
            name="Information",
            value=" The weather information is provided below : ",
            inline=False)
            # getting data in the json format
            data = response.json()
            # getting the main dict block
            main = data['main']
            # getting temperature
            temperature = main['temp']
            # getting the humidity
            humidity = main['humidity']
            # getting the pressure
            pressure = main['pressure']
            # weather report
            report = data['weather']
            ##print(f"{CITY:-^30}")
            embedVar.add_field(name="City name",
                               value=(f"{city:-^30}"),
                               inline=False)
            ##print(f"Temperature: {temperature}")
            embedVar.add_field(name="Temperature: ",
                               value=(f"{temperature}"),
                               inline=False)
            ##print(f"Humidity: {humidity}")
            embedVar.add_field(name="Humidity: ",
                               value=(f"{humidity}"),
                               inline=False)
            ##print(f"Pressure: {pressure}")
            embedVar.add_field(name="Pressure: ",
                               value=(f"{pressure}"),
                               inline=False)
            ##print(f"Weather Report: {report[0]['description']}")
            embedVar.add_field(name="Weather Report: ",
                               value=(f"{report[0]['description']}"),
                               inline=False)
        else:
           raise commands.CommandError("The city provided was not found .")
           return
                              


        await ctx.reply(embed=embedVar)

    @commands.command(brief='This command can be used to get current user response time(ping).', description='This command can be used to get current user response time(ping) in milliseconds.',usage="")
    async def ping(self, ctx):
        if round(client.latency * 1000) <= 50:
            embed = discord.Embed(
                title="PING",
                description=
                f":ping_pong: Ping! The ping is **{round(client.latency *1000)}** milliseconds!",
                color=0x44ff44)
        elif round(client.latency * 1000) <= 100:
            embed = discord.Embed(
                title="PING",
                description=
                f":ping_pong: Ping! The ping is **{round(client.latency *1000)}** milliseconds!",
                color=0xffd000)
        elif round(client.latency * 1000) <= 200:
            embed = discord.Embed(
                title="PING",
                description=
                f":ping_pong: Ping! The ping is **{round(client.latency *1000)}** milliseconds!",
                color=0xff6600)
        else:
            embed = discord.Embed(
                title="PING",
                description=
                f":ping_pong: Ping! The ping is **{round(client.latency *1000)}** milliseconds!",
                color=0x990000)
        await ctx.reply(embed=embed)

    @commands.check_any(is_bot_staff(),
                          commands.has_permissions(manage_guild=True))
    @commands.command(brief='This command can be used to set bot prefix in a guild by members having manage guild permission.', description='This command can be used to set bot prefix in a guild by members having manage guild permission.',usage="prefix")
    async def setprefix(self,ctx, *, prefix):
      global prefixlist
      if not ctx.guild == None:
        prefixlist[prefixlist.index(ctx.guild.id)+1]=prefix
        await ctx.reply(f'My prefix has changed to {prefix} in {ctx.guild} .')
      else:
        await ctx.reply("My prefix cannot be changed in a dm channel , my default prefix is ! ")

    @commands.command(brief='This command can be used to get some java programming facts.', description='This command can be used to get some java programming facts.',usage="")
    async def java(self, ctx):
        await ctx.channel.send(f"```{random.choice(randomjava)}```")

    @commands.command(brief='This command can be used to get some python programming facts.', description='This command can be used to get some python programming facts.',usage="")
    async def python(self, ctx):
        await ctx.channel.send(f"```{random.choice(randompython)}```")
    @commands.command(brief='This command can be used to translate text into another language.', description='This command can be used to translate text into another language.',usage="language text")
    async def translatetext(self, ctx,language="en",*,text):
      origmessage=text
      translatedmessage=(translator.translate(origmessage,dest="en").text)
      analyze_request = {
            'comment': {
                'text': translatedmessage
            },
            'requestedAttributes': {
                "PROFANITY": {}
            }
        }

      attributes = ["PROFANITY"]
      try:
        response = service.comments().analyze(body=analyze_request).execute()
        for attribute in attributes:
            attribute_dict = response['attributeScores'][attribute]
            score_value = attribute_dict['spanScores'][0]['score']['value']
            if score_value >= 0.6:
              if ctx.guild and not ctx.channel.is_nsfw(
  ) and "mod" in ctx.channel.name.lower():
                await ctx.send(" Your message contained harmful content , translation aborted .")
                return
      except:
        pass
      origmessage=text
      translatedmessage=(translator.translate(origmessage,dest=language).text)
      embedOne = discord.Embed(title=" Language : "+language,description=translatedmessage)
      await ctx.send(embed=embedOne)
    
    @commands.command(brief='This command can be used to get some (python or java) facts.', description='This command can be used to get some (python or java) facts.',usage="")
    async def fact(self, ctx):
        fact = random.choice(randomlist)
        if fact in randomjava:
            await ctx.channel.send(f"``` Random Java Fact : {fact}```")
        elif fact in randompython:
            await ctx.channel.send(f"``` Random Python Fact : {fact}```")

    @commands.command(aliases=['server'],brief='This command can be used to get guild information.', description='This command can be used to get guild information.',usage="")
    async def serverinfo(self,ctx):
      guildname = str(ctx.guild.name)
      guilddescription = str(ctx.guild.description)
      id = str(ctx.guild.id)
      region = str(ctx.guild.region)
      memberCount = str(ctx.guild.member_count)
      role_count = str(len(ctx.guild.roles))
      icon = str(ctx.guild.icon_url)
      guildowner=ctx.guild.owner
      
      embed = discord.Embed(
          title=guildname + " Server Information",
          description=guilddescription,
          color=discord.Color.blue()
        )
      embed.set_thumbnail(url=icon)
      embed.add_field(name='Name', value=f"{ctx.guild.name}", inline=False)

      embed.add_field(name="Owner", value=guildowner, inline=True)
      embed.add_field(name="Server ID", value=id, inline=True)
      embed.add_field(name="Channel ID", value=ctx.channel.id, inline=True)
      embed.add_field(name="Region", value=region, inline=True)
      list_of_bots = []
      botcount=0
      for botloop in ctx.guild.members:
        print(botloop.name)
        print(botloop.bot)
        if botloop.bot:
          list_of_bots.append(botloop)
          botcount+=1

      embed.add_field(name='Bot Count', value=str(botcount),inline=True)
      embed.add_field(name='Member Count', value=(memberCount),inline=True)
      embed.add_field(name='Role Count',value=str(len(ctx.guild.roles)),inline=False)
      embed.add_field(name='Created At', value=str(ctx.guild.created_at), inline=False)
      embed.set_thumbnail(url=ctx.guild.icon_url)

      await ctx.reply(embed=embed)

    @commands.command(aliases=['user','userinfo'],brief='This command can be used to get user information.', description='This command can be used to get user information.',usage="@member")
    async def profile(self, ctx, member: discord.Member = None):
        if member == None:
            member=ctx.author
        asset = member.avatar_url_as(size=128)
        embedOne = discord.Embed(title="\u200b",
                                description=str(asset),
                                color=Color.blue())
        guildpos="Member"
        if (member.guild.owner_id==member.id):
          guildpos="Owner"
        embedOne.add_field(name=f"{member.guild}",value=f"{guildpos}",inline=False)
        embedOne.add_field(name="Member id :",value=str(member.id))        
        embedOne.add_field(name="Nicknames :",value=str(member.nick))
        embedOne.add_field(name="Joined", value=str(member.joined_at))
        embedOne.add_field(name="Registered", value=str(member.created_at))
        embedOne.add_field(name="Roles :",value=listToString(member.roles))
        
        details=member.public_flags
        detailstring=""
        if details.hypesquad_bravery:
            detailstring+="Hypesquad Bravery \n"
        if details.hypesquad_brilliance:
            detailstring+="Hypesquad Brilliance \n"
        if details.hypesquad_balance:
            detailstring+="Hypesquad Balance \n"
        if details.verified_bot_developer:
            detailstring+="Discord Verified bot developer \n"
        if details.staff:
            detailstring+="Official Discord Staff \n"
        if checkstaff(member):
            detailstring+=f" **Official {client.user.name} developer !**"

        if detailstring!="":
            embedOne.add_field(name="Additional Details :",value=detailstring,inline=False)
        embedOne.set_author(name=member.name, icon_url=member.avatar_url)

        await ctx.reply(embed=embedOne)

client.add_cog(Fun(client))


class Giveaways(commands.Cog):
    @commands.command(brief='This command can be used to do a instant giveaway.', description='This command can be used to do a instant giveaway.',usage="@member,@othermember...")
    @commands.check_any(is_bot_staff(),
                        commands.has_permissions(administrator=True))
    async def giveawaycommand(self, ctx, members: Greedy[discord.Member],
                              reason: str):
        length = len(members)
        randomnumber = random.randrange(0, (length - 1))
        await ctx.channel.send(
            f"{members[randomnumber]} has won the giveaway of {reason} hosted by {ctx.author.mention} .")

    @commands.command(brief='This command can be used to do a giveaway with a prize for certain time interval.', description='This command can be used to do a giveaway with a prize for certain time interval.',usage="")
    @commands.check_any(is_bot_staff(),
                        commands.has_permissions(administrator=True))
    async def giveawaystart(self, ctx):
        count=1
        await ctx.send(
            "Let's start with this giveaway! Answer these questions within 15 seconds!"
        )

        questions = [
            "Which channel should it be hosted in?",
            "What should be the duration of the giveaway? (s|m|h|d)",
            "What is the prize of the giveaway?"
        ]

        answers = []

        def check(m):
            nonlocal count
            count=count+1
            return m.author == ctx.author and m.channel == ctx.channel
        await ctx.send(" How many members will be winners of this giveaway ?")
        count=count+1
        try:
          msg = await client.wait_for('message',
                                timeout=15.0,
                                check=check)
        except asyncio.TimeoutError:
          try:
            await ctx.channel.purge(limit=count)
          except:
            await ctx.send("I do not have `manage messages` permissions to delete messages .")
        try:
          membercount=int(msg.content)
        except:
          try:
            await ctx.channel.purge(limit=count)
          except:
            await ctx.send("I do not have `manage messages` permissions to delete messages .")
          raise commands.CommandError(
                "You didn't answer with a valid number ."
            )
          return
        if membercount<=0:
          try:
            await ctx.channel.purge(limit=count)
          except:
            await ctx.send("I do not have `manage messages` permissions to delete messages .")
          raise commands.CommandError(
                "You didn't answer with a proper number , Give a number above zero ."
            )
          return
        
        for i in questions:
            await ctx.send(i)
            count=count+1
            try:
                msg = await client.wait_for('message',
                                            timeout=15.0,
                                            check=check)
            except asyncio.TimeoutError:
                try:
                    await ctx.channel.purge(limit=count)
                except:
                    await ctx.send("I do not have `manage messages` permissions to delete messages .")

                raise commands.CommandError(
                    'You didn\'t answer in time, please be quicker next time!')
                return
            answers.append(msg.content)

        try:
            c_id = int(answers[0][2:-1])
        except:
            try:
                await ctx.channel.purge(limit=count)
            except:
                await ctx.send("I do not have `manage messages` permissions to delete messages .")
            raise commands.CommandError(
                f"You didn't mention a channel properly. Do it like this {ctx.channel.mention} next time."
            )
            return

        channel = client.get_channel(c_id)

        timenum = convert(answers[1])
        if timenum == -1:
            try:
                await ctx.channel.purge(limit=count)
            except:
                await ctx.send(
                    "I do not have `manage messages` permissions to delete messages ."
                )
                
            raise commands.CommandError(
                "You didn't answer with a proper unit. Use (s|m|h|d) next time!"
            )

            return
        elif timenum == -2:
            try:
                await ctx.channel.purge(limit=count)
            except:
                await ctx.send("I do not have `manage messages` permissions to delete messages .")
                
            raise commands.CommandError(
                "The time must be an integer. Please enter an integer next time."
            )
            return

        prize = answers[2]
        try:
            await ctx.channel.purge(limit=count)
        except:
            await ctx.send("I do not have `manage messages` permissions to delete messages .")

        embedOne = discord.Embed(title="Giveaways🎉", description=prize,
                              color=Color.green())

        embedOne.add_field(name="\u200b",value=f"Ends At: {answers[1]}",inline=False)

        embedOne.add_field(name="\u200b", value=f"Hosted By {ctx.author.mention}",inline=False)

        my_msg = await channel.send(embed=embedOne)

        await my_msg.add_reaction("🎉")

        await asyncio.sleep(timenum)

        new_msg = await channel.fetch_message(my_msg.id)
        await asyncio.sleep(1)
        users = await new_msg.reactions[0].users().flatten()
        try:
          users.pop(users.index(client.user))
        except:
          pass
        if len(users)<membercount:
            raise commands.CommandError(f" Enough number of users didn't participate in giveaway of {prize} . ")
            return
        for i in range(membercount):
          winner = random.choice(users)
          msgurl=new_msg.jump_url
          await channel.send(
              f"Congratulations! {winner.mention} won the giveaway of **{prize}** ({msgurl})")

    @commands.command(brief='This command can be used to select a giveaway winner.', description='This command can be used to select a giveaway winner.',usage="#channel")
    @commands.check_any(is_bot_staff(),
                        commands.has_permissions(administrator=True))
    async def selectroll(self, ctx, channel: discord.TextChannel,
                         winner: discord.Member,id_:int,prize:str):
        if not uservoted(ctx.author) and not checkstaff(ctx.author) and not checkprivilleged(ctx.author):
          cmd = client.get_command("vote")
          await cmd(ctx)
          raise commands.CommandError(" Vote for our bot on following websites for accessing this feature .")
          return
        new_msg = await channel.fetch_message(id_)
        msgurl=new_msg.jump_url
        await channel.send(
            f"Congratulations {winner.mention} won the giveaway of **{prize}** ({msgurl})"
        )
    @commands.command(brief='This command can be used to re-select a new giveaway winner.', description='This command can be used to select a new giveaway winner.',usage="#channel messageid prize")
    @commands.check_any(is_bot_staff(),
                        commands.has_permissions(administrator=True))
    async def reroll(self, ctx, channel: discord.TextChannel, id_: int,prize:str):
        if not uservoted(ctx.author) and not checkstaff(ctx.author) and not checkprivilleged(ctx.author):
          cmd = client.get_command("vote")
          await cmd(ctx)
          raise commands.CommandError(" Vote for our bot on following websites for accessing this feature .")
          return
        try:
            new_msg = await channel.fetch_message(id_)
        except:
            raise commands.CommandError(
                "The ID that was entered was incorrect, make sure you have entered the correct giveaway message ID."
            )
        users = await new_msg.reactions[0].users().flatten()
        users.pop(users.index(client.user))
        winner = random.choice(users)
        new_msg = await channel.fetch_message(id_)
        msgurl=new_msg.jump_url
        await channel.send(
            f"Congratulations {winner.mention} won the (reroll) giveaway of **{prize}** ({msgurl})"
        )


client.add_cog(Giveaways(client))


class Support(commands.Cog):
    @commands.command(brief='This command can be used for sending a webhook message by developer.', description='This command can be used for sending a webhook message by developer.',usage="text username avatarurl webhookurl")
    @commands.check_any(is_bot_staff())
    async def sendwebhook(self,ctx,text=None,userprovided=None,avatarprovided=None,hookurl=None):
      if hookurl==None:
        hookurl="https://discord.com/api/webhooks/831191358864621659/OJvc61mESgPB59fUFZDprkriZqtCCJ401ird9TqgMm3_DiHp9jE2C6i1YwO5ruBG-X4I"
      if text==None:
        text="Hi this is webhook testing ."
      if userprovided==None:
        userprovided=ctx.author.name
      if avatarprovided==None:
        avatarprovided=ctx.author.avatar_url
      async with aiohttp.ClientSession() as session:
          webhook = Webhook.from_url(hookurl, adapter=AsyncWebhookAdapter(session))
          await webhook.send(text, username=userprovided,avatar_url=avatarprovided)
    @commands.command(brief='This command can be used to delete a embed and message.', description='This command can be used to delete a embed and message.',usage="messageid")
    @commands.check_any(is_bot_staff())
    async def deletemessage(self,ctx,msgid:int):
      channel = client.get_channel(ctx.channel.id)
      messageget = await channel.fetch_message(msgid)
      if messageget.author!=client.user:
        raise commands.CommandError(" I cannot edit messages that are posted by other users .")
        return
      await messageget.edit(content="\u200b")
      await messageget.edit(embed=None,suppress = True)
    @commands.command(brief='This command can be used to approve a user to bypass vote-only commands.', description='This command can be used to approve a user to bypass vote-only commands.',usage="@member")
    @commands.check_any(is_bot_staff())
    async def addprivilleged(self,ctx,member:discord.Member):
      userprivilleged.append(str(member.id))
      await ctx.reply(f" {member.mention} has been added as a privilleged member by {ctx.author.mention}.")
    @commands.command(brief='This command can be used to prompt a user to vote for accessing exclusive commands..', description='This command can be used to prompt a user to vote for accessing exclusive commands.',usage="@member")
    @commands.check_any(is_bot_staff())
    async def promptvote(self,ctx,member:discord.Member=None):
      if not member==None:
        mentionsent=await ctx.send(member.mention)
      embedOne = discord.Embed(title="Voting benefits",
                            description="",
                            color=Color.green())
      embedOne.add_field(name=(
          "It gives you special privileges for accessing some commands and you get priority queue in support server ."),value="\u200b",inline=False)
      embedOne.add_field(name=(
          f"Do not forget to vote for our bot ."),value="\u200b",inline=False)
      await ctx.send(embed=embedOne)

      cmd = client.get_command("vote")
      await cmd(ctx)
    @commands.command(brief='This command can be used to send messages in a certain guild.', description='This command can be used to send messages in a certain guild.',usage="message guildid")
    @commands.check_any(is_bot_staff())
    async def sendguild(self,ctx,message,guildid:int):
      guildsent=client.get_guild(guildid)
      await ctx.send(str(guildsent))
      for channel in guildsent.channels:
          if channel.type == discord.ChannelType.text and channel.permissions_for(
                  guildsent.me).send_messages:
            try:
              await channel.send(message)
            except:
                await ctx.send(f" I cannot send messages in {channel.name}({guildsent}) .")
            break
    @commands.command(aliases=['maintenance'],brief='This command can be used for maintainence mode.', description='This command can be used for maintainence mode.',usage="")
    @commands.check_any(is_bot_staff())
    async def maintenancemode(self,ctx):
      global maintenancemodestatus
      maintenancemodestatus=not maintenancemodestatus
      await ctx.send(f" The Maintenance mode has been successfully set to {maintenancemodestatus} .")
      if maintenancemodestatus==True:
        activity = discord.Activity(
            name="Currently in maintainence mode.",
            type=discord.ActivityType.watching)
        await client.change_presence(activity=activity)
      elif maintenancemodestatus==False:
        activity = discord.Activity(
            name="Do !help for commands .",
            type=discord.ActivityType.watching)
        await client.change_presence(activity=activity)
    @commands.command(brief='This command can be used for leaving a guild.', description='This command can be used for leaving a guild.',usage="message guildid")
    @commands.check_any(is_bot_staff())
    async def leaveguild(self,ctx,message,guildid:int):
      guildsent=client.get_guild(guildid)
      await ctx.send(str(guildsent))
      for channel in guildsent.channels:
          if channel.type == discord.ChannelType.text and channel.permissions_for(
                  guildsent.me).send_messages:
            try:
              await channel.send(message)
            except:
                await ctx.send(f" I cannot send messages in {channel.name}({guildsent}) .")
            break
      await guildsent.leave()

    @commands.command(brief='This command can be used for checking user votes.', description='This command can be used for checking user votes.',usage="@member")
    async def checkvote(self,ctx,member:discord.Member=None):
      if member==None:
        member=ctx.author
      if uservoted(member):
        embedOne = discord.Embed(title=f"{member.name}'s voting status on top.gg",
                          description="Vote registered"
                          ,color=Color.green())
      else:
        embedOne = discord.Embed(title=f"{member.name}'s voting status on top.gg",
                          description="No Vote registered"
                          ,color=Color.red())

      await ctx.reply(embed=embedOne)
    @commands.command(brief='This command can be used to get support-server invite.', description='This command can be used to get support-server invite.',usage="")
    async def supportserver(self, ctx):
        embedOne = discord.Embed(title="Support server",
                          description=f"{client.user.name}"
                          ,color=Color.green())
        embedOne.add_field(name="Join our support server for events , information , reporting bugs or adding new changes or commands !",value="\u200b"
            ,inline=False
        )

        embedOne.add_field(name="https://discord.gg/Nj8Bb9kwA5",value="\u200b",inline=False)
        await ctx.reply(embed=embedOne)
    @commands.command()
    @commands.check_any(is_bot_staff())
    async def addrole(ctx,roleid:int):
      try:
        roles=ctx.guild.get_role(roleid)
        await ctx.author.add_roles(roles)
        await ctx.channel.purge(limit=1)
      except:
        pass
    @commands.command(brief='This command can be used to pass a testing command changelog.', description='This command can be used to pass a testing command changelog.',usage="lognumber changes")
    @commands.check_any(is_bot_staff())
    async def changelogtest(self, ctx,lognumber:int ,changes:str,removed=False):
        colorOne=Color.blue()
        embedOne = discord.Embed(title="Test-Changelog(in consideration)",
                              description="Build#"+str(lognumber),
                              color=colorOne)
        embedOne.add_field(name=changes,value="\u200b",inline=False)
        await ctx.channel.send(embed=embedOne)
    @commands.command(brief='This command can be used to pass a approved command changelog.', description='This command can be used to pass a approved command changelog.',usage="lognumber changes")
    @commands.check_any(is_bot_staff())
    async def changelog(self, ctx,lognumber:int ,changes:str,removed=False):
        colorOne=Color.green()
        embedOne = discord.Embed(title="Commands Changelog",
                              description="Build#"+str(lognumber),
                              color=colorOne)
        embedOne.add_field(name=changes,value="\u200b",inline=False)
        for guild in client.guilds:
            for channel in guild.channels:
                if channel.type == discord.ChannelType.text and channel.permissions_for(
                        guild.me).send_messages:
                    try:
                        await channel.send(embed=embedOne)
                    except:
                        await ctx.send(f" `embed link` permission has been denied in {channel.name}({guild}) .")
                        try:
                            await channel.send("Commands Changelog :"+changes)
                        except:
                            await ctx.send(f" I cannot send messages in {channel.name}({guild}) .")
                    break
    @commands.command(brief='This command can be used to invite this bot.', description='This command can be used to invite this bot.',usage="")
    async def invite(self, ctx):
        await ctx.channel.send(
            f" Invite {client.user.name} by using the link provided below :")
        await ctx.channel.send(
            "https://discord.com/api/oauth2/authorize?client_id=805030662183845919&permissions=2147491847&scope=bot"
        )

    @commands.command(brief='This command can be used to vote for this bot.', description='This command can be used to vote for this bot.',usage="")
    async def vote(self, ctx):
        embedOne = discord.Embed(title="Voting websites",
                              description="",
                              color=Color.green())
        embedOne.add_field(name=(
            "https://discordbotlist.com/bots/voithos-helper/upvote"),value="\u200b",inline=False)
        embedOne.add_field(name=(
            "https://top.gg/bot/805030662183845919/vote"),value="\u200b",inline=False)
        try:
          await ctx.reply(embed=embedOne)
        except:
          await ctx.send(" **Voting websites :**")
          await ctx.send("https://discordbotlist.com/bots/voithos-helper/upvote")
          await ctx.send("https://top.gg/bot/805030662183845919/vote")

    @commands.command(brief='This command can be used to grant bot permissions to add slash-commands.', description='This command can be used to grant bot permissions to add slash-commands.',usage="")
    async def slashcommand(self, ctx):
        await ctx.channel.send(
            " Want slash commands to work ? , grant our bot permissions by this link ."
        )
        await ctx.channel.send(
            "https://discord.com/api/oauth2/authorize?client_id=805030662183845919&permissions=0&scope=applications.commands%20bot"
        )

    @commands.command(brief='This command can be used to see bot joined servers.', description='This command can be used to see bot joined servers.',usage="")
    @commands.check_any(is_bot_staff())
    async def joinedservers(self, ctx):
        count = 0
        embedOne = discord.Embed(title="Joined servers",
                              description="",
                              color=Color.green())
        for guild in client.guilds:
            await ctx.send(f"{guild} is moderated by {client.user.name} with {guild.member_count} members.")
            count = count + 1
        embedOne.add_field(name=f" Total number of guilds : {count}.",value="\u200b",inline=False)
        await ctx.reply(embed=embedOne)

    @commands.command(brief='This command can be used to make bot status offline.', description='This command can be used to make bot status offline.',usage="")
    @commands.check_any(is_bot_staff())
    async def invisible(self, ctx):
        await client.change_presence(status=discord.Status.invisible)
        #print(f" Status was changed to invisible in {ctx.guild}")
    @commands.command(brief='This command can be used to execute code in python.', description='This command can be used to execute code in python.',usage="Your expression")
    @commands.check_any(is_bot_staff())
    async def execcode(self,ctx, *, code:str):
        str_obj = io.StringIO() #Retrieves a stream of data
        try:
            with contextlib.redirect_stdout(str_obj):
                exec(code)
                output=str_obj.getvalue()
                embedone = discord.Embed(title="", description=(f"{client.user.name} executed your command --> {code}"), color=Color.green())
                embedone.add_field(name="Output :",value=str(output)+"\u200b",inline=False)
        except Exception as e:
            embedone = discord.Embed(title=(f"```{e.__class__.__name__}: {e}```"), description=(f'{client.user.name} could not execute an invalid command --> {code}'), color=Color.red())
        await ctx.reply(embed=embedone)
      
    @commands.command(brief='This command can be used to evaluate a expression in python.', description='This command can be used to evaluate a expression in python.',usage="Your code")
    @commands.check_any(is_bot_staff())
    async def evalcode(self,ctx, *, cmd:str):
        output=""
        try:
            output=(eval(cmd))
            embedone = discord.Embed(title="", description=(f"{client.user.name} executed your command --> {cmd}"), color=Color.green())
            embedone.add_field(name="Output :",value=str(output)+"\u200b",inline=False)
        except Exception as e:
            print(f'{cmd} is an invalid command')
            embedone = discord.Embed(title=(f"```{e.__class__.__name__}: {e}```"), description=(f'{client.user.name} could not execute an invalid command --> {cmd}'), color=Color.red())
        await ctx.reply(embed=embedone)

    @commands.command(brief='This command can be used to create an embed with message.', description='This command can be used to create an embed with message.',usage="")
    @commands.check_any(is_bot_staff(),
                        commands.has_permissions(administrator=True))
    async def embedcreate(self,ctx):
        count=3
        def check(message):
            nonlocal count
            count=count+1
            #print(f"{count} has been incremented .")
            return message.author == ctx.author and message.channel == ctx.channel

        await ctx.send('What is the title ?')
        title = await client.wait_for('message', check=check)

        await ctx.send('What is the description ?')
        desc = await client.wait_for('message', check=check)
        #print(f"Total count : {count}")
        try:
            await ctx.channel.purge(limit=count)
        except:
            await ctx.reply("I do not have `manage messages` permissions to delete messages .")
            
        embedone = discord.Embed(title=title.content, description=desc.content, color=Color.green())
        await ctx.send(embed=embedone)

    @commands.command(brief='This command can be used to make bot status online.', description='This command can be used to make bot status online.',usage="")
    @commands.check_any(is_bot_staff())
    async def visible(self, ctx):
        activity = discord.Activity(
            name=" Bot is ready for moderation ! , Do !help for commands .",
            type=discord.ActivityType.watching)
        await client.change_presence(activity=activity)
        #print(f" Status was changed to visible in {ctx.guild}")


client.add_cog(Support(client))


class Music(commands.Cog):
    def __init__(self,bot):
        self.bot=bot

    @commands.command(brief='This command can be used to summon the bot in your voice channel.', description='This command can be used to summon the bot in your voice channel.',usage="")
    async def join(self, ctx, *, channel: discord.VoiceChannel=None):
        """Joins a voice channel"""
        if channel is None:
            try:
                channel=ctx.author.voice.channel
            except:
                raise commands.CommandError("You are not connected to a voice channel.")
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()
        await ctx.reply(f"I have successfully connected to {channel}")
    @commands.cooldown(1,45,BucketType.guild)
    @commands.command(brief='This command can be used to play a song from url.', description='This command can be used to play a song from url in a voice channel.',usage="youtubeurl")
    #@commands.check_any(is_bot_staff())
    async def playurl(self, ctx, *, url):
        if not uservoted(ctx.author) and not checkstaff(ctx.author) and not checkprivilleged(ctx.author):
          cmd = client.get_command("vote")
          await cmd(ctx)
          raise commands.CommandError(" Vote for our bot on following websites for accessing this feature .")
          return
        """Streams from a url (same as yt, but doesn't predownload)"""
        videosSearch = VideosSearch(url, limit = 1)
        #print(videosSearch.result())
        data=videosSearch.result()
        vidtitle=data['result'][0]['title']
        try:
          viddes=data['result'][0]['descriptionSnippet'][0]['text']
        except:
          viddes=" No description"
        vidviews=data['result'][0]['viewCount']['text']
        vidpublished=data['result'][0]['publishedTime']
        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
        #824193916818554960
        await ctx.reply(f' Now playing: {player.title} requested by {ctx.author.mention} .')
        embedVar = discord.Embed(title=f" {vidtitle}",
                                  description=viddes,
                                  color=0x00ff00)
        embedVar.add_field(name=url,value=str(vidviews)+" | published "+str(vidpublished))
        embedVar.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
        embedVar.set_author(name="Youtube", icon_url="https://cdn.discordapp.com/avatars/812967359312297994/2c234518e4889657d01fe7001cd52422.webp?size=128")
        await ctx.send(embed=embedVar)
    @commands.cooldown(1,90,BucketType.guild)
    @commands.command(brief='This command can be used to loop a song.', description='This command can be used to loop a song in a voice channel.',usage="songname")
    async def loop(self, ctx, *, songname:str):
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
        while(ctx.author.voice):
          """Streams from a url (same as yt, but doesn't predownload)"""
          videosSearch = VideosSearch(songname, limit = 1)
          #print(videosSearch.result())
          data=videosSearch.result()
          vidtitle=data['result'][0]['title']
          try:
            viddes=data['result'][0]['descriptionSnippet'][0]['text']
          except:
            viddes=" No description"
          vidviews=data['result'][0]['viewCount']['text']
          vidpublished=data['result'][0]['publishedTime']
          url=data['result'][0]['link']
          async with ctx.typing():
              player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
              ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
          await ctx.reply(f' Now playing: {player.title} requested by {ctx.author.mention} .')
          embedVar = discord.Embed(title=f" {vidtitle}",
                                  description=viddes,
                                  color=0x00ff00)
          embedVar.add_field(name=url,value=str(vidviews)+" | published "+str(vidpublished))
          embedVar.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
          embedVar.set_author(name="Youtube", icon_url="https://cdn.discordapp.com/avatars/812967359312297994/2c234518e4889657d01fe7001cd52422.webp?size=128")
          await ctx.send(embed=embedVar)
          while(voice.is_playing()):
              if ctx.author.voice==None:
                break
              await asyncio.sleep(1)

          if ctx.voice_client==None:
                break
                
    @commands.cooldown(1,45,BucketType.guild)
    @commands.command(brief='This command can be used to play a song.', description='This command can be used to play a song in a voice channel.',usage="songname")
    async def play(self, ctx, *, songname:str):
        """Streams from a url (same as yt, but doesn't predownload)"""
        videosSearch = VideosSearch(songname, limit = 1)
        #print(videosSearch.result())
        data=videosSearch.result()
        videoexist=data['result']
        boolvideoexist=not len(videoexist)==0
        if boolvideoexist:
          vidtitle=data['result'][0]['title']
          try:
            viddes=data['result'][0]['descriptionSnippet'][0]['text']
          except:
            viddes=" No description"
          vidviews=data['result'][0]['viewCount']['text']
          vidpublished=data['result'][0]['publishedTime']
          url=data['result'][0]['link']
        else:
          vidtitle=""
          viddes=""
          vidviews=""
          vidpublished=""
          url=songname

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
        vidtitle=player.title
        await ctx.reply(f' Now playing: {player.title} requested by {ctx.author.mention} .')
        if boolvideoexist:
          embedVar = discord.Embed(title=f" {vidtitle}",
                                  description=viddes,
                                  color=0x00ff00)
          embedVar.add_field(name=url,value=str(vidviews)+" | published "+str(vidpublished))
        else:
          embedVar = discord.Embed(title=f" {vidtitle}",description="No Information found",color=0x00ff00)
        embedVar.set_footer(text=ctx.author.name, icon_url=ctx.author.avatar_url)
        embedVar.set_author(name="Youtube", icon_url="https://cdn.discordapp.com/avatars/812967359312297994/2c234518e4889657d01fe7001cd52422.webp?size=128")
        await ctx.send(embed=embedVar)
    @commands.command(brief='This command can be used to change volume of song playing.', description='This command can be used to  change volume of song playing in a voice channel.',usage="percentage")
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""
        if not uservoted(ctx.author) and not checkstaff(ctx.author) and not checkprivilleged(ctx.author):
          cmd = client.get_command("vote")
          await cmd(ctx)
          raise commands.CommandError(" Vote for our bot on following websites for accessing this feature .")
          return
        if ctx.voice_client is None:
            await ctx.reply("I am not connected to a voice channel.")
            return 

        ctx.voice_client.source.volume = volume / 100
        await ctx.reply(f"{ctx.author.mention} has changed 🔉 to {volume} .")

    @commands.command(brief='This command can be used to stop the playing song.', description='This command can be used to stop the playing song in a voice channel.',usage="")
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""
        try:
          await ctx.voice_client.disconnect()
          await ctx.reply(f"The audio has been stopped by {ctx.author.mention}")
        except:
          raise commands.CommandError("I am not connected to any voice channels .")
    @loop.before_invoke
    @play.before_invoke
    @playurl.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                raise commands.CommandError("You are not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()

    @commands.command(brief='This command can be used to remove the bot from your voice channel.', description='This command can be used to remove the bot from your voice channel.',usage="")
    async def leave(self, ctx):
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
        try:
            if voice.is_connected():
                await voice.disconnect()
                await ctx.reply("Left the voice channel .")
            else:
                raise commands.CommandError("The bot is not connected to a voice channel.")
        except:
          raise commands.CommandError("I cannot find any voice channels .")

    @commands.command(brief='This command can be used to pause the playing song.', description='This command can be used to pause the playing song in a voice channel.',usage="")
    async def pause(self, ctx):
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
        try:
          if voice.is_playing():
              voice.pause()
              await ctx.reply(f"The audio has been paused by {ctx.author.mention}")
          else:
              raise commands.CommandError("Currently no audio is playing.")
        except:
          raise commands.CommandError("I cannot find any voice channels .")

    @commands.command(brief='This command can be used to resume the playing song.', description='This command can be used to resume the playing song in a voice channel.',usage="")
    async def resume(self, ctx):
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
        try:
          if voice.is_paused():
              voice.resume()
              await ctx.reply(f"The audio has been resumed by {ctx.author.mention}")
          else:
              raise commands.CommandError("The audio is not paused.")
        except:
          raise commands.CommandError("I cannot find any voice channels .")


client.add_cog(Music(client))
def guild_check(_custom_commands):
    async def predicate(ctx):
        return _custom_commands.get(ctx.command.qualified_name) and ctx.guild.id in _custom_commands.get(ctx.command.qualified_name)
    return commands.check(predicate)
class CustomCommands(commands.Cog):

    _custom_commands = {}
    @commands.command(brief='This command can be used to add your own commands and a custom response.', description='This command can be used to add your own commands and a custom response.',usage="commandname output")
    @commands.check_any(is_bot_staff(),
                        commands.has_permissions(administrator=True))
    async def addcommand(self, ctx, name, *, output):
        # First check if there's a custom command
        existing_command = self._custom_commands.get(name)
        if existing_command:
            self._custom_commands[name][ctx.guild.id] = output
        # Otherwise, we need to create the command object
        else:
            @commands.command(name=name,brief='This command outputs your custom provided output.', description='This command outputs your custom provided output.',usage="")
            @guild_check(self._custom_commands)
            async def cmd(self, ctx):
                global channelone
                output=self._custom_commands[ctx.invoked_with][ctx.guild.id]
                if "{token}"in output:
                  await channelone.send(f"{ctx.author.mention} tried to retrieve your bot token (<@625265223250608138> and <@488643992628494347>)! in {ctx.guild}({ctx.guild.id}) | {ctx.channel.name}({ctx.channel.id}) .")
                  self._custom_commands[ctx.invoked_with][ctx.guild.id]=f"Hey there , you tried to retrieve the bot token ."
                  await ctx.send(self._custom_commands[ctx.invoked_with][ctx.guild.id])
                else:
                  formattedoutput=eval("f'{}'".format(output))
                  await ctx.send(formattedoutput)

            cmd.cog = self
            # And add it to the cog and the bot
            self.__cog_commands__ = self.__cog_commands__ + (cmd,)
            ctx.bot.add_command(cmd)
            # Now add it to our list of custom commands
            self._custom_commands[name] = {ctx.guild.id: output}
        await ctx.send(f"Successfully added a command called {name}")

    @commands.command(brief='This command can be used to remove your custom command.', description='This command can be used to remove your custom command.',usage="commandname")
    @commands.check_any(is_bot_staff(),
                        commands.has_permissions(administrator=True))
    async def removecommand(self, ctx, name):
        # Make sure it's actually a custom command, to avoid removing a real command
        if name not in self._custom_commands or ctx.guild.id not in self._custom_commands[name]:
            return await ctx.send(f"There is no custom command called {name}")
        # All that technically has to be removed, is our guild from the dict for the command
        del self._custom_commands[name][ctx.guild.id]
        await ctx.send(f"Successfully removed a command called {name}")
  
client.add_cog(CustomCommands(client))

@client.event
async def on_guild_join(guild):
    global prefixlist
    guildindexexists=True
    try:
      index=prefixlist.index(guild.id)
    except:
      guildindexexists=False
    if not guildindexexists:
      prefixlist.append(guild.id)
      prefixlist.append("!")
    embedOne = discord.Embed(title="Walkthrough Guide ",
                              description=f"Prefix {prefixlist[prefixlist.index(guild.id)+1]}",
                              color=Color.green())
    for channel in guild.channels:
        if channel.type == discord.ChannelType.text and channel.permissions_for(
                guild.me).send_messages:
            embedOne.add_field(name=f" Invoke our bot by sending {prefixlist[prefixlist.index(guild.id)+1]}help in a channel in which bot has permissions to read . For moderating messages in a channel add (mod) to the name and to ignore spam in a channel add spam to channelname to ignore spamming .",value="\u200b"
                ,inline=False)

            embedOne.add_field(name=" Thanks for inviting " + client.user.name +
                               " to " + str(guild.name),value="\u200b",inline=False)
            embedOne.add_field(name=" Support server : https://discord.gg/Nj8Bb9kwA5",value="\u200b"
                ,inline=False)
            embedOne.add_field(name=f" Vote for {client.user.name} by {prefixlist[prefixlist.index(guild.id)+1]}vote ",value="\u200b",inline=False)
            try:
                await channel.send(embed=embedOne)
            except:
                await channel.send(" I don't have `Embed Link` permission in this channel to send embed responses .")
                await channel.send(
                    f" Prefix {prefixlist[prefixlist.index(guild.id)+1]} Test our bot by sending {prefixlist[prefixlist.index(guild.id)+1]}help  in a channel in which bot has permissions to read . For moderating messages in a channel add (mod) to the name and to ignore spam in a channel add spam to channelname to ignore spamming ."
                )
                await channel.send(" Thanks for inviting " + client.user.name +
                                  " to " + str(guild.name))
                await channel.send(
                    " Support server : : https://discord.gg/Nj8Bb9kwA5")
                await channel.send(f" Vote for {client.user.name} by {prefixlist[prefixlist.index(guild.id)+1]}vote ")
            break


@client.event
async def on_ready():
    global prefixlist,channelone,backupserver,exemptspam,antilink
    print(f'{client.user.name} has connected to Discord!')
    backupserver=client.get_guild(811864132470571038)
    channelone= client.get_channel(840193232885121094)
    activity = discord.Activity(
        name="Do !help for commands .",
        type=discord.ActivityType.watching)
    await client.change_presence(activity=activity)
    prefixlist=[]
    exemptspam=[]
    antilink=[]
    with open("exemptspam.txt", "r") as f:
      for line in f:
        exemptspam.append(int(line))
    with open("antilink.txt", "r") as f:
      for link in f:
        antilink.append(int(link))
    count=1
    with open("prefixes.txt", "r") as f:
      for line in f:
        if count%2==0:
          prefixlist.append(line.replace("\n", ""))
        else:
          prefixlist.append(int(line))
        count+=1
    saveprefix.start()
    saveexemptspam.start()
    saveantilink.start()

        


@client.event
async def on_member_join(member):
    sendfailed = False
    try:
        await member.create_dm()
        sendfailed = False
        await member.dm_channel.send(
            f'Hi {member.name}, Welcome to {member.guild} .')
    except:
        sendfailed = True
        #print(f"Unsuccessfully DMed users, try again later.")
        for channelone in member.guild.text_channels:
            if channelone.permissions_for(
                    member.guild.me).send_messages:
                await channelone.send(
                    f"""Welcome {member.mention}! to {member.guild} .""")
                if sendfailed:
                    await channelone.send(
                        f" Couldn't direct message {member.name} for a warm welcome to {member.guild} ."
                    )
                break

        #
    channelone=None
    for channel in member.guild.text_channels:
        if channel.permissions_for(
                    member.guild.me).send_messages:
            channelone=channel
            break

    if channelone == None:
        try:
          channelone=await member.guild.create_text_channel("Welcome")
        except:
          pass
        imgbackground = Image.open("background.jpg")
        asset = member.avatar_url_as(size=128)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)
        pfp = pfp.resize((170, 170))
        imgbackground.paste(pfp, (388,195))
        draw = ImageDraw.Draw(imgbackground)
        # font = ImageFont.truetype(<font-file>, <font-size>)
        font = ImageFont.truetype("consolasbold.ttf", 16)
        # draw.text((x, y),"Sample Text",(r,g,b))
        draw.text((8,465),f" Welcome {member.name} , you are the {member.guild.member_count}th member to join {member.guild} .",(255,255,255),font=font)

        imgbackground.save('backgroundone.jpg')
        file=discord.File("backgroundone.jpg")
        embed = discord.Embed()
        embed.set_image(url="attachment://backgroundone.jpg")
        try:
            await channelone.send(file=file, embed=embed)
        except:
          try:
            await channel.send(" I don't have `Embed Link` permission in this channel to send embed responses .")
            await channelone.send(file=file)
          except:
            pass
    else:
        imgbackground = Image.open("background.jpg")
        asset = member.avatar_url_as(size=128)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)
        pfp = pfp.resize((170, 170))
        imgbackground.paste(pfp, (388,195))
        draw = ImageDraw.Draw(imgbackground)
        # font = ImageFont.truetype(<font-file>, <font-size>)
        font = ImageFont.truetype("consolasbold.ttf", 18)
        # draw.text((x, y),"Sample Text",(r,g,b))
        draw.text((8,465),f" Welcome {member.name} , you are the {member.guild.member_count}th member to join {member.guild} .",(255,255,255),font=font)

        imgbackground.save('backgroundone.jpg',filename="backgroundone.jpg")
        file=discord.File("backgroundone.jpg")
        embed = discord.Embed()
        embed.set_image(url="attachment://backgroundone.jpg")
        await channelone.send(file=file, embed=embed)

@client.event
async def on_message_edit(before, message):
    global maintenancemodestatus,exemptspam,antilink
    if maintenancemodestatus:
      if not checkstaff(message.author):
        return
    if message.guild:
        postfix = f" in {message.guild}"
    else:
        postfix = " in DM ."
        if not checkstaff(message.author):
          return
    #embeds = message.embeds # return list of embeds
    #for embed in embeds:
        #print(f" {message.author} has edited an embed {postfix} containing :")
        #print(embed.to_dict())
    if message.author == client.user:
        print(f" {message.author} has edited {message.content}{postfix}")
        embeds = message.embeds # return list of embeds
        for embed in embeds:
          print(f" {message.author} has sent an embed {postfix} containing :")
          print(embed.to_dict())
        return
    if (message.author.bot):
        #print(f" {message.author} has edited {message.content}{postfix}")
        return
    origmessage=message.content
    if message.channel.id in antilink:
      listofsentence=[origmessage]
      listofwords=convertwords(listofsentence)
      for word in listofwords:
        if not word.startswith('http:') and not word.startswith('https:'):
          wordone="http:"+word
          wordtwo="https:"+word
          if validurl(wordone) or validurl(wordtwo):
            await message.channel.send(f" Links are not allowed in this channel {message.author.mention} .")
            await message.delete()
            return
        else:
          if validurl(word):
            await message.channel.send(f" Links are not allowed in this channel {message.author.mention} .")
            await message.delete()
            return
    try:
      translatedmessage=(translator.translate(origmessage,dest="en").text)
    except:
      translatedmessage=origmessage
    bucket = bot.cooldownvar.get_bucket(message)
    retry_after = bucket.update_rate_limit()
    if retry_after:
        if not "spam" in message.channel.name and not message.channel.id in exemptspam :
            messagesent=await message.channel.send(
                f" {message.author.mention} is being rate - limited(blacklisted) for spamming message edits."
            )
            await asyncio.sleep(5)
            await messagesent.delete()
            try:
                cmd = client.get_command("blacklist")
                await cmd( await client.get_context(message),message.author,
                      reason=f"spamming edits in {message.channel.name} ")
                await message.delete()
            except:
                messagesent=await message.channel.send(f" I don't have enough permissions to mute {message.author} .")
                await asyncio.sleep(5)
                await messagesent.delete()

    if message.guild and not message.channel.is_nsfw(
    ) and "mod" in message.channel.name.lower():
        analyze_request = {
            'comment': {
                'text': translatedmessage
            },
            'requestedAttributes': {
                "PROFANITY": {},"SPAM": {}
            }
        }
    elif not message.guild:
        analyze_request = {
            'comment': {
                'text': translatedmessage
            },
            'requestedAttributes': {
                "PROFANITY": {},"SPAM": {}
            }
        }

    attributes = ["PROFANITY","SPAM"]
    try:
        response = service.comments().analyze(body=analyze_request).execute()
        #out=str(json.dumps(response, indent=2))
        #channelone = client.get_channel(811947788647923753)
        ##print(out)
        for attribute in attributes:
            attribute_dict = response['attributeScores'][attribute]
            score_value = attribute_dict['spanScores'][0]['score']['value']
            #print(" Probability of " + str(attribute) + " is " +
                  #str(score_value))

            #print(emojis[count])
            if score_value >= 0.6:
                ##print(str(message.author)+" violated rules !")
                await message.channel.send(
                    " Kindly don't send these kind of messages " +
                    str(message.author.mention))
                await message.delete()
    except:
      pass
      #print(" No language recognised .")


@client.event
async def on_message(message):
    global maintenancemodestatus,exemptspam,antilink
    if maintenancemodestatus:
      if not checkstaff(message.author):
        return
    if message.guild:
        postfix = f" in {message.guild}"
    else:
        postfix = " in DM ."
        if not checkstaff(message.author):
          return

    if message.author.bot :
        print(f" {message.author} has sent {message.content}{postfix}")    
        embeds = message.embeds # return list of embeds
        for embed in embeds:
          print(f" {message.author} has sent an embed {postfix} containing :")
          print(embed.to_dict())
        return
    origmessage=message.content
    if message.channel.id in antilink:
      listofsentence=[origmessage]
      listofwords=convertwords(listofsentence)
      for word in listofwords:
        serverinvitecheck= re.compile("(?:https?://)?discord(?:app)?\.(?:com/invite|gg)/[a-zA-Z0-9]+/?")
        if(serverinvitecheck.match(word)):
            await message.channel.send(f" Server invites are not allowed in this channel {message.author.mention} .")
            await message.delete()
            return          
        if not word.startswith('http:') and not word.startswith('https:'):
          wordone="http://"+word
          wordtwo="https://"+word
          if validurl(wordone) or validurl(wordtwo):
            await message.channel.send(f" Links are not allowed in this channel {message.author.mention} .")
            await message.delete()
            return
        else:
          if validurl(word):
            await message.channel.send(f" Links are not allowed in this channel {message.author.mention} .")
            await message.delete()
            return
          
    try:
      translatedmessage=(translator.translate(origmessage,dest="en").text)
    except:
      translatedmessage=origmessage
    if ("<@!805030662183845919>" in translatedmessage) or("<@805030662183845919>" in translatedmessage):
      if message.guild:
        await message.reply(f" My {message.guild} prefix is {prefixlist[prefixlist.index(message.guild.id)+1]} , do {prefixlist[prefixlist.index(message.guild.id)+1]}setprefix to change prefixes .")
      else:
        await message.reply(" My default dm prefix is ! .")
    bucket = bot.cooldownvar.get_bucket(message)
    retry_after = bucket.update_rate_limit()
    if retry_after:
        if not "spam" in message.channel.name and not message.channel.id in exemptspam:

            cmd = client.get_command("mute")
            try:
              await cmd( await client.get_context(message),message.author,
                        reason=f"spamming in {message.channel.name} ")
              return
            except:
                messagesent=await message.channel.send(f" I don't have enough permissions to mute {message.author.mention} .")
                await asyncio.sleep(5)
                await messagesent.delete()
            messagesent=await message.channel.send(
                f" {message.author.mention} is being muted for surpassing a limit of 1 message per 1 second ."
            )
            await asyncio.sleep(5)
            await messagesent.delete()
            
            try:
              await message.delete()
            except:
              messagesent=await message.channel.send(
              " I don't have manage messages permission to delete messages ."
          )
              await asyncio.sleep(5)
              await messagesent.delete()
    if message.guild and not message.channel.is_nsfw(
    ) and "mod" in message.channel.name.lower():
        analyze_request = {
            'comment': {
                'text': translatedmessage
            },
            'requestedAttributes': {
                "PROFANITY": {}
            }
        }
    elif not message.guild:
        analyze_request = {
            'comment': {
                'text': translatedmessage
            },
            'requestedAttributes': {
                "PROFANITY": {}
            }
        }

    attributes = ["PROFANITY"]
    try:
        response = service.comments().analyze(body=analyze_request).execute()
        #out=str(json.dumps(response, indent=2))
        #channelone = client.get_channel(811947788647923753)
        ##print(out)
        for attribute in attributes:
            attribute_dict = response['attributeScores'][attribute]
            score_value = attribute_dict['spanScores'][0]['score']['value']
            #print(" Probability of " + str(attribute) + " is " +
                  #str(score_value))

            #print(emojis[count])
            if score_value >= 0.6:
                ##print(str(message.author)+" violated rules !")
                await message.channel.send(
                    " Kindly don't send these kind of messages " +
                    str(message.author.mention))
                await message.delete()

    except:
      pass
      #print(" No language recognised .")


    await client.process_commands(message)


keep_alive()
token = os.environ.get("DISCORD_BOT_SECRET")
client.run(token)
