from Field import Field
from PlayerChars import PlayerChars
from typing import Self

class Node:
    def __init__(self, player, field:Field, childs:list[Self], value:int=0):
        self.player = player
        self.children:list[Self] = childs
        self.value = value
        self.field:Field = field

    def __str__(self):
        return f"Node(player={self.player}, value={self.value}, field={self.field})"

class MiniMax:
    RATING_OWN_PLAYER = 1
    RATING_OPPONENT = -1
    def __init__(self, field:Field, player:str):
        self.player = player
        self.field = field
        self.opponent = PlayerChars.get_opponent(player)


    def basic_rate(self, field:Field):
        value = 0
        if field.is_win(self.player)[0]:
            value = self.RATING_OWN_PLAYER
        elif field.is_win(self.opponent)[0]:
            value = self.RATING_OPPONENT
        return value

    def build_tree(self, player, field:Field|None=None):
        if field is None:
            field = self.field.clone()

        if not field.has_empty():
            value = self.basic_rate(field)
            node = Node(player, field.clone(), [], value)
            print(node)
            return True,node

        children = []
        for x, y in field.get_empty_positions():
            sub_field = field.clone()
            sub_field.place(x, y, player)

            end, result = self.build_tree(PlayerChars.get_opponent(player), sub_field)
            children.append(result)

        value = self.basic_rate(field)

        return False, Node(PlayerChars.get_opponent(player), field,  [] if value != 0 else children, value)
        pass

    def rate_tree(self, node: Node) -> int:
        if not node.children:
            return node.value


        for child in node.children:
            self.rate_tree(child)

        if node.player == self.player:
            node.value = max([c.value for c in node.children])
        else:
            node.value = min([c.value for c in node.children])