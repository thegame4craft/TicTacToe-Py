import random


class PlayerChars:
    PLAYER_X = "X"
    PLAYER_O = "O"
    EMPTY_CHAR = " "

    @staticmethod
    def get_opponent(player:str) -> str:
        return PlayerChars.PLAYER_O if player == PlayerChars.PLAYER_X else PlayerChars.PLAYER_X

    @staticmethod
    def select_random_player() -> str:
        return random.choice([PlayerChars.PLAYER_X, PlayerChars.PLAYER_O])

