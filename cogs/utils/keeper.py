import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import concurrent.futures
from cogs.utils.message import LangMessage
import discord


class Keeper:
    def __init__(self, bot):
        self.bot = bot
        self.cred = credentials.Certificate("serviceAccountKey.json")
        firebase_admin.initialize_app(self.cred)
        self.db = firestore.client()
        self.collection = self.db.collection('keeper')
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=20)

    async def run(self, func, *args):
        return await self.bot.loop.run_in_executor(self.executor, func, *args)

    async def greeting(self, guild):
        lang = LangMessage(guild)
        if await self.send_not_enough_message(guild.system_channel):
            return
        await guild.system_channel.send(embed=lang.greeting_embed)

    def check_permissions(self, guild):
        if self.get_not_enough_permissons(guild):
            return False
        else:
            return True

    def get_not_enough_permissons(self, guild):
        permissions = guild.me.guild_permissions
        not_enough = []
        if not permissions.manage_roles:
            not_enough.append('manage roles')
        if not permissions.embed_links:
            not_enough.append('embed links')

        return not_enough

    async def send_not_enough_message(self, channel):
        lang = LangMessage(channel.guild)
        if self.check_permissions(channel.guild):
            return False
        await channel.send(lang.create_not_enough_message(self.get_not_enough_permissons(channel.guild)))
        return True

    async def show_help(self, ctx):
        lang = LangMessage(ctx.guild)
        if await self.send_not_enough_message(ctx.channel):
            return
        await ctx.send(embed=lang.help_embed)

    async def save_role(self, member):
        ignore_list = await self.get_ignore(member.guild)
        roles = list(map(lambda x: x.id, member.roles))
        guild = member.guild
        save_roles = []
        for role in guild.roles:
            if role.id in ignore_list:
                continue
            if role.id == guild.default_role.id:
                continue
            if role.name == "Role Keeper":
                if role.permissions.manage_roles:
                    break
            if role.id in roles:
                save_roles.append(str(role.id))
        guild_document = self.collection.document(f'{guild.id}')
        await self.run(guild_document.set, {str(member.id): save_roles})

    async def load_role(self, member):
        guild = member.guild
        guild_document = self.collection.document(f'{guild.id}')
        r = await self.run(guild_document.get)
        result = r.to_dict()
        ignore_list = [int(i) for i in result.get('ignore', [])]
        if result is None or str(member.id) not in result:
            return
        for role_id in result[str(member.id)]:
            role = guild.get_role(int(role_id))
            if not role:
                continue
            if role.id in ignore_list:
                continue
            try:
                await member.add_roles(role)
            except discord.Forbidden:
                continue

    async def add_ignore(self, guild, role):
        ignore = await self.get_ignore(guild)
        if role.id in ignore:
            return False
        ignore.append(role.id)
        guild_document = self.collection.document(f'{guild.id}')
        await self.run(guild_document.set, {'ignore': [str(i) for i in ignore]})
        return True

    async def remove_ignore(self, guild, role):
        ignore = await self.get_ignore(guild)
        if role.id not in ignore:
            return False
        ignore.remove(role.id)
        guild_document = self.collection.document(f'{guild.id}')
        await self.run(guild_document.set, {'ignore': [str(i) for i in ignore]})
        return True

    async def get_ignore(self, guild):
        guild_document = self.collection.document(f'{guild.id}')
        r = await self.run(guild_document.get)
        result = r.to_dict()
        if result is None or 'ignore' not in result:
            return []
        return [int(i) for i in result['ignore']]





