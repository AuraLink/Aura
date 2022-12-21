import discord
from discord.ext import commands
from discord.ext import tasks

import os
import asyncio
import platform
from dotenv import load_dotenv
from itertools import cycle

from database import DB
from sqlite3 import sqlite_version
from assets.scripts import terminal as t
from assets.scripts.terminal import colors as tc
from assets.scripts.date import now


# terminal setup
load_dotenv()
t.clear()

# Setup
intents = discord.Intents.all()
intents.message_content = True

def prefix(client, message): return DB.fetch_prefix(message.guild.id)

bot_version = "alpha 1.0.0"

client = commands.Bot(command_prefix=prefix, intents=intents)
client.remove_command('help')

class ClientEvents:
    @client.event
    async def on_ready():
        t.title("Status: ON")
        change_status.start()
        print(f"{now()} {tc.fg.lightblue}INFO     {tc.fg.purple}{client.user}{tc.reset} is ready to rock n'roll!")
        print(f"{now()} {tc.fg.lightblue}INFO     {tc.fg.purple}bot.version{tc.reset} {bot_version}")
        print(f"{now()} {tc.fg.lightblue}INFO     {tc.fg.purple}python.version{tc.reset} {platform.python_version()}")
        print(f"{now()} {tc.fg.lightblue}INFO     {tc.fg.purple}sqlite.version{tc.reset} {sqlite_version}")
        print(f"{now()} {tc.fg.lightblue}INFO     {tc.fg.purple}platform{tc.reset} {platform.system()} {platform.release()} ({os.name})")


    @client.event
    async def on_guild_join(guild):
        guild_id = str(guild.id)
        guild_prefix = "*"
        print(guild_id, guild_prefix)
        DB.add_guild(guild_id, guild_prefix)

    @client.event
    async def on_guild_remove(guild):
        guild_id = str(guild.id)
        DB.delete_guild(guild_id)


    @client.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            minutes, seconds = divmod(error.retry_after, 60)
            hours, minutes = divmod(minutes, 60)
            hours = hours % 24
            embed = discord.Embed(
                title="Hey, please slow down!",
                description=f"You can use this command again in {f'{round(hours)} hours' if round(hours) > 0 else ''} {f'{round(minutes)} minutes' if round(minutes) > 0 else ''} {f'{round(seconds)} seconds' if round(seconds) > 0 else ''}.",
                color=0xE02B2B
            )
            await ctx.send(embed=embed)

            return
        if isinstance(error, commands.CommandNotFound):
            return
        await ctx.send(f"Error: {error}") # Disable after deployment

    @client.event
    async def on_message(message):
        channel = client.get_channel(1054943734472658984)
        #if message.content.startswith("report"):
        if message.guild is None and message.author != client.user:
            await channel.send(message.content)
        await client.process_commands(message)


@client.group(name="cog", invoke_without_command=True)
async def cogHandler(ctx):
    await ctx.send("Available commands: check, load, unload, reload")

@cogHandler.command()
async def check(ctx, cog_name):
    try:
        await client.load_extension(f"cogs.{cog_name}")
    except commands.ExtensionAlreadyLoaded:
        await ctx.send(f"{cog_name} is loaded.")
    except commands.ExtensionNotFound:
        await ctx.send(f"{cog_name} is not found or doesn't exist.")
    else:
        await ctx.send(f"{cog_name} is unloaded")
        await client.unload_extension(f"cogs.{cog_name}")

@cogHandler.command()
async def load(ctx, cog_name):
    try:
        await client.load_extension(f"cogs.{cog_name}")
        print(f"{now()} {tc.fg.yellow}COG     Succesfully loaded {cog_name}! {tc.reset}")
    except commands.ExtensionAlreadyLoaded:
        await ctx.send(f"{cog_name} is already loaded.")
    except commands.ExtensionNotFound:
        await ctx.send(f"{cog_name} is not found or doesn't exist.")

@cogHandler.command()
async def unload(ctx, cog_name):
    try:
        await client.unload_extension(f"cogs.{cog_name}")
        print(f"{now()} {tc.fg.yellow}COG     Succesfully unloaded {cog_name}! {tc.reset}")
    except commands.ExtensionAlreadyLoaded:
        await ctx.send(f"{cog_name} unloaded.")
    except commands.ExtensionNotFound:
        await ctx.send("Cog not found")

@cogHandler.command()
async def reload(ctx, cog_name):
    try:
        await client.reload_extension(f"cogs.{cog_name}")
        print(f"{now()} {tc.fg.yellow}COG     Succesfully reloaded {cog_name}! {tc.reset}")
    except commands.ExtensionNotFound:
        await ctx.send(f"{cog_name} is not found or doesn't exist.")

# Testing command
@client.command()
async def comenzi(ctx):
    await ctx.send("""
# Bot 
cog 
cog check
cog load
cog unload
cog reload
leave
guilds
ping
bot

# Database

adduser
addguildmembers
addguild

# Admin
clear
kick
ban
unban
change_prefix    
""")

@client.command()
async def invite(ctx):
    await ctx.send("https://discord.com/api/oauth2/authorize?client_id=908432947609206784&permissions=8&scope=bot%20applications.commands")


rich_presence = cycle(["default prefix *", "*help", "ig:@zewutz"])
@tasks.loop(seconds=7)
async def change_status():
    try:
        await client.change_presence(activity=discord.Game(next(rich_presence)))
    except Exception as ext:
        print(ext)
        return

async def LoadCogs():
    try:
        t.title("Status: Loading cogs")
        print(f"{now()} {tc.fg.yellow}COG     Loading cogs process started {tc.reset}")
        for file in os.listdir('./cogs'):
            if file.endswith(".py"):
                extension = file[:-3]
                try:
                    await client.load_extension("cogs.{}".format(extension))
                    print(f"{now()} {tc.fg.yellow}COG     Succesfully loaded {extension}! {tc.reset}")

                except Exception as e:
                    print(f"{tc.fg.darkgrey} {now()} {tc.fg.red}COG     Failed to load {extension}! {tc.reset}")
                    exception = f"{type(e).__name__}: {e}"
                    print(exception)
                    
                    continue

    finally:
        print(f"{tc.fg.darkgrey} {now()} {tc.fg.yellow}COG     Done! {tc.reset}")

asyncio.run(LoadCogs())
clientToken = os.getenv("TOKEN")
client.run(clientToken)