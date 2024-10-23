import discord
from discord import Embed
from discord import utils
from discord.ui import Button,View
from itertools import cycle
import redditeasy
import os
from os import system
from io import BytesIO
from PIL import Image 
import asyncio
import random
import json
import youtube_dl
import requests
from requests import get
from datetime import datetime as dt
from typing import Optional
from discord.ext import tasks,commands
from discord.ext.commands import Bot
from discord.utils import get
from keep_alive import keep_alive

romeo_juliet = requests.get("https://d1csarkz8obe9u.cloudfront.net/posterpreviews/blank-wanted-poster-template-design-37a9a451cb794713d8bba77bd3c0ca6f_screen.jpg?ts=1636980305")

status = cycle(['Helping server','Ping for prefix'])

def get_prefix(bot,message):

    with open("prefixes.json", "r") as f:
       prefixes = json.load(f)

    return prefixes[str(message.guild.id)]


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(case_insensitive=True,command_prefix=get_prefix,intents=intents)
bot.remove_command("help")

@bot.event
async def on_guild_join(guild):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = "d!"

    with open("prefixes.json", "w") as f:
        json.dump(prefixes,f)

    with open("mute_role.json", "r") as f:
        mute_is_role = json.load(f)

    mute_is_role[str(guild.id)] = "123"

    with open("mute_role.json", "w") as f:
        json.dump(mute_is_role,f)

    with open("unmute_role.json", "r") as f:
        unmute_is_role = json.load(f)

    unmute_is_role[str(guild.id)] = "321"

    with open("unmute_role.json", "w") as f:
        json.dump(unmute_is_role,f)

@bot.command(aliases=['sp','cp','changeprefix'])
@commands.has_any_role("doge","Doge","DOGE") 
async def setprefix(ctx, prefix):

    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open("prefixes.json", "w") as f:
        json.dump(prefixes,f)    

    await ctx.send(f"The prefix was changed to {prefix}")

@bot.command()
async def test1(ctx):
  with open("mute_role.json", "r") as f:
                mute_is_role = json.load(f)

                muteid = mute_is_role[str(ctx.guild.id)] 

                await ctx.channel.send(f"My mute id for this server is {muteid}")
  with open("unmute_role.json", "r") as f:
                unmute_is_role = json.load(f)

                unmuteid = unmute_is_role[str(ctx.guild.id)] 

                await ctx.channel.send(f"My unmute id for this server is {unmuteid}")


@bot.event
async def on_ready():
  print('on')
  change_status.start()

@tasks.loop(seconds=10)
async def change_status():
  await bot.change_presence(status=discord.Status.idle,activity=discord.Streaming(name=(next(status)), url='https://www.youtube.com/watch?v=iik25wqIuFo'))

@bot.group(invoke_without_command=True,aliases=["h",'COMMANDSINFO','CI','cmdi','commands','command','CMD'])
async def help (ctx):
  em=discord.Embed(title= "Commands",description="Use d!help {command} for extended information on a command.",color=ctx.author.color)
  em.add_field(name ="Moderation",value="Mute | Unmute | role | clean | SetPrefix",inline=False)
  if ctx.guild.id==941357999132409956:
   em.add_field(name ="Server specific",value="Permit | Autospawn | Boost ",inline=False)
  em.add_field(name ="Basic",value="Remind | UserInfo",inline=False)
  em.add_field(name ="Fun",value=" TicTacToe | Wanted | Meme",inline=False)
  em.set_footer(text="NOTE: If value if enclosed in '{}' it is optional and if it is enclosed in '<>' it is mandatory")
  em.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
  await ctx.send(embed=em)
  
@help.command(aliases=['m','mu','mut'])
async def mute(ctx):
  em = discord.Embed(title ="Mute",description="This command helps an 'ADMINISTRATOR' to mute a specified user",color=ctx.author.color)
  em.add_field(name ="**SYNTAX**",value=f"d! @<mention> || d!m @<mention>") 
  em.set_footer(text="NOTE: If value if enclosed in '[]' it is optional and if it is enclosed in '<>' it is mandatory")
  em.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
  await ctx.send(embed=em)

@help.command(aliases=['sp','cp','changeprefix'])
async def setprefix(ctx):
  em = discord.Embed(title ="Set Prefix",description="This command helps an 'ADMINISTRATOR' to change the prefix of the bot",color=ctx.author.color)
  em.add_field(name ="**SYNTAX**",value="doge setprefix <prefix> || d!sp <prefix>") 
  em.set_footer(text="NOTE: If value if enclosed in '{}' it is optional and if it is enclosed in '<>' it is mandatory")
  em.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
  await ctx.send(embed=em)


@help.command(aliases=['um','unm'])
async def unmute(ctx):
  em = discord.Embed(title ="Unmute",description="This command helps an 'ADMINISTRATOR' to unmute a specified user",color=ctx.author.color)
  em.add_field(name ="**SYNTAX**",value="doge unmute @<mention> || d!um @<mention>") 
  em.set_footer(text="NOTE: If value if enclosed in '{}' it is optional and if it is enclosed in '<>' it is mandatory")
  em.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
  await ctx.send(embed=em)


@help.command()
async def permit(ctx):
  if ctx.guild.id==941357999132409956:
   em = discord.Embed(title ="Permit",description="This command helps an 'ADMINISTRATOR' to permit a specified user",color=ctx.author.color)
   em.add_field(name ="**SYNTAX**",value="doge permit @<mention> <Time in minutes> || d!rem @<mention> <Time in minutes>") 
   em.set_footer(text="NOTE: If value if enclosed in '{}' it is optional and if it is enclosed in '<>' it is mandatory")
   em.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
   await ctx.send(embed=em)

@help.command(aliases=['as','ausp'])
async def AUTOSPAWN(ctx):
  if ctx.guild.id==941357999132409956:
   em = discord.Embed(title ="Autospawn",description="This command helps a user to trigger the autospawner",color=ctx.author.color)
   em.add_field(name ="**SYNTAX**",value="doge autospawn  || d!as ") 
   em.set_footer(text="NOTE: If value if enclosed in '{}' it is optional and if it is enclosed in '<>' it is mandatory")
   em.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
   await ctx.send(embed=em)


@help.command(aliases=['b','pokeboost','pb'])
async def BOOST(ctx):
  if ctx.guild.id==941357999132409956:
   em = discord.Embed(title ="Boost",description="This command helps a user to re-trigger the autospawner",color=ctx.author.color)
   em.add_field(name ="**SYNTAX**",value="doge boost  || d!b ") 
   em.set_footer(text="NOTE: If value if enclosed in '{}' it is optional and if it is enclosed in '<>' it is mandatory")
   em.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
   await ctx.send(embed=em)
   

@help.command(aliases=['r','ro','rol'])
async def role(ctx):
  em = discord.Embed(title ="Role",description='This command helps an "ADMINISTRATOR" to give role to specified user',color=ctx.author.color)
  em.add_field(name ="**SYNTAX**",value="doge role @<mention> @<role> || d!r @<mention> @<role>") 
  em.set_footer(text="NOTE: If value if enclosed in '{}' it is optional and if it is enclosed in '<>' it is mandatory")
  em.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
  await ctx.send(embed=em)

@help.command(aliases=['c','cl','cle','clea','PURGE','PU','pur','PURG'])
async def clean(ctx):
  em = discord.Embed(title ="Clean",description='This command helps an "ADMINISTRATOR" to clean the chat',color=ctx.author.color)
  em.add_field(name ="**SYNTAX**",value="doge clean <number of words> || d!c <number of words>") 
  em.set_footer(text="NOTE: If value if enclosed in '{}' it is optional and if it is enclosed in '<>' it is mandatory")
  em.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
  await ctx.send(embed=em)


@help.command(aliases=['mod','moder'])
async def MODERATION(ctx):
  em = discord.Embed(title ="Moderation",description='This command category usually used by an "ADMINISTRATOR" to control the server',color=ctx.author.color)
  em.add_field(name ="**CATEGORY COMMANDS**",value="Mute | Unmute | Role | Clean  ") 
  em.set_footer(text="NOTE: If value if enclosed in '{}' it is optional and if it is enclosed in '<>' it is mandatory")
  em.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
  await ctx.send(embed=em)


@help.command(aliases=['serspe','serverspec'])
async def Serverspecific(ctx):
  if ctx.guild.id==941357999132409956:
   em = discord.Embed(title ="Server Specific",description=f'This command category usually used in {ctx.guild.name}',color=ctx.author.color)
   em.add_field(name ="**CATEGORY COMMANDS**",value="Permit | Boost | Autospawn ") 
   em.set_footer(text="NOTE: If value if enclosed in '{}' it is optional and if it is enclosed in '<>' it is mandatory")
   em.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
   await ctx.send(embed=em)

@help.command(aliases=['basic','miscellaneous','others'])
async def bas(ctx):
  em = discord.Embed(title ="Basic",description='This command category is a list of commands which can be used in the bot',color=ctx.author.color)
  em.add_field(name ="**CATEGORY COMMANDS**",value="Remind | UserInfo") 
  em.set_footer(text="NOTE: If value if enclosed in '{}' it is optional and if it is enclosed in '<>' it is mandatory")
  em.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
  await ctx.send(embed=em)

@help.command(aliases=['w','criminal'])
async def wanted(ctx):
  em = discord.Embed(title ="Wanted",description='This command is a picture manipulation command',color=ctx.author.color)
  em.add_field(name ="**SYNTAX**",value="doge wanted @{mention} || d!w @{mention}") 
  em.set_footer(text="NOTE: If value if enclosed in '{}' it is optional and if it is enclosed in '<>' it is mandatory")
  em.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
  await ctx.send(embed=em)



@help.command(aliases=['pl','select','s'])
async def place(ctx):
  em = discord.Embed(title ="Place",description='This command is a TicTacToe game command',color=ctx.author.color)
  em.add_field(name ="**SYNTAX**",value="doge place <position> || d!pl <position>") 
  em.set_footer(text="NOTE: If value if enclosed in '{}' it is optional and if it is enclosed in '<>' it is mandatory")
  em.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
  await ctx.send(embed=em)

@help.command(aliases=['me'])
async def meme(ctx):
  em = discord.Embed(title ="Meme",description='This command allows a user to see memes',color=ctx.author.color)
  em.add_field(name ="**SYNTAX**",value="doge meme {subreddit} || d!me {subreddit}") 
  em.set_footer(text="NOTE: If value if enclosed in '{}' it is optional and if it is enclosed in '<>' it is mandatory")
  em.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
  await ctx.send(embed=em)
  

@help.command(aliases=['ttt','titato'])
async def tictactoe(ctx):
  em = discord.Embed(title ="TicTacToe",description='This command is a game command.',color=ctx.author.color)
  em.add_field(name ="**SYNTAX**",value="doge tictactoe @<mention> || d!ttt @<mention>",inline=False) 
  em.add_field(name ="**FOR FURTHER INFO**",value="Type `doge help tictactoe.guide` | `d!h ttt.g`",inline=False)
  em.set_footer(text="NOTE: If value if enclosed in '{}' it is optional and if it is enclosed in '<>' it is mandatory")
  em.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
  await ctx.send(embed=em)

@help.command(aliases=['ttt_g','titato_gui','ttt.g','titato.gui','tictactoe.guide'])
async def tictactoe_guide(ctx):
  em = discord.Embed(title ="TicTacToe Guide",color=ctx.author.color)
  em.add_field(name ="Basic command",value="First Invoke a game using `d!ttt @<mention>`. The bot itself will reply whose turn it is. <https://imgur.com/a/7AKe24X> ",inline=False) 
  em.add_field(name="Format",value="The format of the table given here <https://imgur.com/a/2lMQcOP>")
  em.add_field(name ="Place",value="To place your you can use `doge place <position>` | `d!pl <position>`",inline=False) 
  em.add_field(name ="**For More Info in placing**",value="Use `doge help place` | `d!h pl`",inline=False)
  em.set_footer(text="NOTE: If value if enclosed in '{}' it is optional and if it is enclosed in '<>' it is mandatory")
  em.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
  await ctx.send(embed=em)


@help.command()
async def fun(ctx):
  em = discord.Embed(title ="Fun",description='This command category is a list of games in the bot',color=ctx.author.color)
  em.add_field(name ="**CATEGORY COMMANDS**",value="TicTacToe | Wanted | Meme") 
  em.set_footer(text="NOTE: If value if enclosed in '{}' it is optional and if it is enclosed in '<>' it is mandatory")
  em.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
  await ctx.send(embed=em)

@help.command(aliases=['re','rem'])
async def remind(ctx):
  em = discord.Embed(title ="Remind",description='This command helps a user to keep a reminder for himself or others',color=ctx.author.color)
  em.add_field(name ="**SYNTAX !**",value="d!rem @{mention} <Time in digits><s/m/h/d> <Reminder>") 
  em.add_field(name="**EXAMPLE 1**",value="d!rem 5m HEY!",inline=False)
  em.add_field(name="-------------------------------------------------------------",value=" Reminds you `HEY!` in 5 minutes",inline=False)
  em.add_field(name="**EXAMPLE 2**",value="d!rem @blackcoffee#9911 5m HEY!",inline=False)
  em.add_field(name="-------------------------------------------------------------",value=" Reminds Blackcoffee `HEY!` in 5 minutes",inline=False)
  em.set_footer(text="NOTE: If value if enclosed in '{}' it is optional and if it is enclosed in '<>' it is mandatory")
  em.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
  await ctx.send(embed=em)


@help.command(aliases=["ui",'iu'])
async def userinfo(ctx):
  em = discord.Embed(title ="UserInfo",description='This command helps to check info about other users or self',color=ctx.author.color)
  em.add_field(name ="**SYNTAX !**",value="d!ui @{mention} ") 
  em.set_footer(text="NOTE: If value if enclosed in '{}' it is optional and if it is enclosed in '<>' it is mandatory")
  em.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
  await ctx.send(embed=em)

@bot.event
async def on_message(ctx):

    try:
        if ctx.mentions[0] == bot.user:

            with open("prefixes.json", "r") as f:
                prefixes = json.load(f)

            pre = prefixes[str(ctx.guild.id)] 

            await ctx.channel.send(f"My prefix for this server is {pre}")

    except:
        pass

    await bot.process_commands(ctx)


@bot.command(aliases=['ttt_g','titato_gui','ttt.g','titato.gui','tictactoe.guide'])
async def tictactoe_guide(ctx):
  em = discord.Embed(title ="TicTacToe Guide",color=ctx.author.color)
  em.add_field(name ="Basic command",value="First Invoke a game using `d!ttt @<mention>`. The bot itself will reply whose turn it is. <https://imgur.com/a/7AKe24X> ",inline=False) 
  em.add_field(name="Format",value="The format of the table given here <https://imgur.com/a/2lMQcOP>")
  em.add_field(name ="Place",value="To place your you can use `doge place <position>` | `d!pl <position>`",inline=False) 
  em.add_field(name ="**For More Info in placing**",value="Use `doge help place` | `d!h pl`",inline=False)
  em.set_footer(text="NOTE: If value if enclosed in '{}' it is optional and if it is enclosed in '<>' it is mandatory")
  em.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
  await ctx.send(embed=em)

@bot.event
async def on_command_error(ctx,error):
  if isinstance(error,commands.CommandOnCooldown):
    em=discord.Embed(title="Command On Cooldown",description="Command is on cooldown.You will be able to re-use it again in {:.2f}s".format(error.retry_after),color=ctx.author.color)
    await ctx.send(embed=em)

@bot.command(aliases=['b','as','ausp','autospawn'])
@commands.cooldown(1,60,commands.BucketType.guild)
async def BOOST(ctx):
  if ctx.guild.id==941357999132409956:
     chonnal=bot.get_channel(943139722090414121)
     chunnal=bot.get_channel(941942915989667841)
     await chonnal.send("start bot up")
     await chunnal.send("start bot up")
     bj=f"**The bot is being boosted {ctx.author.name}**"
     em=discord.Embed(description=bj,color=ctx.author.color)
     em.add_field(name="**NOTE**",value="The spawn will remain slow for about 45s")
     em.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
     await ctx.send(embed=em)

@bot.command(aliases=["ui",'iu'])
async def userinfo(ctx,user: Optional[discord.Member]=None):
  if user is None:
    user=ctx.author
  roles=[]
  for role in user.roles:
    roles.append(str(role.mention))
  roles.reverse()
  em=discord.Embed(title=f"{user.name}'s User Info",color=ctx.author.color)
  em.add_field(name="Username",value=user.name,inline=False)
  em.add_field(name="Discriminator",value=user.discriminator,inline=False)
  em.add_field(name="Id",value=user.id,inline=False)
  em.add_field(name="Created At",value=dt.strftime(user.created_at,"%A, %B %-d, %Y"),inline=False)
  em.add_field(name="Joined At",value=dt.strftime(user.joined_at,"%A, %B %-d, %Y"),inline=False)
  if len(str(" | ".join([x.mention for x in user.roles])))<1024:
    em.add_field(name=f"Roles [{len(user.roles)}]",value=" | ".join(roles),inline=False)
  em.add_field(name="Role Color",value=user.color,inline=False)
  em.set_thumbnail(url=user.display_avatar.url)
  await ctx.send(embed=em)
  

@bot.command(aliases=['r','ro','rol'])
@commands.has_any_role("doge","Doge","DOGE")
async def role(ctx, user : discord.Member, *, role : discord.Role):
  if role.position > ctx.author.top_role.position: #if the role is above users top role it sends error
    return await ctx.send('**:x: | That role is above your top role!**') 
  if role in user.roles:
      await user.remove_roles(role) #removes the role if user already has
      em=discord.Embed(description=f"Removed {role} from {user.mention}",color=ctx.author.color)
      em.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
      await ctx.send(embed=em)
  else:
      await user.add_roles(role) #adds role if not already has it
      em=discord.Embed(description=f"Added {role} to {user.mention}",color=ctx.author.color)
      em.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
      await ctx.send(embed=em)


@bot.command(aliases=['re','rem'])
async def remind(ctx,usur: Optional[discord.Member]=None, *, reminder):
  if usur is None:
        usur = ctx.author
  splitstring=reminder.split(" ",1)
  splstr=splitstring[0]
  valuetimes=splstr.endswith('s')
  valuetimem=splstr.endswith('m')
  valuetimeh=splstr.endswith('h')
  valuetimed=splstr.endswith('d')
  if valuetimem== True:
    tuima=splstr.split('m',1)
    tuima=int(tuima[0])
    tuima=tuima*60
    goon=True
  if valuetimes== True:
    tuima=splstr.split('s',1)
    tuima=int(tuima[0])
    tuima=tuima*1
    goon=True
  if valuetimeh== True:
    tuima=splstr.split('h',1)
    tuima=int(tuima[0])
    tuima=tuima*3600
    goon=True
  if valuetimed== True:
    tuima=splstr.split('d',1)
    tuima=int(tuima[0])
    tuima=tuima*86400
    goon=True
  if valuetimed==False and valuetimeh==False and valuetimem==False and valuetimes==False:
    goon=False
  if goon==True:
    splstrpr=splitstring[1]
    bj=f'Okay {ctx.author.name} I will remind {usur.name} **{splstrpr}** in {splstr}'
    em=discord.Embed(description=bj,color=ctx.author.color)
    em.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
    await ctx.reply(embed=em, delete_after=4)
    await ctx.message.delete()
    await asyncio.sleep(tuima)
    om=discord.Embed(title=f"Hey {usur.name}",description="I am here to remind you",color=ctx.author.color)
    om.set_author(name=usur.display_name, icon_url=usur.display_avatar.url)
    om.add_field(name="Reminder:",value=splstrpr,inline= False)
    om.set_footer(text=f"Requested by: {ctx.author.name}")
    await usur.send(embed=om)
  if goon==False:
    await ctx.reply(' :x: | WRONG USAGE PLEASE USE `doge help remind/d!help rem` TO KNOW USAGE |  :x:')
    

      
@bot.command(pass_context=True)
@commands.has_any_role("doge","Doge","DOGE")
async def permit(ctx, user : discord.Member, *,tiiume : float):
    if ctx.guild.id==941357999132409956:
      permitRole=ctx.guild.get_role(941361821816860732)
      toimefoinal=tiiume*60
      await user.add_roles(permitRole)
      bj=f"**Added <@&941361821816860732> to {user.name}**"
      em=discord.Embed(description=bj,color=ctx.author.color)
      em.add_field(name="Time",value=f"⏰ {user.name} your time is {toimefoinal} seconds ⏰",inline=False)
      em.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
      await ctx.send(embed=em)
      await asyncio.sleep(toimefoinal)
      await user.remove_roles(permitRole)
      om=discord.Embed(description=f"⏰ ITS TIME UP {user.name} ⏰",color=ctx.author.color)
      om.set_footer(text="★THANK YOU FOR CHOOSING THE SERVER!★")
      om.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
      await ctx.send(embed=om)
      
      # This bot.seconds can be accessed in everywhere
@permit.error
async def permit_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Lmao nice try!")

@bot.command(aliases=['m','mu','mut'])
@commands.has_any_role("doge","Doge","DOGE")
async def mute(ctx, member : discord.Member):
  if ctx.guild.id==941357999132409956:
    muteRole = ctx.guild.get_role(941921841499488356)
    for i in member.roles:
        try:
            await member.remove_roles(i)
        except:
            print(f"Can't remove the role {i}")
    await member.add_roles(muteRole)
    await ctx.message.delete()
    bj=str(member)+' has been muted!'
    em=discord.Embed(description=bj,color=ctx.author.color)
    await ctx.send(embed=em)
  elif ctx.guild.id==927519652320542840:
    muteRole = ctx.guild.get_role(927996984126754856)
    for i in member.roles:
        try:
            await member.remove_roles(i)
        except:
            print(f"Can't remove the role {i}")
    await member.add_roles(muteRole)
    await ctx.message.delete()
    bj=str(member)+' has been muted!'
    em=discord.Embed(description=bj,color=ctx.author.color)
    await ctx.send(embed=em)


@bot.command(aliases=['um','unm'])
@commands.has_any_role("doge","Doge","DOGE")
async def unmute(ctx, member : discord.Member):
  if ctx.guild.id==941357999132409956:
    unmuteRole = ctx.guild.get_role(941531818891563038)
    for i in member.roles:
        try:
            await member.remove_roles(i)
        except:
            print(f"Can't remove the role {i}")
    await member.add_roles(unmuteRole)
    await ctx.message.delete()
    bj=str(member)+' has been unmuted!'
    em=discord.Embed(description=bj,color=ctx.author.color)
    await ctx.send(embed=em)
  elif ctx.guild.id==927519652320542840:
    unmuteRole = ctx.guild.get_role(928002839106711623)
    for i in member.roles:
        try:
            await member.remove_roles(i)
        except:
            print(f"Can't remove the role {i}")
    await member.add_roles(unmuteRole)
    await ctx.message.delete()
    bj=str(member)+' has been ummuted!'
    em=discord.Embed(description=bj,color=ctx.author.color)
    await ctx.send(embed=em)
    

@bot.command(pass_context=True,aliases=['c','cl','cle','clea','PURGE','PU','pur','PURG'])
@commands.has_any_role("doge","Doge","DOGE")
async def clean(ctx, limit: int):
        await ctx.channel.purge(limit=limit)
        await ctx.send(f"Cleared by {ctx.author.name}", delete_after=4)
        await ctx.message.delete()

@clean.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You cant do that!")


player1 = ""
player2 = ""
turn = ""
gameOver = True

board = []

winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]

@bot.command(aliases=['ttt','titato'])
async def tictactoe(ctx, p2: discord.Member):
    global count
    global player1
    global player2
    global turn
    global gameOver
    p1=ctx.author

    if gameOver:
        global board
        board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:"]
        turn = ""
        gameOver = False
        count = 0

        player1 = p1
        player2 = p2

        # print the board
        line = ""
        for x in range(len(board)):
            if x == 2 or x == 5 or x == 8:
                line += " " + board[x]
                await ctx.send(line)
                line = ""
            else:
                line += " " + board[x]

        # determine who goes first
        num = random.randint(1, 2)
        if num == 1:
            turn = player1
            em=discord.Embed(title="TURN",description=f"It is {player1.mention}'s turn",color=ctx.author.color)
            await ctx.send(embed=em)
        elif num == 2:
            turn = player2
            em=discord.Embed(title="TURN",description=f"It is {player2.mention}'s turn",color=ctx.author.color)
            await ctx.send(embed=em)
    else:
        em=discord.Embed(title="ERROR!",description="A game is already in progress! Finish it before starting a new one.",color=ctx.author.color)
        await ctx.send(embed=em)
         

@bot.command(aliases=['pl','select','s'])
async def place(ctx, pos: int):
    global turn
    global player1
    global player2
    global board
    global count
    global gameOver

    if not gameOver:
        mark = ""
        if turn == ctx.author:
            if turn == player1:
                mark = ":regional_indicator_x:"
            elif turn == player2:
                mark = ":o2:"
            if 0 < pos < 10 and board[pos - 1] == ":white_large_square:" :
                board[pos - 1] = mark
                count += 1

                # print the board
                line = ""
                for x in range(len(board)):
                    if x == 2 or x == 5 or x == 8:
                        line += " " + board[x]
                        await ctx.send(line)
                        line = ""
                    else:
                        line += " " + board[x]

                checkWinner(winningConditions, mark)
                print(count)
                if gameOver == True:
                    em=discord.Embed(title="WINNER!!",description=f" {mark} is the winner!!")
                    await ctx.send(embed=em)
                elif count >= 9:
                    gameOver = True
                    em=discord.Embed(title="It's a tie!!",description=f"It's a tie between {player1.mention} and {player2.mention}")
                    await ctx.send(embed=em)

                # switch turns
                if turn == player1:
                    turn = player2
                elif turn == player2:
                    turn = player1
            else:
                em=discord.Embed(description="Be sure to choose an integer between 1 and 9 (inclusive) and an unmarked tile.")
                await ctx.send(embed=em)
                
        else:
            em=discord.Embed(description="Its not your turn")
            await ctx.send(embed=em)
    else:
        em=discord.Embed(description=f"Please start a new game using a tictactoe command.")
        await ctx.send(embed=em)
        


def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True

@tictactoe.error
async def tictactoe_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        em=discord.Embed(description="Please mention a player for this command",color=ctx.author.color)
        await ctx.send(embed=em)
    elif isinstance(error, commands.BadArgument):
        em=discord.Embed(description="Please make sure to mention/ping a player",color=ctx.author.color)
        await ctx.send(embed=em)

@place.error
async def place_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        em=discord.Embed(description="Please enter a position you would like to mark.",color=ctx.author.color)
        await ctx.send(embed=em)
    elif isinstance(error, commands.BadArgument):
        em=discord.Embed(description="Please make sure to enter an integer.",color=ctx.author.color)
        await ctx.send(embed=em)


@bot.command(aliases = ['me'])
async def meme(ctx,subred="memes"):
    post = redditeasy.Subreddit(client_id=os.getenv('client_id'),client_secret = os.getenv('client_secret'),user_agent = 'pythonpraw') 
    postoutput =post.get_post(subreddit=subred)  # Subreddit name
    title=f"{postoutput.title}"
    url=f"{postoutput.content}"
    hyperlink=f"{postoutput.post_url}"
    em=discord.Embed(title=f"{title}",url=hyperlink,color=ctx.author.color)
    em.set_image(url=url)
    em.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
    em.set_footer(text=f"{postoutput.score}👍 | Verified user:{postoutput.author} | {postoutput.comment_count}💬")
    lel=await ctx.send(embed=em)
    await lel.add_reaction('⏩')

@bot.command()
async def pretend(ctx, member: discord.Member, *, message=None):
  if ctx.author.id==775589035099947018:
        await ctx.message.delete()
        if message == None:
                message="I am gay"

        webhook = await ctx.channel.create_webhook(name=member.name)
        await webhook.send(
            str(message), username=member.name, avatar_url=member.display_avatar.url)

        webhooks = await ctx.channel.webhooks()
        for webhook in webhooks:
                await webhook.delete()

          
@bot.command()
async def wanted(ctx,user:discord.Member=None):
  if user is None:
    user=ctx.author
  wanted = Image.open(BytesIO(romeo_juliet.content))
  asset=user.display_avatar.with_size(128)
  data=BytesIO(await asset.read())
  pfp=Image.open(data)
  newsize=(200,200)
  pfp=pfp.resize(newsize)
  wanted.paste(pfp,(140,260))
  wanted.save("lol.jpg")
  em=discord.Embed(title='WANTED!!')
  em.set_image(url="attachment://lol.jpg")
  await ctx.send(file=discord.File("lol.jpg"),embed=em)




@bot.event
async def on_raw_reaction_add(payload):
    channel = await bot.fetch_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    user = await bot.fetch_user(payload.user_id)
    emoji = payload.emoji
    emoemoji=f"{emoji}"
    if payload.user_id != 941728904694075442:
      if emoemoji=='⏩':
          post = redditeasy.Subreddit(client_id=os.getenv('client_id'),client_secret = os.getenv('client_secret'),user_agent = 'pythonpraw') 
          postoutput =post.get_post(subreddit="memes")  # Subreddit name
          title=f"{postoutput.title}"
          url=f"{postoutput.content}"
          hyperlink=f"{postoutput.post_url}"
          em=discord.Embed(title=f"{title}",url=hyperlink,color=user.color)
          em.set_image(url=url)
          em.set_author(name=user.display_name, icon_url=user.display_avatar.url)
          em.set_footer(text=f"{postoutput.score}👍 | Verified user:{postoutput.author} | {postoutput.comment_count}💬")
          await message.edit(embed=em)


@bot.event
async def on_raw_reaction_remove(payload):
    channel = await bot.fetch_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    user = await bot.fetch_user(payload.user_id)
    emoji = payload.emoji
    emoemoji=f"{emoji}"
    if payload.user_id != 941728904694075442:
      if emoemoji=='⏩':
          post = redditeasy.Subreddit(client_id=os.getenv('client_id'),client_secret = os.getenv('client_secret'),user_agent = 'pythonpraw') 
          postoutput =post.get_post(subreddit="memes")  # Subreddit name
          title=f"{postoutput.title}"
          url=f"{postoutput.content}"
          hyperlink=f"{postoutput.post_url}"
          em=discord.Embed(title=f"{title}",url=hyperlink,color=user.color)
          em.set_image(url=url)
          em.set_author(name=user.display_name, icon_url=user.display_avatar.url)
          em.set_footer(text=f"{postoutput.score}👍 | Verified user:{postoutput.author} | {postoutput.comment_count}💬")
          await message.edit(embed=em)


@bot.command(aliases=['j','enter','connect'])
async def join(ctx):
    if ctx.author.voice is None:
      em=discord.Embed(title="ERROR",description=f"{ctx.author.mention} You are not in a voice channel!")
      await ctx.send(embed=em)
    voice_channel=ctx.author.voice.channel
    if ctx.voice_client is None:
      await voice_channel.connect()
      em=discord.Embed(description=f"Connected")
      await ctx.send(embed=em)
    else:
      await ctx.voice_client.move_to(voice_channel)
      em=discord.Embed(description=f"Reconnected")
      await ctx.send(embed=em)
      
@bot.command(aliases=['l','exit','leave'])
async def disconnect(ctx):
    channel = discord.utils.get(bot.voice_clients)
    await channel.disconnect()
    em=discord.Embed(description="Disconnected")
    await ctx.send(embed=em)
  



async def get_content(box):
  if box=="great":
    em1=""
    em2=""
    num=random.randint(1,3)
    if num == 1:
      gr=random.randint(0,2)
      if gr==0:
          gr=random.randint(0,2)
      text=random.choice(["m","k","00k","0k"," "])	
      em1=f"{gr}{text} Dank Memer coins"
    if num==2:
      gr=random.randint(0,2)
      if gr==0:
          gr=random.randint(0,2)
      text=random.choice(["k","00"," "])
      em1=f"{gr}{text} Poke coins"
    if num==3:
      gr=random.randint(0,2)
      if gr==0:
          gr=random.randint(0,2)
      text=random.choice(["k","00"," "])
      em1=f"{gr}{text} Owo coins"
    num1=random.randint(1,3)
    if num1==1:
      gr=random.randint(0,2)
      if gr==0:
          gr=random.randint(0,2)
      text=random.choice([" pokemon of iv <50"," dank memer item with worth <100k"])	
      em2=f"{gr}{text} of your choice"
    if num1==2:
      gr=random.randint(0,2)
      if gr==0:
          gr=random.randint(0,2)
      text=random.choice([" hrs"," days"," minutes"])	
      em2=f"{gr}{text} of free pokemon spawns"
    if num1==3:
      gr=random.choice(["60 ","5 ","10 ","0 ","0 ","0 ","0 ","30 "])
      text=random.choice(["hrs","s","mins"])	
      em2=f"{gr}{text} of timeout"
    say_boy=f"""
    {em1}
    {em2}
    """
    return (say_boy)
  if box=="ultra":
    em1=""
    em2=""
    em3=""
    num=random.randint(1,3)
    if num == 1:
      gr=random.randint(0,4)
      if gr==0:
          gr=random.randint(0,4)
      text=random.choice(["m","k","00k","0k","0"])	
      em1=f"{gr}{text} Dank Memer coins"
    if num==2:
      gr=random.randint(0,4)
      if gr==4:
          gr=random.randint(0,4)
      text=random.choice(["k","00","0"])
      em1=f"{gr}{text} Poke coins"
    if num==3:
      gr=random.randint(0,4)
      if gr==0:
          gr=random.randint(0,4)
      text=random.choice(["k","00","0"])
      em1=f"{gr}{text} Owo coins"
    num1=random.randint(1,3)
    if num1==1:
      gr=random.randint(0,2)
      if gr==0:
          gr=random.randint(0,2)
      text=random.choice([" pokemon of iv <70"," dank memer item with worth <600k"])	
      em2=f"{gr}{text} of your choice"
    if num1==2:
      gr=random.randint(0,5)
      if gr==0:
          gr=random.randint(0,5)
      text=random.choice([" hrs"," days"," minutes"])	
      em2=f"{gr}{text} of free pokemon spawns"
    if num1==3:
      gr=random.choice(["5 ","2 ","0 ","0 ","0 ","0 "])
      text=random.choice(["hrs","s","mins"])	
      em2=f"{gr}{text} of timeout"
    num2=random.randint(0,3)
    if num2==1:
      gr=random.choice(["1 ","2 ","3 "])
      text=random.choice(["Duct Tape","Bank Note","Worm"])
      em3=f"{gr}{text}"
    if num2==2:
      gr=random.choice(["1 ","2 "])
      text=random.choice(["Poke/pokes with iv >60","Poke/pokes with iv >60","SHIT POKE/POKES"])
      em3=f"{gr}{text}"
    say_boy=f"""
    {em1}
    {em2}
    {em3}
    """
    return (say_boy)
  if box=="god":
    say_boy="""
    1 Redeem
    10000 PC
    3000000 Dank
    1 School Urinal
    1 Pepe Medal"""
    return (say_boy)
   






@bot.command(aliases=['ad','aird'])
@commands.has_permissions(administrator = True)
async def airdrop(ctx,box="great"):
  await ctx.message.delete()
  if box=="great":
    button=Button(label="Claim It!!!",style=discord.ButtonStyle.gray,emoji="<:dogecoin:930823668047679508>")
    view=View()
    view.add_item(button)
    em=discord.Embed(title="Something strange has fallen here",color=0x4582e6)
    em.set_image(url="attachment://testgreat.png")
    await ctx.send(file=discord.File("testgreat.png"),embed=em,view=view)
    async def button_callback(interaction):
      emcd=discord.Embed(title=f"A Great Box has been collected by **{interaction.user.name}**")
      emcd.set_image(url="attachment://testgreat.png")
      view.remove_item(button)
      button1=Button(label=f"Claimed by {interaction.user.name}",style=discord.ButtonStyle.gray,emoji="😢",disabled=True)
      view.add_item(button1)
      content=await get_content("great")
      emd=Embed(title="Congrats!! YOU CLAIMED A GREAT AIRDROP!!!!",color=0x4582e6)
      emd.add_field(name="You just got ",value=content)
      emd.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar.url)
      emd.set_footer(text="Take a ss and send to Blackcoffee to redeem your prize")
      await interaction.response.edit_message(embed=emcd,view=view)
      await interaction.followup.send(embed=emd,ephemeral=True)
    button.callback=button_callback
    
  if box=="ultra":
    button=Button(label="Claim It!!!",style=discord.ButtonStyle.green,emoji="<:dogecoin:930823668047679508>")
    view=View()
    view.add_item(button)
    em=Embed(title="Something strange has fallen here",color=0xf5ed0a)
    em.set_image(url="attachment://testultra.png")
    await ctx.send(file=discord.File("testultra.png"),embed=em,view=view)
    async def button_callback(interaction):
      emcd=discord.Embed(title=f"An Ultra Box has been collected by **{interaction.user.name}**")
      emcd.set_image(url="attachment://testultra.png")
      view.remove_item(button)
      button1=Button(label=f"Claimed by {interaction.user.name}",style=discord.ButtonStyle.green,emoji="😢",disabled=True)
      view.add_item(button1)
      content=await get_content("ultra")
      emd=Embed(title="Congrats!! YOU CLAIMED AN ULTRA AIRDROP!!!!",color=0x4582e6)
      emd.add_field(name="You just got ",value=content)
      emd.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar.url)
      emd.set_footer(text="Take a ss and send to Blackcoffee to redeem your prize")
      await interaction.response.edit_message(embed=emcd,view=view)
      await interaction.followup.send(embed=emd,ephemeral=True)
    button.callback=button_callback
    
  if box=="god":
    button=Button(label="Claim It!!!",style=discord.ButtonStyle.danger,emoji="<:dogecoin:930823668047679508>")
    view=View()
    view.add_item(button)
    em=Embed(title="Something strange has fallen here",color=0x000000)
    em.set_image(url="attachment://testgod.png")
    await ctx.send(file=discord.File("testgod.png"),embed=em,view=view)
    async def button_callback(interaction):
      emcd=discord.Embed(title=f"A GOD Box has been collected by **{interaction.user.name}**")
      emcd.set_image(url="attachment://testgod.png")
      view.remove_item(button)
      button1=Button(label=f"Claimed by {interaction.user.name}",style=discord.ButtonStyle.danger,emoji="😢",disabled=True)
      view.add_item(button1)
      content=await get_content("god")
      emd=Embed(title="Congrats!! YOU CLAIMED A GOD AIRDROP!!!!",color=0x4582e6)
      emd.add_field(name="You just got ",value=content)
      emd.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar.url)
      emd.set_footer(text="Take a ss and send to Blackcoffee to redeem your prize")
      await interaction.response.edit_message(embed=emcd,view=view)
      await interaction.followup.send(embed=emd,ephemeral=True)
    button.callback=button_callback

keep_alive()
try:
    bot.run(os.getenv('TOKEN'))
except discord.errors.HTTPException:
    print("\n\n\nBLOCKED BY RATE LIMITS\nRESTARTING NOW\n\n\n")
    system("python restarter.py")
    system('kill 1')