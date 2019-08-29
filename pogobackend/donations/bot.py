from discord.ext import commands
import discord
import aiohttp


class RoleBot(commands.Bot):

    def __init__(self, guild_to_roles, members):
        super().__init__(command_prefix=["/"], description="", pm_help=None,
                         help_attrs=dict(hidden=True))
        self.session = aiohttp.ClientSession(loop=self.loop)
        self.guild_to_roles = guild_to_roles
        self.members = members

    async def on_ready(self):
        # fetch all guilds the bot belongs to.
        for guild in self.guilds:
            await guild.fetch_roles()
            # if the server_id is not in our dict server_to_role, skip it.
            if guild.id not in self.guild_to_roles.keys():
                continue
            # get the roles we aim to assign.
            roles = [guild.get_role(role_id) for role_id in self.guild_to_roles[guild.id]]
            async for member in guild.fetch_members(limit=10000):
                username = f'{member.name}#{member.discriminator}'
                if username in self.members:
                    await member.add_roles(*roles)
                    print(f'gave {username}, roles {roles}')
                else:
                    await member.remove_roles(*roles)
                    print(f'took {username}, roles {roles}')
        await self.session.close()
        await self.logout()
