from BasePlayer import BasePlayer
from Field import Field
from MiniMax import MiniMax


class KIPlayer(BasePlayer):
    def __init__(self, player, field:Field):
        super().__init__(player)
        self.field = field
        self.ki = MiniMax(field, player)

    def select_move(self, field):
        self.ki.field = field
        return self.ki.best_move(self.player)