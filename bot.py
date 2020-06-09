from discord.ext import commands, tasks
import discord
import config
from cogs.utils.keeper import Keeper


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or('k'), help_command=None)
        for cog in config.cogs:
            try:
                self.load_extension(cog)
            except Exception as exc:
                print('Could not load extension {0} due to {1.__class__.__name__}: {1}'.format(cog, exc))
        self.keeper = Keeper(self)
        self.activity_task.start()

    async def on_ready(self):
        print('Logged on as {0} (ID: {0.id})'.format(self.user))

    async def on_command_error(self, context, exception):
        if isinstance(exception, commands.CommandNotFound):
            return
        if isinstance(exception, commands.BadArgument):
            await context.send('引数の型が間違っています。')
            return
        if isinstance(exception, commands.MissingRequiredArgument):
            await context.send('引数が足りません。')
            return
        await super().on_command_error(context, exception)

    @tasks.loop(minutes=10)
    async def activity_task(self):
        await self.wait_until_ready()
        await self.change_presence(activity=discord.Game(name=f'help -> khelp : {len(self.guilds)} servers'))

    async def on_guild_join(self, guild):
        await self.keeper.greeting(guild)

    async def on_member_join(self, member):
        await self.keeper.load_role(member)

    async def on_member_remove(self, member):
        await self.keeper.save_role(member)


bot = Bot()

# write general commands here


@bot.command(name="help")
async def help_command(ctx):
    await bot.keeper.show_help(ctx)

bot.run(config.token)
