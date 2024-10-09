import pygame
from PlayerChars import PlayerChars

class PygameRenderer:
    def __init__(self):
        self.width = 640
        self.height = 900
        self.padding = 20
        pygame.init()

    def start(self):
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.running = True
        self.error = False

    def tick(self, board, halted=False):
        if not self.running: return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        
        if not halted:
            self.render_board()
            self.render_players(board)
        pygame.display.flip()
        self.clock.tick(60)


    def get_input_position(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_KP1]: return (0, 2)
        if keys[pygame.K_KP2]: return (1, 2)
        if keys[pygame.K_KP3]: return (2, 2)
        if keys[pygame.K_KP4]: return (0, 1)
        if keys[pygame.K_KP5]: return (1, 1)
        if keys[pygame.K_KP6]: return (2, 1)
        if keys[pygame.K_KP7]: return (0, 0)
        if keys[pygame.K_KP8]: return (1, 0)
        if keys[pygame.K_KP9]: return (2, 0)

    def invalid_position(self, type_):
        self.error = type_

    def render_board(self):
        self.screen.fill("black")
        
        onecell_w = (self.width - 2*self.padding) / 3
        onecell_h = (self.height - 2*self.padding) / 3
        
        pygame.draw.line(self.screen, "white", 
                [onecell_w + self.padding, self.padding],
                [onecell_w+ self.padding, self.height - 2*self.padding], 3)
        
        pygame.draw.line(self.screen, "white", 
                [onecell_w*2 + self.padding, self.padding],
                [onecell_w*2 + self.padding, self.height - 2*self.padding], 3)
        
        pygame.draw.line(self.screen, "white",
                [self.padding, onecell_h + self.padding], 
                [self.width - 2*self.padding, onecell_h + self.padding], 3)

        pygame.draw.line(self.screen, "white",
                [self.padding, onecell_h*2 + self.padding], 
                [self.width - 2*self.padding, onecell_h*2 + self.padding], 3)

    def draw_winner(self, from_x, from_y, to_x, to_y):
        cell_width = (self.width - 2*self.padding) / 3
        cell_height = (self.height - 2*self.padding) / 3

        from_x = self.padding + cell_width * (from_x + 0.5)
        from_y = self.padding + cell_height * (from_y + 0.5)
        to_x = self.padding + cell_width * (to_x + 0.5)
        to_y = self.padding + cell_height * (to_y + 0.5)

        pygame.draw.line(self.screen, "green", [from_x, from_y], [to_x, to_y], 12)

    def render_players(self, board:list[str]) -> None:
        cell_width = (self.width - 2*self.padding) / 3 
        cell_height = (self.height - 2*self.padding) / 3 
        for y in range(0, 3):
            for x in range(0, 3):
                char = board[y * 3 + x]
                base_x = self.padding + cell_width * x
                base_y = self.padding + cell_height * y
                
                if char == PlayerChars.PLAYER_X:
                    pygame.draw.line(self.screen, "blue", [base_x + 2*self.padding, base_y + 2*self.padding],
                            [base_x + cell_width - 2*self.padding, base_y + cell_height - 2*self.padding], 3)
                    pygame.draw.line(self.screen, "blue", 
                            [base_x + cell_width - 2*self.padding, base_y + 2*self.padding], 
                            [base_x + 2*self.padding, base_y + cell_height - 2*self.padding], 3)
                elif char == PlayerChars.PLAYER_O:
                    radius = min(cell_width // 2, cell_height // 2) - 2*self.padding
                    pygame.draw.circle(self.screen, "blue",
            [base_x + (cell_width // 2), base_y + (cell_height // 2)], radius, 3)
                elif char == " ": pass
                else:
                    raise Exception(f"Undefined behaviour {char=}")
        

    def stop(self):
        pygame.quit()

