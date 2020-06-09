from discord.ext import commands
import discord
from cogs.utils.message import LangMessage


class Ignore(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    async def ignore(self, ctx):
        pass

    @ignore.command()
    async def add(self, ctx, role: discord.Role):
        await ctx.send(LangMessage(ctx.guild).add_role_message(await self.bot.keeper.add_ignore(ctx.guild, role)))

    @ignore.command()
    async def remove(self, ctx, role: discord.Role):
        await ctx.send(LangMessage(ctx.guild).remove_role_message(await self.bot.keeper.remove_ignore(ctx.guild, role)))

    @ignore.command(name='list')
    async def role_list(self, ctx):
        role_id_list = await self.bot.keeper.get_ignore(ctx.guild)
        role_list = [ctx.guild.get_role(i) for i in role_id_list if ctx.guild.get_role(i) is not None]
        embed = discord.Embed(title='Role list', description=' '.join(i.mention for i in role_list),
                              color=0x00bfff)
        await ctx.send(embed=embed)


def setup(bot):
    return bot.add_cog(Ignore(bot))