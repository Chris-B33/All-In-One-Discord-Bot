import discord
from discord.ext import commands


class Basic(commands.Cog):
    @commands.command(
        name="ping",
        help="Returns bot's current ping"
    )
    async def ping(self, ctx):
        ping = round(ctx.bot.latency * 1000)
        await ctx.send(f"My ping is {ping}ms.")