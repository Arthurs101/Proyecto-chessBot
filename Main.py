import pygame
import chess
from MMAgent import MinMaxAgent

pygame.init()
pygame.font.init()

WIDTH = 400
HEIGHT = 450
screen = pygame.display.set_mode([WIDTH, HEIGHT])
font = pygame.font.Font('freesansbold.ttf', 10)
big_font = pygame.font.Font('freesansbold.ttf', 25)
timer = pygame.time.Clock()
fps = 60

# load in game piece images
def load_image(path, size):
    image = pygame.image.load(path)
    return pygame.transform.scale(image, size)

# piece images
pieces = {
    'r': load_image('./images/b_rook.png', (40, 40)),
    'n': load_image('./images/b_knight.png', (40, 40)),
    'b': load_image('./images/b_bishop.png', (40, 40)),
    'q': load_image('./images/b_queen.png', (40, 40)),
    'k': load_image('./images/b_king.png', (40, 40)),
    'p': load_image('./images/b_pawn.png', (40, 40)),
    'R': load_image('./images/w_rook.png', (40, 40)),
    'N': load_image('./images/w_knight.png', (40, 40)),
    'B': load_image('./images/w_bishop.png', (40, 40)),
    'Q': load_image('./images/w_queen.png', (40, 40)),
    'K': load_image('./images/w_king.png', (40, 40)),
    'P': load_image('./images/w_pawn.png', (40, 40)),
}

# colors
LIGHT_SQUARE_COLOR = 'light gray'
DARK_SQUARE_COLOR = 'gray'
BACKGROUND_COLOR = 'dark gray'
STATUS_BAR_COLOR = 'gray'
STATUS_BAR_BORDER_COLOR = 'gold'

# chess board and agent
board = chess.Board()
agent = MinMaxAgent()

# draw main game board
def draw_board():
    for row in range(8):
        for col in range(8):
            color = LIGHT_SQUARE_COLOR if (row + col) % 2 == 0 else DARK_SQUARE_COLOR
            pygame.draw.rect(screen, color, [col * 50, row * 50, 50, 50])
    
    # draw status bar
    pygame.draw.rect(screen, STATUS_BAR_COLOR, [0, 400, WIDTH, 50])
    pygame.draw.rect(screen, STATUS_BAR_BORDER_COLOR, [0, 400, WIDTH, 50], 5)
    pygame.draw.rect(screen, STATUS_BAR_BORDER_COLOR, [400, 0, 100, HEIGHT], 5)
    
    status_text = ['White: Select a Piece to Move', 'White: Select a Destination!', ' Black: Select a Piece to Move', 'Black: Select a Destination!']
    screen.blit(big_font.render(status_text[0], True, 'black'), (10, 410))

def draw_pieces(board):
    board_str = str(board)
    for row, line in enumerate(board_str.split('\n')):
        col_count = 0
        for piece in line:
            if piece != ' ' and piece != '.':
                screen.blit(pieces[piece], (col_count * 50 + 5, row * 50 + 5))
                col_count += 1  # Increment column count only when a piece is drawn
            elif piece == '.':
                col_count += 1  # Increment column count for empty squares

# convert pixel coordinates to chess board coordinates
def get_board_pos(mouse_pos):
    x, y = mouse_pos
    return x // 50, 7 - (y // 50)  # adjust for 0-indexed board starting from top left

# main game loop
run = True
selected_piece = None
user_turn = True

while run:
    timer.tick(fps)
    screen.fill(BACKGROUND_COLOR)
    draw_board()
    draw_pieces(board)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN and user_turn:
            x, y = get_board_pos(pygame.mouse.get_pos())
            square = chess.square(x, y)  # adjust for 0-indexed board starting from top left
            if selected_piece is not None:
                move = chess.Move(selected_piece, square)
                if move in board.legal_moves:
                    board.push(move)
                    selected_piece = None
                    user_turn = False
            else:
                if board.piece_at(square) and board.piece_at(square).color == chess.WHITE:
                    selected_piece = square

    if not user_turn:
        move = agent.pick_move(board)
        if move:
            board.push(move)
        user_turn = True

    pygame.display.flip()

pygame.quit()
