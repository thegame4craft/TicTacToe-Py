from Field import Field
from PygameRenderer import PygameRenderer
from PlayerChars import PlayerChars

class Game:
    def __init__(self):
        self.field = Field()
        self.halted = False
        self.renderer = PygameRenderer()

    def loop(self):
        self.renderer.start()
        current_player = PlayerChars.PLAYER_X 
        while self.renderer.running:
            if self.halted: 
                self.renderer.tick([], True)
                continue

            input_coord = self.renderer.get_input_position()
            if input_coord is not None:
                ic_x, ic_y = input_coord
                if self.field.get_char(ic_x, ic_y) == " ":
                    self.field.place(ic_x, ic_y, current_player)
                    current_player = PlayerChars.PLAYER_O if current_player == PlayerChars.PLAYER_X else PlayerChars.PLAYER_X

            self.renderer.tick(self.field.board)
            b = self.field.board
            if b[0] == b[1] and b[1] == b[2] and b[0] != " " and b[1] != " " and b[2] != " ":
                self.renderer.draw_winner(0, 0, 2, 0)
                self.halted = True
            elif b[3] == b[4] and b[4] == b[5] and b[3] != " " and b[4] != " " and b[5] != " ":
                self.renderer.draw_winner(0, 1, 2, 1)    
                self.halted = True
            elif b[6] == b[7] and b[7] == b[6] and b[6] != " " and b[7] != " " and b[8] != " ":               
                self.renderer.draw_winner(0, 2, 2, 2)    
                self.halted = True
            elif b[0] == b[3] and b[3] == b[6] and b[0] != " " and b[3] != " " and b[6] != " ":            
                self.renderer.draw_winner(0, 0, 0, 2)    
                self.halted = True
            elif b[1] == b[4] and b[4] == b[7] and b[1] != " " and b[4] != " " and b[7] != " ":
                self.renderer.draw_winner(1, 0, 1, 2)    
                self.halted = True
            elif b[2] == b[5] and b[5] == b[8] and b[2] != " " and b[5] != " " and b[8] != " ":        
                self.renderer.draw_winner(2, 0, 2, 2)    
                self.halted = True
            elif b[0] == b[4] and b[4] == b[8] and b[0] != " " and b[4] != " " and b[8] != " ":
                self.renderer.draw_winner(0, 0, 2, 2)    
                self.halted = True
            elif b[2] == b[4] and b[4] == b[6] and b[2] != " " and b[4] != " " and b[2] != " ":
                self.renderer.draw_winner(2, 0, 0, 2)    
                self.halted = True

        self.renderer.stop()

if __name__ == "__main__":
    _ = Game()
    _.loop()
