from discord.ext import commands
import discord
import aiohttp
import enum

class BotMode(enum.Enum):
    UPDATE = 0,
    FETCH_IDS = 1,
    IDLE = 2

class RoleBot(commands.Bot):

    def __init__(self, guild_to_roles=None, members=None, username_to_id=None):
        super().__init__(command_prefix=["/"], description="", pm_help=None,
                         help_attrs=dict(hidden=True))
        self.session = aiohttp.ClientSession(loop=self.loop)
        self.guild_to_roles = guild_to_roles
        self.members = members
        self.username_to_id = username_to_id
        if guild_to_roles is not None and self.members is not None:
            self.mode = BotMode.UPDATE
        elif username_to_id is not None:
            self.mode = BotMode.FETCH_IDS
        else:
            self.mode = BotMode.IDLE

    async def on_ready(self):
        if self.mode != BotMode.IDLE:
            # fetch all guilds the bot belongs to.
            for guild in self.guilds:
                await guild.fetch_roles()
                # if the server_id is not in our dict server_to_role, skip it.
                if self.guild_to_roles is not None and guild.id not in self.guild_to_roles.keys():
                    continue
                # get the roles we aim to assign.
                if self.guild_to_roles is not None:
                    roles = [guild.get_role(role_id) for role_id in self.guild_to_roles[guild.id]]
                async for member in guild.fetch_members(limit=10000):
                    if self.mode == BotMode.UPDATE:
                        # if the id is in our memberlist, we give him the desired roles.
                        if self.members is not None and member.id in self.members:
                            await member.add_roles(*roles)
                            print(f'gave {member.name}, roles {roles}')
                        else:
                            await member.remove_roles(*roles)
                            print(f'took {member.name}, roles {roles}')
                    elif self.mode == BotMode.FETCH_IDS:
                        username = f'{member.name}#{member.discriminator}'
                        self.username_to_id[username.replace(' ','').encode('ascii', 'ignore').decode("utf-8").lower()] = member.id
        await self.session.close()
        await self.logout()
