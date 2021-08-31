import discord
import logging
from discord.ext import commands
from lib.music import Music
from lib.basic import Basic
from lib.server import Server


class MyBot(commands.Bot):

    async def on_ready(self):
        print("Connected!")
        await bot.change_presence(activity=discord.Activity(
            type=discord.ActivityType.watching,
            name='you...'))

    async def on_message(self, message):
        if message.author == bot.user:
            return
        await bot.process_commands(message)

    async def on_member_join(self, member):
        await member.send("Welcome!")


if __name__ == "__main__":
    logger = logging.getLogger('discord')
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)

    with open("art.txt", "r") as art:
        print(art.read())

    bot = MyBot(command_prefix="a!")
    bot.add_cog(Basic())
    bot.add_cog(Music(bot))
    bot.add_cog(Server(bot))
    token = open("token.txt", "r").read()
    bot.run(token)
