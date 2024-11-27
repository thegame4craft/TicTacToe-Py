import pygame

from Field import Field
from PlayerChars import PlayerChars
from colors import BACKGROUND_COLOR, INNER_LINE_COLOR, WINNER_LINE_COLOR, TEXT_COLOR, X_COLOR, O_COLOR, \
    INNER_LINE_STROKE, PLAYER_STROKE


class PygameRenderer:
    def __init__(self):
        self.width = 640
        self.height = 900
        self.padding = 20
        self.text = None
        pygame.init()
        self.human_player = None

    def start(self):
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.running = True

    def tick(self, board, halted=False):
        if not self.running: return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        
        if not halted:
            self.render_board()
            self.render_players(board)


    def update_display(self):
        pygame.display.flip()
        self.clock.tick(60)

    @staticmethod
    def pull_reset():
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]: return True
        return False


    def render_board(self):
        self.screen.fill(BACKGROUND_COLOR)

        # fps in the top right corner
        font = pygame.font.Font(None, 36)
        text = font.render(str(int(self.clock.get_fps())), True, TEXT_COLOR)
        self.screen.blit(text, (self.width - 50, 10))

        # draw small X or O in the top right corner
        if self.human_player == PlayerChars.PLAYER_X:
            pygame.draw.line(self.screen, X_COLOR, [50, 50], [10, 10], 8)
            pygame.draw.line(self.screen, X_COLOR, [50, 10], [10, 50], 8)
        elif self.human_player == PlayerChars.PLAYER_O:
            pygame.draw.circle(self.screen, O_COLOR, [30, 30], 20, 8)


        
        one_cell_w = (self.width - 2*self.padding) / 3
        one_cell_h = (self.height - 2*self.padding) / 3
        
        pygame.draw.line(self.screen, INNER_LINE_COLOR,
                [one_cell_w + self.padding, self.padding],
                [one_cell_w+ self.padding, self.height - 2*self.padding], INNER_LINE_STROKE)
        
        pygame.draw.line(self.screen, INNER_LINE_COLOR,
                [one_cell_w*2 + self.padding, self.padding],
                [one_cell_w*2 + self.padding, self.height - 2*self.padding], INNER_LINE_STROKE)
        
        pygame.draw.line(self.screen, INNER_LINE_COLOR,
                [self.padding, one_cell_h + self.padding],
                [self.width - 2*self.padding, one_cell_h + self.padding], INNER_LINE_STROKE)

        pygame.draw.line(self.screen, INNER_LINE_COLOR,
                [self.padding, one_cell_h*2 + self.padding],
                [self.width - 2*self.padding, one_cell_h*2 + self.padding], INNER_LINE_STROKE)

    def draw_winner(self, from_x, from_y, to_x, to_y):
        cell_width = (self.width - 2*self.padding) / 3
        cell_height = (self.height - 2*self.padding) / 3

        from_x = self.padding + cell_width * (from_x + 0.5)
        from_y = self.padding + cell_height * (from_y + 0.5)
        to_x = self.padding + cell_width * (to_x + 0.5)
        to_y = self.padding + cell_height * (to_y + 0.5)

        pygame.draw.line(self.screen, WINNER_LINE_COLOR, [from_x, from_y], [to_x, to_y], 12)

    def render_text_center(self, text:str, color=TEXT_COLOR) -> None:
        y = self.height // 2 - (len(text.split("\n")) * 150) // 4
        font = pygame.font.Font(None, 120)
        for line in text.split("\n"):
            text = font.render(line, True, color)
            rect = text.get_rect(center=(self.width / 2, y))
            y += 150
            self.screen.blit(text, rect)

    def render_players(self, board:list[str]) -> None:
        cell_width = (self.width - 2*self.padding) / 3 
        cell_height = (self.height - 2*self.padding) / 3 
        for y in range(0, 3):
            for x in range(0, 3):
                char = board[y * 3 + x]
                base_x = self.padding + cell_width * x
                base_y = self.padding + cell_height * y
                
                if char == PlayerChars.PLAYER_X:
                    pygame.draw.line(self.screen, X_COLOR, [base_x + 2*self.padding, base_y + 2*self.padding],
                            [base_x + cell_width - 2*self.padding, base_y + cell_height - 2*self.padding], PLAYER_STROKE)
                    pygame.draw.line(self.screen, X_COLOR,
                            [base_x + cell_width - 2*self.padding, base_y + 2*self.padding], 
                            [base_x + 2*self.padding, base_y + cell_height - 2*self.padding], PLAYER_STROKE)
                elif char == PlayerChars.PLAYER_O:
                    radius = min(cell_width // 2, cell_height // 2) - 2*self.padding
                    pygame.draw.circle(self.screen, O_COLOR,
            [base_x + (cell_width // 2), base_y + (cell_height // 2)], radius, PLAYER_STROKE)
                elif char == Field.EMPTY_CHAR: pass
                else:
                    raise Exception(f"Undefined behaviour {char=}")
        

    @staticmethod
    def stop():
        pygame.quit()

    @staticmethod
    def get_input_position():
        keys = pygame.key.get_pressed()
        if keys[pygame.K_KP1]: return 0, 2
        if keys[pygame.K_KP2]: return 1, 2
        if keys[pygame.K_KP3]: return 2, 2
        if keys[pygame.K_KP4]: return 0, 1
        if keys[pygame.K_KP5]: return 1, 1
        if keys[pygame.K_KP6]: return 2, 1
        if keys[pygame.K_KP7]: return 0, 0
        if keys[pygame.K_KP8]: return 1, 0
        if keys[pygame.K_KP9]: return 2, 0

