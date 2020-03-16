import time

from PIL import Image

"""
Taille pièce original: 60x60
Taille pièce voulue: 135x135
Taille plateau 1080x1080

"""


def description_to_image(description, highlights=set(), highlight_color="Gold"):
    """
    Transform a description of a game to a corresponding image using PIL library
    :param description: description of game using the format of ChessBot
    :return: path of newly created image
    """

    image = Image.open('./Ressources/empty_board.jpg')
    for y in range(8):
        for x in range(8):
            piece = description[x + (8 * y)]
            if (8 * y) + x in highlights:
                highlight_img = Image.open('./Ressources/highlight_' + highlight_color.lower() + '.png')
                image.paste(highlight_img, (135 * x, 135 * y))
            if piece != 'O':
                piece_img = Image.open('./Ressources/' + piece + '.png')
                piece_img = piece_img.resize((135, 135))
                image.paste(piece_img, (135 * x, 135 * y), piece_img)

    path = './Ressources/Boards/' + str(int(time.time())) + '.png'
    image.save(path)
    return path


if __name__ == '_main__':
    print(description_to_image('R' * 64))
