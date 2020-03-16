from utils import *


def check_pion(orig, dest, description, moved_pieces, last_move):
    print(f'Check pion from {orig}')

    piece = description[orig]
    if piece.isupper():  # White
        mouvement = orig - dest
    else:  # Black
        mouvement = dest - orig

    if mouvement == 8 and description[dest] == 'O':  # The pawn go up by one case and the case if free
        return True
    if mouvement == 7 or mouvement == 9:
        if can_go_to(piece, description[dest]) and description[dest] != 'O':  # The pawn can eat in diagonal
            return True

    if mouvement == 2 * 8:
        # print(orig % 8)
        if piece.isupper() and orig // 8 == 6 and description[dest] == description[
            dest + 8] == 'O':  # Is on row 6 and white
            return True

        if piece.islower() and orig // 8 == 1 and description[dest] == description[
            dest - 8] == 'O':  # Is on row 1 and black
            return True

    return False


def check_en_passant(orig, dest, description, last_move):
    print(f"Check en passant from {orig} with last_move = {last_move}")
    if description[orig] == 'P' and description[dest] == 'O':  # White pawn
        mouvement = orig - dest
        expected_last_move = coordinates_to_place(dest - 8) + ' ' + coordinates_to_place(dest + 8)
        enemy_pawn = 'p'
        if mouvement == 7 and description[dest + 8] == enemy_pawn and expected_last_move == last_move:
            return True

    elif description[orig] == 'p' and description[dest] == 'O':  # Black pawn
        mouvement = dest - orig
        expected_last_move = coordinates_to_place(dest + 8) + ' ' + coordinates_to_place(dest - 8)
        enemy_pawn = 'P'
        # print(expected_last_move)
        # print(description[dest - 8])
        if mouvement in (7, 9) and description[dest - 8] == enemy_pawn and expected_last_move == last_move:
            return True

    return False


def check_cavalier(orig, dest, description, moved_pieces, last_move):
    print(f'Check cavalier from {orig}')
    possible_moves = [-2 + 8, -2 - 8, 2 + 8, 2 - 8, 16 - 1, 16 + 1, -16 - 1,
                      -16 + 1]  # Get all legal differences of dest - orig for this piece
    return dest - orig in possible_moves and can_go_to(description[orig], description[dest])


def check_fou(orig, dest, description, moved_pieces, last_move):
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

        if can_go_to(description[orig], description[dest]):
            return True

    return False


def check_roi(orig, dest, description, moved_pieces, last_move):
    print(f'Check roi from {orig}')
    possible_mouvements = [-8 - 1, -8, -8 + 1, -1, 1, 8 - 1, 8, 8 + 1]  # All 8 possible mouvement from a King
    if dest - orig in possible_mouvements and can_go_to(description[orig], description[dest]):
        return True
    return False


def check_roque(orig, dest, description, moved_pieces, last_move):
    """
    Check if roque is possible beetwen orig and dest. orig is the king involved and dest is the rook. Returns True if possible
    :param orig: index of the piece (usually King)
    :param dest: index of the rook
    :param description: state of the board
    :param moved_pieces: list of all moved pieces
    :return: True if roque possible, False otherwise
    """
    print(f"Check roque from {orig} to {dest}")
    if description[orig].upper() == 'K' and moved_pieces[orig] == '0' and description[dest].upper() == 'T' and \
            moved_pieces[
                dest] == '0':  # Check if orig and dest are respectively King and Rook, and check if they didn't moved
        if orig > dest:
            low = dest
            high = orig
        elif orig < dest:
            low = orig
            high = dest

        for i in range(low + 1, high):
            if description[i] != 'O' or piece_menaced(i, description, moved_pieces, last_move):
                return False
        return True
    return False


def check_tour(orig, dest, description, moved_pieces, last_move):
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

        if can_go_to(description[orig], description[dest]):
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

        if can_go_to(description[orig], description[dest]):
            return True

    return False


def check_reine(orig, dest, description, moved_pieces, last_move):
    print(f'Check reine from {orig}')
    if check_fou(orig, dest, description, moved_pieces, last_move) or check_tour(orig, dest, description,
                                                                                 moved_pieces,
                                                                                 last_move):
        return True
    return False


def piece_not_found(orig, dest, description, moved_pieces, last_move):
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


def check_move(orig, dest, description, moved_pieces, last_move):
    """
    Test if move is legal in chess in the configuration of description argiment
    Coordinates are the index in description of the corresponding piece, NOT the formated chess coordinates
    :param orig: coordinate of origin piece, we assume the color of the player is the same as the piece's color
    :param dest: coordinate of destination place
    :param description: represent state of the board, before the actual move
    :return: True if the move is legal, False otherwise
    """
    is_possible = move_handler.get(description[orig], piece_not_found)(orig, dest, description, moved_pieces,
                                                                       last_move) and orig != dest

    future_description = list(description)
    future_description[dest] = orig
    future_description[orig] = 'O'
    future_moved_pieces = list(moved_pieces)
    future_moved_pieces[dest], future_moved_pieces[orig] = '1'
    future_last_move = coordinates_to_place(orig) + ' ' + coordinates_to_place(dest)

    king_coordinates = description.index('K' if description[orig].isupper() else 'k')
    is_possible = is_possible and not piece_menaced(king_coordinates, future_description, future_moved_pieces,
                                                    future_last_move)

    return is_possible


def piece_menaced(piece_coordinate, description, moved_pieces, last_move):
    """
    Check if piece at `piece_coordinate` is under the menace of an enemy piece. Is used to see if there is check(mate)
    :param piece_coordinate: index of piece in description
    :param description: Array corresponding to the board
    :param moved_pieces: list of all moved pieces
    :return: bool
    """
    focused_piece = description[piece_coordinate]
    for coord, piece in enumerate(description):
        if are_differents(focused_piece, piece):
            can_eat = check_move(coord, piece_coordinate, description, moved_pieces, last_move)
            if can_eat:
                return True
    return False


def is_checkmate(king_coordinate, description, moved_pieces, last_move):
    """
    Check all possible moves to see if a certain piece is checkmate (alias nothing can
    :param king_coordinate:
    :param description:
    :return: Bool


    Procédure:
        Pour tout les mouvements possibles de l'équipe du roi:
            Si le roi n'est plus échec:
                :return True
    """

    for piece_coordinate, piece in enumerate(description):
        if are_differents(description[king_coordinate], piece) or piece == 'O':  # Pass if not the same color or empty
            continue

        for new_coord in range(64):
            if check_move(piece_coordinate, new_coord, moved_pieces, last_move) and not piece_menaced(king_coordinate,
                                                                                                      description,
                                                                                                      moved_pieces,
                                                                                                      last_move):
                return False

    return True


if __name__ == '__main__':
    NO_MOVES = '0' * 64

    orig1 = place_to_coordinates('d1')
    dest1 = place_to_coordinates('h5')
    description1 = "tOfOTfctOOppOpppcpOOOOOOpOOOpOOOPOOOPOOrOPOOOOOOOOPPOPPPOCFRKFCO"
    print(check_move(orig1, dest1, description1, NO_MOVES, ''))
    print('==========================================================================')
    orig2 = place_to_coordinates('a6')
    dest2 = place_to_coordinates('c6')
    description2 = "OcfrkfctOpppOppptOOOFOOOpOOOOOOOOOOOOOOOOOOKPOOOPPPPCPPPTCFROOOT"
    print(check_move(orig2, dest2, description2, NO_MOVES, ''))
    print('==========================================================================')
    orig3 = place_to_coordinates('a7')
    dest3 = place_to_coordinates('a5')
    description3 = "tcfrkfctppppppppOOOOOOOOOOOOOOOOOOOOPOOOOOOOOOOOPPPPOPPPTCFRKFCT"
    print(check_move(orig3, dest3, description3, NO_MOVES, ''))
    print("==========================================================================")
    orig4 = place_to_coordinates('b4')
    dest4 = place_to_coordinates('a3')
    description4 = "tcfrkfctpOppOpppOOOOpOOOOOOOOOOOPpOOPOOOOOOPOPOOOPPOOOPPTCFRKFCT"
    last_move4 = 'a2 a4'
    print(check_en_passant(orig4, dest4, description4, last_move4))
    print('==========================================================================')
    orig5 = place_to_coordinates('e1')
    dest5 = place_to_coordinates('h1')
    description5 = 'tcfOkfctpOppOpppOpOOOOOOOOOOpOOOOOOOPOOrOOOFOCOOPPPPOPPPTCFRKOOT'
    print(check_roque(orig5, dest5, description5, NO_MOVES, ''))
    print('==========================================================================')
    orig6 = place_to_coordinates('e8')
    dest6 = place_to_coordinates('a8')
    description6 = 'tOOOkfOtpppOOpppOOcpOOOcOOOOpOOOOOFOPOOCOOOPOOOPPPPOOPPOTOFCKOOT'
    print(check_roque(orig6, dest6, description6, NO_MOVES, ''))
