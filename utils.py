import random

alphabet = "abcdefghijklmnopqrs tuvwxyz1234567890"
VIDE, PION_BLANC, PION_NOIR, TOUR_BLANC, TOUR_NOIR, CAVALIER_BLANC, CAVALIER_NOIR, FOU_BLANC, FOU_NOIR, REINE_BLANC, REINE_NOIR, ROI_BLANC, ROI_NOIR = \
    'O', 'P', 'p', 'T', 't', 'C', 'c', 'F', 'f', 'R', 'r', 'K', 'k'


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


def coordinates_to_place(index):
    """
    Return the matching place on the board on a certain index. Index go from up to bottom and then from left to right
    :param index: int
    :return: Char[2]
    """
    y, x = index // 8, index % 8
    row = str(8 - y)
    column = chr(x + ord('a'))
    return row + column


def are_differents(piece1, piece2):
    """
    Returns True if one piece is black (lowercase) and the other is white (uppercase) and vice-versa
    Used to determine if one piece can eat the other.
    Return False otherwise
    :param piece1: Char
    :param piece2: Char
    :return: Bool
    """
    return ((piece1.isupper() and piece2.islower()) or (piece1.islower() and piece2.isupper())) or 'O' in {piece1,
                                                                                                           piece2}
