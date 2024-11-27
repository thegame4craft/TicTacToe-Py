import random

from BasePlayer import BasePlayer
from Field import Field
from HumanPlayer import HumanPlayer
from KIPlayer import KIPlayer
from PygameRenderer import PygameRenderer
from PlayerChars import PlayerChars
from colors import TEXT_COLOR


class Game:
    def __init__(self):
        self.field = Field()
        self.halted = False
        self.renderer = PygameRenderer()

        self.players = {}
        self.current_player: BasePlayer | None = None
        self.attach_players()

    # Place a stone on the field returns true if successful
    def place(self, input_coord:tuple[int,int], current_player:BasePlayer):
        if input_coord is None: return False
        ic_x, ic_y = input_coord
        if self.field.get_char(ic_x, ic_y) == Field.EMPTY_CHAR:
            self.field.place(ic_x, ic_y, current_player.player)
            return True
        return False

    def attach_players(self):
        player1 = PlayerChars.select_random_player()
        player2 = PlayerChars.get_opponent(player1)
        self.renderer.human_player = player1

        self.players[player1] = HumanPlayer(player1)
        self.players[player2] = KIPlayer(player2, self.field)
        self.next_player(player1)

    def next_player(self, player=None):
        if player is not None:
            self.current_player = self.players[player]
            return
        if self.current_player is None:
            self.current_player = random.choice(list(self.players.values()))
        else:
            self.current_player = self.players[self.current_player.opponent]

    def reset(self):
        self.field = Field()
        self.halted = False
        self.players = {}
        self.attach_players()

    def test_reset(self):
        pull_reset = self.renderer.pull_reset()
        if pull_reset and self.halted:
            self.reset()
            self.renderer.tick(self.field.get_board())
            return True

        if self.halted:
            self.renderer.tick([], True)
            return True

        return False

    def loop(self):
        if len(self.players.keys()) == 0:
            raise Exception("No players attached")
        if self.current_player is None:
            raise Exception("No current player set")

        self.renderer.start()
        self.renderer.tick(self.field.get_board())
        while self.renderer.running:
            if self.test_reset():
                self.renderer.tick(self.field.get_board())
                continue

            self.renderer.tick(self.field.get_board())

            win_current_player, from_x, from_y, to_x, to_y = self.field.is_win(self.current_player.player)
            if win_current_player:
                self.halted = True
                self.renderer.draw_winner(from_x, from_y, to_x, to_y)
                self.renderer.render_text_center(f"{self.current_player.player} win!\n\nPress SPACE \nto restart", TEXT_COLOR)

            win_opponent, from_x, from_y, to_x, to_y = self.field.is_win(self.current_player.opponent)
            if win_opponent:
                self.halted = True
                self.renderer.draw_winner(from_x, from_y, to_x, to_y)
                self.renderer.render_text_center(f"{self.current_player.opponent} wins!\n\nPress SPACE \nto restart",TEXT_COLOR)

            if not self.field.has_empty():
                self.halted = True
                self.renderer.render_text_center("Draw!\n\nPress SPACE\n to restart", TEXT_COLOR)

            input_coord = self.current_player.select_move(self.field)
            if self.place(input_coord, self.current_player):
                self.next_player()
                self.renderer.tick(self.field.get_board(), self.halted)

            self.renderer.update_display()

        self.renderer.stop()



if __name__ == "__main__":
    g = Game()
    g.loop()
