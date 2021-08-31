import discord

# Draw Art
with open("art.txt", "r") as art:
    print(art.read())


class MyClient(discord.Client):

    @staticmethod
    async def on_ready():
        print("Connected!")

    @staticmethod
    async def on_message(ctx):
        await ctx.send("Found message!")


if __name__ == "__main__":
    client = MyClient()
    token = open("token.txt", "r").read()
    client.run(token)
