import discord
from pogobackend.settings import BOT_TOKEN

whitelist = ['Bree#2002']

guild_to_roles = {
    409418083632152577 : [616562233475989514]
}

client = discord.Client()

@client.event
async def on_ready():
    # fetch all guilds the bot belongs to.
    for guild in client.guilds:
        await guild.fetch_roles()
        # if the server_id is not in our dict server_to_role, skip it.
        if guild.id not in guild_to_roles.keys():
            continue
        # get the roles we aim to assign.
        roles = [guild.get_role(role_id) for role_id in guild_to_roles[guild.id]]
        async for member in guild.fetch_members(limit=10000):
            username = f'{member.name}#{member.discriminator}'
            if username in whitelist:
                await member.add_roles(*roles)
                print(f'gave {username}, roles {roles}')
            else:
                await member.remove_roles(*roles)
                print(f'took {username}, roles {roles}')
    exit(0)

client.run(BOT_TOKEN)