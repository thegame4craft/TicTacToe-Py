import random

from pygame.examples.grid import Player

from Field import Field
from MiniMax import MiniMax
from PygameRenderer import PygameRenderer
from PlayerChars import PlayerChars

class Game:
    def __init__(self):
        self.field = Field()
        self.halted = False
        self.renderer = PygameRenderer()
        self.player = PlayerChars.select_random_player()
        self.ki = MiniMax(self.field, PlayerChars.get_opponent(self.player))

    def loop(self):
        self.renderer.start()
        current_player = self.player # Player always starts
        while self.renderer.running:
            if self.halted: 
                self.renderer.tick([], True)
                continue


            if current_player == self.ki.player:
                _,tree = self.ki.build_tree(current_player)
                rate = self.ki.rate_tree(tree)
                if rate == 0:
                    x,y = random.choice(self.field.get_empty_positions())
                    input_coord = (x, y)
                else:
                    input_coord = None
                    pass
                    x, y = random.choice(self.field.get_empty_positions())
                    input_coord = (x, y)
            elif current_player == self.player:
                input_coord = self.renderer.get_input_position()
            else:
                raise Exception("Invalid player")

            if input_coord is not None:
                ic_x, ic_y = input_coord
                if self.field.get_char(ic_x, ic_y) == Field.EMPTY_CHAR:
                    self.field.place(ic_x, ic_y, current_player)
                    current_player = PlayerChars.get_opponent(current_player)

            self.renderer.tick(self.field.get_board())
            win, from_x, from_y, to_x, to_y = self.field.is_win(current_player)
            if win:
                self.halted = True
                self.renderer.draw_winner(from_x, from_y, to_x, to_y)
                self.renderer.render_text_center(f"{PlayerChars.get_opponent(current_player)} wins!")

            elif not self.field.has_empty():
                self.halted = True
                self.renderer.render_text_center("Draw!")

        self.renderer.stop()



if __name__ == "__main__":
    g = Game()
    g.loop()
