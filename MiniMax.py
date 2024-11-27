from Field import Field
from PlayerChars import PlayerChars
from typing import Self

class Node:
    def __init__(self, player, field:Field, childs:list[Self], value:int=0):
        self.player = player
        self.children:list[Self] = childs
        self.value = value
        self.field:Field = field
        self.mode = "none"

    def __str__(self):
        return f"Node(player={self.player}, value={self.value}, field={self.field}, mode={self.mode})"
    
    def __repr__(self) -> str:
        return str(self)

class MiniMax:
    RATING_OWN_PLAYER = 1
    RATING_OPPONENT = -1
    def __init__(self, field:Field, player:str):
        self.player = player
        self.field = field
        self.opponent = PlayerChars.get_opponent(player)


    def evaluate_board(self, field:Field):
        if field.is_win(self.player)[0]:
            return self.RATING_OWN_PLAYER
        elif field.is_win(self.opponent)[0]:
            return self.RATING_OPPONENT
        return 0

    def build_tree(self, player, field:Field|None=None):
        if field is None:
            field = self.field.clone()

        if not field.has_empty():
            value = self.evaluate_board(field)
            node = Node(player, field.clone(), [], value)
            return True,node

        children = []
        for x, y in field.get_empty_positions():
            sub_field = field.clone()
            sub_field.place(x, y, player)

            end, result = self.build_tree(PlayerChars.get_opponent(player), sub_field)
            children.append(result)

        value = self.evaluate_board(field)

        return False, Node(PlayerChars.get_opponent(player), field,  [] if value != 0 else children, value)
    
    def is_terminal(self, field):
        if field.is_win(self.player):
            return True
        elif field.is_win(self.opponent):
            return True
        return False


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