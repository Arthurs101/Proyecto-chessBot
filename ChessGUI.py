import pygame
from chess import Board


class GUI:

    def __init__(self) -> None:
        self.WIDTH = 400
        self.HEIGHT = 450
        self.BACKGROUND_COLOR = 'dark gray'
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode([self.WIDTH, self.HEIGHT])
        self.font = pygame.font.Font('freesansbold.ttf', 10)
        self.big_font = pygame.font.Font('freesansbold.ttf', 25)
        self.timer = pygame.time.Clock()
        self.fps = 60
        self.pieces = {
            'r': self.load_image('./images/b_rook.png', (40, 40)),
            'n': self.load_image('./images/b_knight.png', (40, 40)),
            'b': self.load_image('./images/b_bishop.png', (40, 40)),
            'q': self.load_image('./images/b_queen.png', (40, 40)),
            'k': self.load_image('./images/b_king.png', (40, 40)),
            'p': self.load_image('./images/b_pawn.png', (40, 40)),
            'R': self.load_image('./images/w_rook.png', (40, 40)),
            'N': self.load_image('./images/w_knight.png', (40, 40)),
            'B': self.load_image('./images/w_bishop.png', (40, 40)),
            'Q': self.load_image('./images/w_queen.png', (40, 40)),
            'K': self.load_image('./images/w_king.png', (40, 40)),
            'P': self.load_image('./images/w_pawn.png', (40, 40)),
        }
    
    def load_image(self, path: str, size: tuple):
        image = pygame.image.load(path)
        return pygame.transform.scale(image, size)
    
    # draw main game board
    def draw_board(self) -> None:
        LIGHT_SQUARE_COLOR = 'light gray'
        DARK_SQUARE_COLOR = 'gray'
        STATUS_BAR_COLOR = 'gray'
        STATUS_BAR_BORDER_COLOR = 'gold'
        for row in range(8):
            for col in range(8):
                color = LIGHT_SQUARE_COLOR if (row + col) % 2 == 0 else DARK_SQUARE_COLOR
                pygame.draw.rect(self.screen, color, [col * 50, row * 50, 50, 50])
        
        # draw status bar
        pygame.draw.rect(self.screen, STATUS_BAR_COLOR, [0, 400, self.WIDTH, 50])
        pygame.draw.rect(self.screen, STATUS_BAR_BORDER_COLOR, [0, 400, self.WIDTH, 50], 5)
        pygame.draw.rect(self.screen, STATUS_BAR_BORDER_COLOR, [400, 0, 100, self.HEIGHT], 5)
        
        status_text = ['White: Select a Piece to Move', 'White: Select a Destination!', ' Black: Select a Piece to Move', 'Black: Select a Destination!']
        self.screen.blit(self.big_font.render(status_text[0], True, 'black'), (10, 410))

    def draw_pieces(self, board: Board) -> None:
        board_str = str(board)
        for row, line in enumerate(board_str.split('\n')):
            col_count = 0
            for piece in line:
                if piece != ' ' and piece != '.':
                    self.screen.blit(self.pieces[piece], (col_count * 50 + 5, row * 50 + 5))
                    col_count += 1  # Increment column count only when a piece is drawn
                elif piece == '.':
                    col_count += 1  # Increment column count for empty squares
    
    # convert pixel coordinates to chess board coordinates
    def get_board_pos(self, mouse_pos) -> tuple:
        x, y = mouse_pos
        return x // 50, 7 - (y // 50)  # adjust for 0-indexed board starting from top left
    

    def draw_text(self, text, font, color, surface, x, y):
        text_obj = font.render(text, True, color)
        text_rect = text_obj.get_rect()
        text_rect.topleft = (x, y)
        surface.blit(text_obj, text_rect)

    def mode_selection_screen(self):
        mode = None
        while mode is None:
            self.screen.fill(self.BACKGROUND_COLOR)
            self.draw_text('Select Mode', self.big_font, 'black', self.screen, 80, 100)
            self.draw_text('1. Player vs Minimax Agent', self.big_font, 'black', self.screen, 20, 200)
            self.draw_text('2. Player vs Q-learning Agent', self.big_font, 'black', self.screen, 20, 250)
            self.draw_text('3. Minimax Agent vs Q-learning Agent', self.big_font, 'black', self.screen, 20, 300)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        mode = 'Player vs MinMAx'
                    
                    elif event.key == pygame.K_2:
                        mode = 'Player vs Q-Learning'

                    elif event.key == pygame.K_3:
                        mode = 'MinMax vs Q-Learning'
                    
                    else:
                        continue
                        
        
        return mode