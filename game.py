import image_processing
import moves_check
from utils import *


class Game:
    def __init__(self, player1_id, player2_id, player_turn, description, last_move, moved_pieces):
        self.player1_id, self.player2_id, self.player_turn, self.description = player1_id, player2_id, player_turn, list(
            description)
        self.last_move, self.moved_pieces = last_move, list(moved_pieces)
        self.playing_user_id = self.player1_id if player_turn == 1 else self.player2_id

    def get_image(self, highligths=set()):
        image_path = image_processing.description_to_image(self.description, highligths)
        return image_path

    def make_move(self, move):

        origin, dest = map(place_to_coordinates, move.split())
        origPiece = self.description[origin]
        destPiece = self.description[dest]

        en_passant = moves_check.check_en_passant(origin, dest, self.description, self.last_move)
        roque = moves_check.check_roque(origin, dest, self.description, self.moved_pieces, self.last_move)

        if origPiece != 'O' and ((origPiece.isupper() and self.player_turn == 1) or (
                origPiece.islower() and self.player_turn == 2)) and (
                moves_check.check_move(origin, dest, self.description, self.moved_pieces,
                                       self.last_move) or en_passant or roque):
            self.description[origin] = 'O'
            self.description[dest] = origPiece

            if en_passant:
                if self.player_turn == 1:
                    self.description[dest + 8] = 'O'
                else:
                    self.description[dest - 8] = 'O'

            if roque:
                if origin > dest:
                    self.description[origin - 1] = destPiece
                    self.description[origin - 2] = origPiece
                else:
                    self.description[origin + 1] = destPiece
                    self.description[origin + 2] = origPiece

                self.description[dest] = 'O'  # Cancels the usual move

            self.player_turn = 1 if self.player_turn == 2 else 2
            self.playing_user_id = self.player1_id if self.player_turn == 1 else self.player2_id
            self.last_move = move
            self.moved_pieces[origin] = '1'
            self.moved_pieces[dest] = '1'

            higlights = [(origin, 'gold'), (dest, 'gold')]
            enemy_king = 'K' if origPiece.islower() else 'k'
            enemy_king_coordinates = self.description.index(enemy_king)
            if moves_check.piece_menaced(enemy_king_coordinates, self.description, self.moved_pieces, self.last_move):
                higlights.append((enemy_king_coordinates, 'red'))

            return self.get_image(higlights)

    def prepare_update_db(self):
        infos = ["".join(self.description), self.player_turn, self.last_move, "".join(self.moved_pieces)]
        return infos
