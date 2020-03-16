from utils import are_differents, place_to_coordinates, coordinates_to_place


def check_pion(orig, dest, description, king1_moved, king2_moved, last_move):
    print(f'Check pion from {orig}')

    piece = description[orig]
    if piece.isupper():  # White
        mouvement = orig - dest
    else:  # Black
        mouvement = dest - orig

    if mouvement == 8 and description[dest] == 'O':  # The pawn go up by one case and the case if free
        return True
    if mouvement == 7 or mouvement == 9:
        if are_differents(piece, description[dest]) and description[dest] != 'O':  # The pawn can eat in diagonal
            return True

    if mouvement == 2 * 8:
        if piece.isupper() and orig % 8 == 6 and description[dest] == description[
            dest - 8] == 'O':  # Is on row 6 and white
            return True

        if piece.islower() and orig % 8 == 1 and description[dest] == description[
            dest + 8] == 'O':  # Is on row 1 and black
            return True

    return False


def check_en_passant(orig, dest, description, last_move):
    if description[orig] == 'P' and description[dest] == 'O':  # White pawn
        mouvement = orig - dest
        expected_last_move = coordinates_to_place(dest) + ' ' + coordinates_to_place(dest - 8)

    elif description[orig] == 'p' and description[dest] == 'O':  # Black pawn
        mouvement = dest - orig
        expected_last_move = coordinates_to_place(dest) + ' ' + coordinates_to_place(dest + 8)

    if mouvement in (7, 9) and description[dest - 8] == 'p' and expected_last_move == last_move:
        return True

    return False


def check_cavalier(orig, dest, description, king1_moved, king2_moved, last_move):
    print(f'Check cavalier from {orig}')
    possible_moves = [-2 + 8, -2 - 8, 2 + 8, 2 - 8, 16 - 1, 16 + 1, -16 - 1,
                      -16 + 1]  # Get all legal differences of dest - orig for this piece
    return dest - orig in possible_moves and are_differents(description[orig], description[dest])


def check_fou(orig, dest, description, king1_moved, king2_moved, last_move):
    print(f'Check fou from {orig} to {dest}')
    yOrig, xOrig = orig // 8, orig % 8
    yDest, xDest = dest // 8, dest % 8
    print(yOrig, xOrig)
    print(yDest, xDest)
    if abs(yOrig - yDest) == abs(
            xOrig - xDest) and orig != dest:  # Same offset for both axis (=is a diagonal) and not the same case
        print("Diagonal ok")
        # To upper left
        if yDest < yOrig and xDest < xOrig:
            print("-Upper left diago")
            for i in range(1, yOrig - yDest):
                newY, newX = yOrig - i, xOrig - i
                if description[8 * newY + newX] != 'O':
                    return False

        # To upper right
        if yDest < yOrig and xDest > xOrig:
            print('-Upper right diago')
            for i in range(1, yOrig - yDest):
                newY, newX = yOrig - i, xOrig + i
                if description[8 * newY + newX] != 'O':
                    print(f'-Not empty cell on {newY}:{newX}')
                    return False

        # To lower left
        if yDest > yOrig and xDest < xOrig:
            print('-Lower left diago')
            for i in range(1, yDest - yOrig):
                newY, newX = yOrig + i, xOrig - i
                if description[8 * newY + newX] != 'O':
                    return False

        # To lower right
        if yDest > yOrig and xDest < xOrig:
            print('-Lower right diago')
            for i in range(1, yOrig - yDest):
                newY, newX = yOrig - i, xOrig - i
                if description[8 * newY + newX] != 'O':
                    return False
        # All cases are empty beetwen orig and dest

        if are_differents(description[orig], description[dest]):
            return True

    return False


def check_roi(orig, dest, description, king1_moved, king2_moved, last_move):
    print(f'Check roi from {orig}')
    possible_mouvements = [-8 - 1, -8, -8 + 1, -1, 1, 8 - 1, 8, 8 + 1]  # All 8 possible mouvement from a King
    if dest - orig in possible_mouvements and are_differents(description[orig], description[dest]):
        return True
    return False


def check_tour(orig, dest, description, king1_moved, king2_moved, last_move):
    print(f'Check tour from {orig} to {dest}')
    yOrig, xOrig = orig // 8, orig % 8
    yDest, xDest = dest // 8, dest % 8
    if yOrig == yDest and xOrig != xDest:  # Movements in a horizontal line
        print('Horizontal line')
        # To the left
        if xOrig > xDest:
            print('To the left')
            for i in range(1, xOrig - xDest):
                newY, newX = yOrig, xOrig - i
                if description[8 * newY + newX] != 'O':
                    return False

        # To the right
        if xOrig < xDest:
            print('To the right')
            for i in range(1, xDest - xOrig):
                newY, newX = yOrig, xOrig + i
                if description[8 * newY + newX] != 'O':
                    return False

        if are_differents(description[orig], description[dest]):
            return True

    if xOrig == xDest and yOrig != yDest:  # Movements in a vertical line
        print("Vertical line")
        # Up
        if yOrig > yDest:
            print('-Up')
            for i in range(1, yOrig - yDest):
                newY, newX = yOrig - i, xOrig
                if description[8 * newY + newX] != 'O':
                    return False

        # Down
        if xOrig < xDest:
            print('Down')
            for i in range(1, xDest - xOrig):
                newY, newX = yOrig + i, xOrig
                if description[8 * newY + newX] != 'O':
                    return False

        if are_differents(description[orig], description[dest]):
            return True

    return False


def check_reine(orig, dest, description, king1_moved, king2_moved, last_move):
    print(f'Check reine from {orig}')
    if check_fou(orig, dest, description, king1_moved, king2_moved, last_move) or check_tour(orig, dest, description,
                                                                                             king1_moved, king2_moved,
                                                                                             last_move):
        return True
    return False


def piece_not_found(orig, dest, description, king1_moved, king2_moved, last_move):
    error_message = f"KeyError: Piece {description[orig]} not supported and not in handler dict."
    raise Exception(error_message)


move_handler = {
    'P': check_pion,
    'p': check_pion,
    'C': check_cavalier,
    'c': check_cavalier,
    'F': check_fou,
    'f': check_fou,
    'K': check_roi,
    'k': check_roi,
    'R': check_reine,
    'r': check_reine,
    'T': check_tour,
    't': check_tour
}


def check_move(orig, dest, description, king1_moved, king2_moved, last_move):
    """
    Test if move is legal in chess in the configuration of description argiment
    Coordinates are the index in description of the corresponding piece, NOT the formated chess coordinates
    :param orig: coordinate of origin piece, we assume the color of the player is the same as the piece's color
    :param dest: coordinate of destination place
    :param description: represent state of the board, before the actual move
    :return: True if the move is legal, False otherwise
    """
    is_possible = move_handler.get(description[orig], piece_not_found)(orig, dest, description, king1_moved,
                                                                       king2_moved, last_move) and orig != dest

    return is_possible


def piece_menaced(piece_coordinate, description):
    """
    Check if piece at `piece_coordinate` is under the menace of an enemy piece. Is used to see if there is check
    :param piece_coordinate: index of piece in description
    :param description: Array corresponding to the board
    :return: bool
    """
    for coord, piece in enumerate(description):
        if piece != 'O':
            can_eat = check_move(coord, piece_coordinate, description)
            if can_eat:
                return True
    return False


if __name__ == '__main__':
    description1 = "tOfOTfctOOppOpppcpOOOOOOpOOOpOOOPOOOPOOrOPOOOOOOOOPPOPPPOCFRKFCO"
    orig1 = place_to_coordinates('d1')
    dest1 = place_to_coordinates('h5')
    print(check_move(orig1, dest1, description1))

    orig2 = place_to_coordinates('a6')
    dest2 = place_to_coordinates('c6')
    description2 = "OcfrkfctOpppOppptOOOFOOOpOOOOOOOOOOOOOOOOOOKPOOOPPPPCPPPTCFROOOT"
    print(check_move(orig2, dest2, description2))
