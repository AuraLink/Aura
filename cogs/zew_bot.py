import os
import discord
from discord.ext import commands
from assets.scripts.terminal import colors as tc
from assets.scripts.date import now

class BotStatus(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        return

    @commands.group(name="bot", invoke_without_command=True)
    async def bot(self, ctx):
        embed=discord.Embed(title=" ", color=discord.Color.dark_theme())
        embed.add_field(name="Contact", value="*Discord*: zewutz#1974\n*Email*: zewutz@gmail.com\n*Instagram*: @zewutz")
        embed.add_field(name="Aura Website", value="auralink.xyz")
        await ctx.send(embed=embed)
    
    
    @bot.command(name="ping")
    @commands.is_owner()
    async def ping(self, ctx):
        embed = discord.Embed(title=f"Ping {round(self.client.latency * 1000)}ms")
        if round(self.client.latency * 1000) <= 50:
            embed.color = discord.Color.green()
        elif round(self.client.latency * 1000) <= 150:
            embed.color = discord.Color.orange()
        else:
            embed.color = discord.Color.red()

        await ctx.send(embed=embed)

    @bot.command(name="leave")
    @commands.is_owner()
    async def leave_guild(self, ctx, confirm):
        if confirm.lower() == "confirm":
            embed=discord.Embed(title=f"Bye {ctx.guild.name}", color=discord.Color.red())
            await ctx.guild.leave()

    @bot.command(name="guilds")
    @commands.is_owner()
    async def botguilds(self, ctx):
        embed = discord.Embed(title=f"{self.client.user.name} is currently connected to {len(list(self.client.guilds))} servers.")
        await ctx.send(embed=embed)

from database import DB

class DBManagement(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        pass

    @commands.is_owner()
    @commands.group(name="db", invoke_without_command=True)
    async def database_(self, ctx):
        status = DB.databaseStatus()
        embed = discord.Embed(title=f"Database status: {status}")
        if status == "Online":
            embed.color = discord.Color.green()
        else:
            embed.color = discord.Color.red()

        await ctx.send(embed=embed)


    @commands.is_owner()
    @database_.command(name="table")
    async def viewTable(self, ctx, tablename):
        return

    @commands.is_owner()
    @database_.command(name="adduser")
    async def addUser(self, ctx ,member : discord.Member):
        print(member)
        member_name = member.name
        member_tag = str(member)[-4:]
        member_id = member.id

        if member.bot is False:
            DB.add_user(member_name, member_tag, member_id)
            print(f"{now()} {tc.fg.green}DATABASE     {tc.reset}{member_id} inserted into database.")
            await ctx.send(f"{now()} {tc.fg.green}DATABASE     {tc.reset}{member_id} inserted into database.")
        elif member.bot is True:
            await ctx.send(f"{member} is a bot. ")

    @commands.is_owner()
    @database_.command(name="addguilduser")
    async def addAllGuildMembers(self, ctx):
        members = ctx.guild.members
        for member in members:
            if member.bot is False:
                result = DB.fetch_user(member.id)
                if result is False:
                    DB.add_user(member.name, str(member)[-4:], member.id)
            else:
                continue

        print(f"{now()} {tc.fg.green}DATABASE     {tc.reset}All {len(list(members))} users inserted into database.")



    @commands.is_owner()
    @database_.command(name="addguild")
    async def addGuild(self, ctx ,guild : discord.Guild):
        guild_id = guild.id
        guild_prefix = '*'

        DB.add_guild(guild_id, guild_prefix)
        await ctx.send(f"{guild} inserted into database.")



async def setup(client):
    await client.add_cog(BotStatus(client))
    await client.add_cog(DBManagement(client))