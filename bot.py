import random
import re
import sqlite3

import discord
from discord.ext import commands

from image_processing import description_to_image
from moves_check import check_move


def generate_random_name():
    name = ['c-']
    for i in range(10):
        name.append(random.choice(alphabet))
    return "".join(name)


def create_blank_game():
    """
    Sens de lecture de haut en bas puis de gauche à droite
    :return text version of blank game
    """
    tableau = [
        TOUR_NOIR, CAVALIER_NOIR, FOU_NOIR, REINE_NOIR, ROI_NOIR, FOU_NOIR, CAVALIER_NOIR, TOUR_NOIR,
        PION_NOIR * 8,
        VIDE * 8 * 4,
        PION_BLANC * 8,
        TOUR_BLANC, CAVALIER_BLANC, FOU_BLANC, REINE_BLANC, ROI_BLANC, FOU_BLANC, CAVALIER_BLANC, TOUR_BLANC
    ]
    tableau = "".join(tableau)
    return tableau


def place_to_coordinates(place):
    """
    Return a number indicating the coordinate in single-dimension array containing the description of the chess game using the place in chess
    :param place: str matching the regex [abcdefgh][12345678]
    :return: coordinate of corresponding place
    """
    letter, num = list(place)
    y = 8 - int(num)
    x = ord(letter) - ord('a')
    return 8 * y + x


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
            move = pattern_moves.search(message.content)
            if move is not None:
                move = move.group()
                game_id = channel.name
                print(game_id)
                game = cursor.execute("""SELECT * FROM games WHERE id=?""", (game_id,)).fetchone()
                player_turn = game['player_turn']
                description = list(game['description'])
                if int(message.author.id) == int(game['player' + str(player_turn)]):
                    print("C'est le tour du mec")
                    origin, dest = list(map(place_to_coordinates, move.split()))
                    origPiece = str(description[origin])
                    if origPiece != 'O' and ((origPiece.isupper() and player_turn == 1) or (
                            origPiece.islower() and player_turn == 2)) and check_move(origin, dest, description):
                        description[origin] = 'O'
                        description[dest] = origPiece
                        description = "".join(description)
                        new_player_turn = 1 if player_turn == 2 else 2

                        cursor.execute("""UPDATE games SET description = ?, player_turn = ? WHERE id = ? """,
                                       (description, new_player_turn, game_id))
                        db_conn.commit()

                        message = f"{author_display_name} a joué {move}. C'est maintenant au tour de <@{game['player' + str(new_player_turn)]}> !"
                        board_path = description_to_image(description, highlights=(origin, dest))
                        board = discord.File(board_path)
                        print("j'envoie l'image")
                        await channel.send(message, file=board)
                    else:
                        print('Mauvais mouvement:', move)
                        print("".join(description))

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
                """INSERT  INTO games (id, description, player1, player2, player_turn) VALUES (?, ?, ?, ?, ?) """,
                (room_name, new_game_description, ids[0], ids[1], 1))
            db_conn.commit()
            await ctx.send(f"La partie va commencer ! Rendez-vous sur le salon <#{new_channel.id}>")

            board_path = description_to_image(new_game_description)
            board = discord.File(board_path)
            start_text = f"Une parti d'échec va se disputer dans ce salon entre <@{ids[0]}> et <@{ids[1]}>.\nL'avancement de pièces se fait par la notation CASE_DEPART CASE_ARRIVEE, quelque soit la pièce.\nQue le meilleur gagne !"

            await new_channel.send(start_text, file=board)

        else:
            await ctx.send("Mauvais usage. !chess start @ADVERSAIRE")

    else:
        await ctx.send("Mauvais argument.")
    return


if __name__ == '__main__':
    with open('creds.txt', 'r') as creds:
        TOKEN = creds.readline()

    db_conn = sqlite3.connect('chess.db')
    db_conn.row_factory = sqlite3.Row  # Set Row to be used as dict
    cursor = db_conn.cursor()
    cursor.execute(
        """ CREATE TABLE IF NOT EXISTS games(id TEXT, description TEXT, player1 INT, player2 INT, player_turn INT) """)

    alphabet = "abcdefghijklmnopqrs tuvwxyz1234567890"
    VIDE, PION_BLANC, PION_NOIR, TOUR_BLANC, TOUR_NOIR, CAVALIER_BLANC, CAVALIER_NOIR, FOU_BLANC, FOU_NOIR, REINE_BLANC, REINE_NOIR, ROI_BLANC, ROI_NOIR = \
        'O', 'P', 'p', 'T', 't', 'C', 'c', 'F', 'f', 'R', 'r', 'K', 'k'

    pattern_moves = re.compile('[abcdefgh][12345678] [abcdefgh][12345678]')

    client.run(TOKEN)
