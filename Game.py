import random

from pygame.examples.grid import Player

from Field import Field
from MiniMax import MiniMax
from PygameRenderer import PygameRenderer
from PlayerChars import PlayerChars
from colors import TEXT_COLOR


class Game:
    def __init__(self):
        self.field = Field()
        self.halted = False
        self.renderer = PygameRenderer()
        self.player = PlayerChars.select_random_player()
        self.ki = MiniMax(self.field, PlayerChars.get_opponent(self.player))

    # Place a stone on the field returns true if successful
    def place(self, input_coord, current_player):
        if input_coord is None: return False
        ic_x, ic_y = input_coord
        if self.field.get_char(ic_x, ic_y) == Field.EMPTY_CHAR:
            self.field.place(ic_x, ic_y, current_player)
            return True
        return False

    def loop(self):
        self.renderer.start()
        current_player = self.player # Player always starts
        while self.renderer.running:
            pull_reset = self.renderer.pull_reset()
            if pull_reset and self.halted:
                self.field = Field()
                self.halted = False
                self.player = PlayerChars.get_opponent(self.player)
                self.ki = MiniMax(self.field, PlayerChars.get_opponent(self.player))
                current_player = self.player
                self.renderer.tick(self.field.get_board())
                continue

            if self.halted: 
                self.renderer.tick([], True)
                continue


            if current_player == self.ki.player:
                input_coord = self.ki.best_move(self.ki.player)
                if input_coord == (-1, -1):
                    self.halted = True
                    self.renderer.render_text_center("ERROR", TEXT_COLOR)
                    continue
                if self.place(input_coord, current_player):
                    current_player = PlayerChars.get_opponent(current_player)
            elif current_player == self.player:
                input_coord = self.renderer.get_input_position()
                if self.place(input_coord, current_player):
                    current_player = PlayerChars.get_opponent(current_player)
            else:
                raise Exception("Invalid player")

            self.renderer.tick(self.field.get_board())

            win_player, from_x, from_y, to_x, to_y = self.field.is_win(self.player)
            if win_player:
                self.halted = True
                self.renderer.draw_winner(from_x, from_y, to_x, to_y)
                self.renderer.render_text_center(f"You win!\n\nPress SPACE \nto restart", TEXT_COLOR)

            win_ki, from_x, from_y, to_x, to_y = self.field.is_win(self.ki.player)
            if win_ki:
                self.halted = True
                self.renderer.draw_winner(from_x, from_y, to_x, to_y)
                self.renderer.render_text_center(f"AI wins!\n\nPress SPACE \nto restart",TEXT_COLOR)

            if not self.field.has_empty():
                self.halted = True
                self.renderer.render_text_center("Draw!\n\nPress SPACE\n to restart", TEXT_COLOR)

            self.renderer.update_display()

        self.renderer.stop()



if __name__ == "__main__":
    g = Game()
    g.loop()
