import discord
import time
from discord.ext import commands


class Basic(commands.Cog):
    @commands.command(
        name="ping",
        help="Returns bot's current ping"
    )
    async def ping(self, ctx):
        ping = round(ctx.bot.latency * 1000)
        await ctx.send(f"My ping is {ping}ms.")

    @commands.command(
        name="test",
        help="Checks if bot is operational."
    )
    async def test(self, ctx):
        await ctx.send("Hello? Yes, I can hear you!")

    @commands.command(
        name="time",
        help="Returns the time from AIO's region."
    )
    async def time(self, ctx):
        local_time = time.localtime(time.time())
        await ctx.send(f"It is currently {local_time[3]}:{local_time[4]} in my region (GMT+1).")
