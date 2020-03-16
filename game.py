import image_processing
import moves_check
from utils import *


class Game:
    def __init__(self, player1_id, player2_id, player_turn, description, last_move, king_moved):
        self.player1_id, self.player2_id, self.player_turn, self.description = player1_id, player2_id, player_turn, list(
            description)
        self.playing_user_id = self.player1_id if player_turn == 1 else self.player2_id

    def get_image(self, highligths=set(), highlight_color="Gold"):
        image_path = image_processing.description_to_image(self.description, highligths, highlight_color)
        return image_path

    def make_move(self, move):
        origin, dest = map(place_to_coordinates, move.split())
        origPiece = self.description[origin]
        if origPiece != 'O' and ((origPiece.isupper() and self.player_turn == 1) or (
                origPiece.islower() and self.player_turn == 2)) and moves_check.check_move(origin, dest,
                                                                                           self.description):
            self.description[origin] = 'O'
            self.description[dest] = origPiece
            self.player_turn = 1 if self.player_turn == 2 else 2

            return self.get_image((origin, dest), 'gold')

    def prepare_update_db(self):
        infos = [self.]
