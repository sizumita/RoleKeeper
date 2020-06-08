from discord.ext import commands
import discord


class Ignore(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def ignore(self, ctx):
        pass

    @ignore.command()
    async def add(self, role: discord.Role):
        pass

    @ignore.command()
    async def remove(self, role: discord.Role):
        pass
