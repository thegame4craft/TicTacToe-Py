class Field:
    board:list[str] = [" "] * 9

    def place(self, x:int, y:int, char:str)->None:
        x = max(0, min(x, 2))
        y = max(0, min(y, 2))
        idx = y * 3 + x
        self.board[idx] = char

    def get_char(self, x:int, y:int) -> str:
        x = max(0, min(x, 2))
        y = max(0, min(y, 2))
        idx = y * 3 + x
        return self.board[idx]
