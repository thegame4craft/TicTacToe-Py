from BasePlayer import BasePlayer
from PygameRenderer import PygameRenderer


class HumanPlayer(BasePlayer):
    def __init__(self, player:str):
        super().__init__(player)

    def select_move(self, field):
        return PygameRenderer.get_input_position()