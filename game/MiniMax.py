from Field import Field
from PlayerChars import PlayerChars


class MiniMax:
    RATING_OWN_PLAYER = 1
    RATING_OPPONENT = -1
    def __init__(self, field:Field, player:str):
        self.player = player
        self.field = field
        self.opponent = PlayerChars.get_opponent(player)


    def minimax(self, field:Field, depth, is_maximizing):
        if field.is_win(self.player)[0]:
            return 1
        elif field.is_win(self.opponent)[0]:
            return -1
        elif not field.has_empty():
            return 0

        if is_maximizing:
            best_score = -float('inf')
            for x, y in field.get_empty_positions():
                field.place(x, y, self.player)
                score = self.minimax(field, depth + 1, False)
                field.place(x, y, Field.EMPTY_CHAR)
                best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for x, y in field.get_empty_positions():
                field.place(x, y, self.opponent)
                score = self.minimax(field, depth + 1, True)
                field.place(x, y, Field.EMPTY_CHAR)
                best_score = min(score, best_score)
            return best_score
        
    def best_move(self, player: str) -> tuple[int, int]:
        best_score = -float('inf')
        move = (-1, -1)
        for x, y in self.field.get_empty_positions():
            self.field.place(x, y, player)
            score = self.minimax(self.field, 0, False)
            self.field.place(x, y, Field.EMPTY_CHAR)
            if score > best_score:
                best_score = score
                move = (x, y)
        return move