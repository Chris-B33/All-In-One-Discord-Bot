from discord.ext import commands


class Games(commands.Cog):

    def __init__(self, b):

        self.bot = b
        self.grid = []
        self.player_turn = 1
        self.score = [0, 0]
        self.replacements_c4 = {
            "o": ":o2:",
            "x": ":regional_indicator_x:",
            "-": ":white_large_square:"
        }
        self.replacements_ttt = {
            "1": ":one:",
            "2": ":two:",
            "3": ":three:",
            "4": ":four:",
            "5": ":five:",
            "6": ":six:",
            "7": ":seven:",
            "8": ":eight:",
            "9": ":nine:",
            "O": ":o2:",
            "X": ":regional_indicator_x:",
        }

    @commands.command(
        name="connect4",
        help="Plays the classic game of Connect 4 in a text channel."
    )
    async def connect4(self, ctx):
        # Initialise
        player1 = ctx.message.author
        self.player_turn = 1
        self.grid = [
            ["-", "-", "-", "-", "-", "-", "-"],
            ["-", "-", "-", "-", "-", "-", "-"],
            ["-", "-", "-", "-", "-", "-", "-"],
            ["-", "-", "-", "-", "-", "-", "-"],
            ["-", "-", "-", "-", "-", "-", "-"],
            ["-", "-", "-", "-", "-", "-", "-"]
        ]

        new_grid = self.grid[:]
        for i in range(6):
            for key, value in self.replacements_c4.items():
                new_grid[i] = [l.replace(key, value) for l in new_grid[i]]
        message = await ctx.send("\n".join(["".join(row) for row in new_grid]))

        # Start Game
        while True:
            # Take input
            await message.edit(content="\n".join(["".join(row) for row in new_grid])+f"\nPlayer {self.player_turn}, what column will you place in?")

            def check(msg):
                return msg.author == player1 and msg.channel == ctx.channel
            player_input = await self.bot.wait_for("message", check=check)
            col = int(player_input.content) - 1
            await player_input.delete()

            # Place chip
            for row in range(len(self.grid) - 1, -1, -1):
                if self.grid[row][col] == "-":
                    self.grid[row][col] = "x" if self.player_turn == 1 else "o"
                    break

            else:
                await message.edit(content="\n".join(["".join(row) for row in new_grid])+"\nCan't place there, try again!")
                continue

            # Apply rules
            def check_win(mtx):

                for y in range(5, 0, -1):
                    for x in range(7):

                        # Make sure tile isn't empty
                        tile = mtx[y][x]
                        if tile == "-":
                            continue

                        # Check cols
                        if y - 3 > 0:
                            for i in range(4):
                                if not mtx[y - i][x] == tile:
                                    break
                            else:
                                return 1

                        # Check rows
                        if x + 3 < len(self.grid[0]):
                            for i in range(4):
                                if not mtx[y][x + i] == tile:
                                    break
                            else:
                                return 1

                        # Check diagonal up
                        if x + 3 < len(self.grid[0]) and y - 3 > 0:
                            for i in range(4):
                                if not mtx[y - i][x + i] == tile:
                                    break
                            else:
                                return 1

                        # Check diagonals down
                        if x + 3 < len(self.grid[0]) and y + 3 < len(self.grid):
                            for i in range(4):
                                if not mtx[y + i][x + i] == tile:
                                    break
                            else:
                                return 1
                return 0

            condition = check_win(self.grid)

            # Update Grid
            new_grid = self.grid[:]
            for i in range(6):
                for key, value in self.replacements_c4.items():
                    new_grid[i] = "".join([l.replace(key, value) for l in new_grid[i]])
            await message.edit(content="\n".join(["".join(row) for row in new_grid]))

            # Print output
            if condition == 1:
                await message.edit(content="\n".join(["".join(row) for row in new_grid])+f"\nPlayer {self.player_turn} wins!")
                return
            else:
                self.player_turn = 2 if self.player_turn == 1 else 1
                continue
