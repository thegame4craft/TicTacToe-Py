from PlayerChars import PlayerChars


class BasePlayer:
    def __init__(self, player):
        self.player = player
        self.opponent = PlayerChars.get_opponent(player)

    def select_move(self, field):
        raise NotImplementedError()
