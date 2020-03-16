import re
import sqlite3

import discord
from discord.ext import commands

import game
from utils import *

client = commands.Bot(command_prefix='!', description="Aujourd'hui j'ai mangé un fou")


async def get_games_category(guild):
    """
    Returns the category named Games of the guild. Create it if it doesn't exists
    :param guild: guild object
    :return: Games category channel
    """
    categories = guild.categories
    for c in categories:
        if c.name == "Games":
            return c

    c = await guild.create_category("Games", reason="Games channel doesn't exist and is needed for ChessBot")
    return c


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    if not message.author.bot:
        author_display_name = message.author.display_name
        print(f"{author_display_name} > {message.clean_content}")

        channel = message.channel
        if channel.name.startswith('c-') and len(
                channel.name) == 12 and channel.category.name == "Games":  # Is an adequate channel for the game, not perfect but good enough
            move = pattern_moves.match(message.content)
            if move is not None:
                move = move.group()
                game_id = channel.name
                print(game_id)

                if game_id in saved_games.keys():
                    chess_game = saved_games[game_id]
                else:
                    game_infos = cursor.execute("""SELECT * FROM games WHERE id=?""", (game_id,)).fetchone()
                    chess_game = game.Game(game_infos['player1'], game_infos['player2'], game_infos['player_turn'],
                                           game_infos['description'], game_infos['last_move'],
                                           game_infos['king1_moved'], game_infos['king2_moved'])

                if message.author.id == chess_game.playing_user_id:
                    board_path = chess_game.make_move(move)
                    if board_path is not None:
                        board = discord.File(board_path)
                        print("Mouvement valide. J'envoie le message")
                        await channel.send(message, file=board)

                        updated_infos = chess_game.prepare_update_db()
                        cursor.execute(
                            """UPDATE games SET description = ?, player_turn = ?, last_move = ?, king1_mobed = ?, king2_moved = ? WHERE id = ?""",
                            (*updated_infos, game_id))
                        db_conn.commit()

                    else:
                        print('Le mouvement n\'est pas valide:', move)
                        print("".join(chess_game.description))

    await client.process_commands(message)


@client.command()
async def ping(ctx):
    await ctx.send("Hey salut")


@client.command()
async def say(ctx, *args):
    await ctx.send(" ".join(args))


@client.command()
async def chess(ctx, *args):
    arg = args[0]
    if arg == 'start':
        if len(args) == 2 and len(ctx.message.mentions) == 1:
            room_name = generate_random_name()
            guild = ctx.guild
            games_channel = await get_games_category(guild)
            new_channel = await guild.create_text_channel(room_name, category=games_channel,
                                                          reason="Created chess channel for ChessBot")
            new_game_description = create_blank_game()
            other_id = ctx.message.mentions[0].id
            ids = [int(ctx.author.id), int(other_id)]
            random.shuffle(ids)
            cursor.execute(
                """INSERT  INTO games (id, description, player1, player2, player_turn, last_move, king_moved) VALUES (?, ?, ?, ?, ?, ?, ?) """,
                (room_name, new_game_description, ids[0], ids[1], 1, "", 0, 0))
            db_conn.commit()
            await ctx.send(f"La partie va commencer ! Rendez-vous sur le salon <#{new_channel.id}>")

            new_game = game.Game(ids[0], ids[1], 1, new_game_description, "", 0, 0)
            saved_games[room_name] = new_game
            board_path = new_game.get_image()

            board = discord.File(board_path)
            start_text = f"Une parti d'échec va se disputer dans ce salon entre <@{new_game.player1_id}> et <@{new_game.player2_id}>.\nL'avancement de pièces se fait par la notation CASE_DEPART CASE_ARRIVEE, quelque soit la pièce.\nQue le meilleur gagne !"

            await new_channel.send(start_text, file=board)

        else:
            await ctx.send("Mauvais usage. !chess start @ADVERSAIRE")

    else:
        await ctx.send("Mauvais argument.")
    return


if __name__ == '__main__':
    with open('creds.txt', 'r') as creds:
        TOKEN = creds.readline()

    saved_games = dict()

    db_conn = sqlite3.connect('chess.db')
    db_conn.row_factory = sqlite3.Row  # Set Row to be used as dict
    cursor = db_conn.cursor()
    cursor.execute(
        """ CREATE TABLE IF NOT EXISTS games(id TEXT, description TEXT, player1 INT, player2 INT, player_turn INT, last_move TEXT, king1_moved INT, king2_moved) """)

    pattern_moves = re.compile('[abcdefgh][12345678] [abcdefgh][12345678]')

    client.run(TOKEN)
