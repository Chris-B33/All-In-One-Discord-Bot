import discord
import json
from discord.ext import commands


class Server(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        with open("roles.json", "r") as roles:
            self.roles = json.load(roles)
        with open("presets.json", "r") as presets:
            self.presets = json.load(presets)

    @commands.command(
        name="create_server",
        brief="Creates categories and channels from an existing preset (1-3)",
        description='''
                Creates categories with channels inside from an existing preset specified (1-3).
                1: Small
                2: Medium
                3: Large
            '''
    )
    @commands.has_permissions(administrator=True)
    async def create_server(self, ctx, num=1):
        guild = ctx.guild
        preset = self.presets["presets"][num - 1]

        await self.create_role_from_file(guild, self.roles["admin"])
        bots = await self.create_role_from_file(guild, self.roles["bots"])
        default = await self.create_role_from_file(guild, self.roles["default"])

        for member in guild.members:
            if member.bot:
                await member.add_roles(bots)
            else:
                await member.add_roles(default)

        for category in preset["categories"]:
            cat = await guild.create_category(category["name"])
            for channel in category["channels"]:
                if channel[1] == "v":
                    await guild.create_voice_channel(name=channel[0], category=cat)
                elif channel[1] == "t":
                    await guild.create_text_channel(name=channel[0], category=cat)

    @classmethod
    def create_role_from_file(cls, server: discord.Guild, role: discord.Role):
        role = server.create_role(
            name=role["name"],
            colour=discord.Colour(int(role["colour"], base=16)),
            permissions=discord.Permissions(role["perms"]),
            hoist=role["hoist"],
            mentionable=role["mentionable"],
            reason=role["reason"]
        )
        return role