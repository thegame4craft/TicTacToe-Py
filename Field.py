from PlayerChars import PlayerChars


class Field:
    EMPTY_CHAR = PlayerChars.EMPTY_CHAR

    def __init__(self):
        self.__board:list[str] = [self.EMPTY_CHAR] * 9

    def get_board(self): return self.__board

    def has_empty(self) -> bool:
        return any([c == self.EMPTY_CHAR for c in self.get_board()])

    def get_empty_positions(self) -> list[tuple[int, int]]:
        return [(x, y) for x in range(3) for y in range(3) if self.get_char(x, y) == self.EMPTY_CHAR]

    def place(self, x:int, y:int, char:str)->None:
        x = max(0, min(x, 2))
        y = max(0, min(y, 2))
        idx = y * 3 + x
        self.__board[idx] = char

    def get_char(self, x:int, y:int) -> str:
        x = max(0, min(x, 2))
        y = max(0, min(y, 2))
        idx = y * 3 + x
        return self.__board[idx]


    def is_win(self, player) -> tuple[bool, int, int, int, int]:
        board = self.get_board()
        _combinations = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],
            [0, 4, 8],
            [2, 4, 6]
        ]
        for c in _combinations:
            if (board[c[0]] == player
                    and board[c[1]] == player
                    and board[c[2]] == player):
                start_x, start_y = Field.board_idx_to_xy(c[0])
                end_x, end_y = Field.board_idx_to_xy(c[2])
                return True, start_x, start_y, end_x, end_y

        return False, 0, 0, 0, 0

    @staticmethod
    def board_idx_to_xy(idx: int) -> tuple[int, int]:
        return idx % 3, idx // 3

    def clone(self):
        f = Field()
        f.__board = self.__board.copy()
        return f

    def __repr__(self):
        return str(self.__board)
