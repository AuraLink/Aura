import os
import discord
from discord.ext import commands
from assets.scripts.terminal import colors as tc
from assets.scripts.date import now

class User(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        return

    @commands.group(name="user", invoke_without_command=True)
    async def user_(self, ctx):
        pass


    @user_.command(name="avatar")
    async def userInformation(self, ctx, member: discord.Member):
        avatar = member.avatar
        embed=discord.Embed(title=" ", color=discord.Color.purple())
        embed.set_image(url = avatar)
        await ctx.send(embed=embed)

    @user_.command(name="about")
    async def userAbout(self, ctx, member: discord.Member):
        userCurrentStatus = None
        if member.status == "dnd":
            userCurrentStatus = "Do not disturb"
        else:
            userCurrentStatus = str(member.status).capitalize()

        embed=discord.Embed(title=f"{member.name}#{member.discriminator}", color=discord.Color.purple())
        embed.add_field(name=f"Joined Discord on", value=f"{member.created_at.date()}", inline=False)
        embed.add_field(name=f"Current status", value=f"{userCurrentStatus}", inline=True)
        if member.bot:
            embed.add_field(name=f"Bot or not?!", value=f"Yep.. It's a bot.", inline=True)
        else:
            embed.add_field(name=f"Bot or not?!", value=f"Nope.. Not a bot", inline=True)
        
        embed.set_thumbnail(url=member.avatar)
        embed.set_footer(text=f"User id: {member.id}\nMore informations will be added soon")

        await ctx.send(embed=embed)

    @user_.command(name="message")
    @commands.is_owner()
    async def userMessage(self, ctx, member: discord.Member, *,message):
        if member in member.guild:
            await member.send(message)
        else:
            await self.client.get_user().send(message)

        await ctx.send(f"message sent to {member.name}#{member.discriminator}:{member.id}")


    @user_.command(name="test")
    @commands.is_owner()
    async def userInformation(self, ctx, member: discord.Member):
        embed=discord.Embed(title="Everything you could ever need to know", color=discord.Color.purple())
        embed.add_field(name="member.id", value=f"{member.id}",inline=False)
        embed.add_field(name="member.accent_color", value=f"{member.accent_color}",inline=False)
        embed.add_field(name="member.accent_colour", value=f"{member.accent_colour}",inline=False)
        embed.add_field(name="member.activities", value=f"{member.activities}",inline=False)
        embed.add_field(name="member.activity", value=f"{member.activity}",inline=False)
        embed.add_field(name="member.bot", value=f"{member.bot}",inline=False)
        embed.add_field(name="member.guild", value=f"{member.guild}",inline=False)
        embed.add_field(name="member.color", value=f"{member.color}",inline=False)
        embed.add_field(name="member.joined_at", value=f"{member.joined_at}",inline=False)
        embed.add_field(name="member.discriminator", value=f"{member.discriminator}",inline=False)
        embed.add_field(name="member.pending", value=f"{member.pending}",inline=False)
        embed.add_field(name="member.public_flags", value=f"{member.public_flags}",inline=False)
        embed.add_field(name="member.desktop_status", value=f"{member.desktop_status}",inline=False)
        embed.add_field(name="member.mobile_status", value=f"{member.desktop_status}",inline=False)
        embed.add_field(name="member.status", value=f"{member.status}",inline=False)
        await ctx.send(embed=embed)



async def setup(client):
    await client.add_cog(User(client))
