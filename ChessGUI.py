'''For the GUI of the Chess game'''

import pygame
import chess

pygame.init()
pygame.font.init()

WIDTH = 500
HEIGHT = 450
screen = pygame.display.set_mode([WIDTH,HEIGHT])
font = pygame.font.Font('freesansbold.ttf', 10)
big_font = pygame.font.Font('freesansbold.ttf', 25)
timer = pygame.time.Clock()
fps = 60
# game variables and images
white_pieces = ['R', 'N', 'B', 'K', 'Q', 'B', 'N', 'R', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P']
white_locations = [(0,0), (1,0), (2,0), (3,0), (4,0), (5,0), (6,0), (7,0),
                    (0,1), (1,1), (2,1), (3,1), (4,1), (5,1), (6,1), (7,1)]
capture_pieces_white = []
black_pieces = ['r', 'n', 'b', 'k', 'q', 'b', 'n', 'r', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'p']
black_locations = [(0,7), (1,7), (2,7), (3,7), (4,7), (5,7), (6,7), (7,7),
                    (0,6), (1,6), (2,6), (3,6), (4,6), (5,6), (6,6), (7,6)]
capture_pieces_black = []
# 0- whites turn, no seleccion, 1- whites turn, piece selected, 2- black turn no selection, 3- black turn piece selected
turn_step = 0
# selection = 50
# valid_moves =[]
# load in game piece images
# black pieces
# queen
bq = pygame.image.load('./images/b_queen.png')
bq = pygame.transform.scale(bq, (40,40))
bq_small = pygame.transform.scale(bq, (22,22))
# king
bk = pygame.image.load('./images/b_king.png')
bk = pygame.transform.scale(bk, (40,40))
bk_small = pygame.transform.scale(bk, (22,22))
# rook
br = pygame.image.load('./images/b_rook.png')
br = pygame.transform.scale(br, (40,40))
br_small = pygame.transform.scale(br, (22,22))
# bishop
bb = pygame.image.load('./images/b_bishop.png')
bb = pygame.transform.scale(bb, (40,40))
bb_small = pygame.transform.scale(bb, (22,22))
# knight
bkn = pygame.image.load('./images/b_knight.png')
bkn = pygame.transform.scale(bkn, (40,40))
bkn_small = pygame.transform.scale(bkn, (22,22))
# pawn
bp = pygame.image.load('./images/b_pawn.png')
bp = pygame.transform.scale(bp, (40,40))
bp_small = pygame.transform.scale(bp, (22,22))

black_images = [bp, bq, bk, bkn, br, bb]
black_images_small = [bp_small, bq_small, bk_small, bkn_small, br_small, bb_small]
# white pieces
# queen
wq = pygame.image.load('./images/w_queen.png')
wq = pygame.transform.scale(wq, (40,40))
wq_small = pygame.transform.scale(wq, (22,22))
# king
wk = pygame.image.load('./images/w_king.png')
wk = pygame.transform.scale(wk, (40,40))
wk_small = pygame.transform.scale(wk, (22,22))
# rook
wr = pygame.image.load('./images/w_rook.png')
wr = pygame.transform.scale(wr, (40,40))
wr_small = pygame.transform.scale(wr, (22,22))
# bishop
wb = pygame.image.load('./images/w_bishop.png')
wb = pygame.transform.scale(wb, (40,40))
wb_small = pygame.transform.scale(wb, (22,22))
# knight
wkn = pygame.image.load('./images/w_knight.png')
wkn = pygame.transform.scale(wkn, (40,40))
wkn_small = pygame.transform.scale(wkn, (22,22))
# pawn
wp = pygame.image.load('./images/w_pawn.png')
wp = pygame.transform.scale(wp, (40,40))
wp_small = pygame.transform.scale(wp, (22,22))

white_images = [wp, wq, wk, wkn, wr, wb]
white_images_small = [wp_small, wq_small, wk_small, wkn_small, wr_small, wb_small]
white_pieces = ['R', 'N', 'B', 'K', 'Q', 'B', 'N', 'R', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P']

piece_list_white=['P', 'Q', 'K', 'N', 'R', 'B']
piece_list_black=['p', 'q', 'k', 'n', 'r', 'b']
# check variables/flashing counter

# draw main game board
def draw_board():
    for i in range(32):
        column = i % 4
        row = i//4
        if row % 2 == 0:
            pygame.draw.rect(screen, 'light gray', [300 - (column * 100), row * 50, 50, 50])
        else:
            pygame.draw.rect(screen, 'light gray', [350 - column * 100, row * 50, 50, 50])
        pygame.draw.rect(screen, 'gray', [0, 400, WIDTH, 50])
        pygame.draw.rect(screen, 'gold', [0, 400, WIDTH, 50], 5)
        pygame.draw.rect(screen, 'gold', [400, 0, 100, HEIGHT], 5)
        status_text = ['White: Select a Piece to Move', 'White: Select a Destination!', ' Black: Select a Piece to Move', 'Black: Select a Destination!']
        screen.blit(big_font.render(status_text[turn_step], True, 'black'), (10, 410))
        for i in range(9):
            pygame.draw.line(screen, 'black', (0, i * 50), (400, i * 50))
            pygame.draw.line(screen, 'black', (i * 50, 0), (i * 50, 400))

def draw_pieces():
    for i in range(len(white_pieces)):
        index = piece_list_white.index(white_pieces[i])
        if white_pieces[i] == 'Pawn':
            screen.blit(wp, (white_locations[i][0] * 50 + 11, white_locations[i][1] * 50 + 15))
        else:
            screen.blit(white_images[index], (white_locations[i][0] * 50 + 5, white_locations[i][1] * 50 + 5))
        

    for i in range(len(black_pieces)):
        index = piece_list_black.index(black_pieces[i])
        if black_pieces[i] == 'Pawn':
            screen.blit(bp, (black_locations[i][0] * 50 + 11, black_locations[i][1] * 50 + 15))
        else:
            screen.blit(black_images[index], (black_locations[i][0] * 50 + 5, black_locations[i][1] * 50 + 5))


# main game loop
run = True 
while run: 
    timer.tick(fps)
    screen.fill('dark gray')
    draw_board()
    draw_pieces()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    pygame.display.flip()
pygame.quit()


# # TODO check functionality and implementation 
# class ChessGUI:

#     def __init__(self, board: chess.Board):
#         pygame.init() # initiate pygame
#         self.screen = pygame.display.set_mode((480,480)) # set display mode for 480x480 px
#         self.board = board
#         self.__loadImages()
    
#     def __loadImages(self):
#         """
#         Loads the images from the /images/ folder and converts them into 60x60 px images
#         """
#         self.images = {}
#         pieces = ['pawn', 'knight', 'bishop', 'rook', 'queen', 'king']
#         colors = ['w', 'b']
#         for color in colors:
#             for piece in pieces:
#                 self.images[color + piece] = pygame.transform.scale(pygame.image.load(f"images/{color}_{piece}.png"), (60,60))
    
#     def __drawBoard(self):
#         """
#         Draws the board in a 8x8 grid
#         """
#         colors = [pygame.Color("white"), pygame.Color("gray")]
#         for row in range(8):
#             for column in range(8):
#                 color = colors[((row + column) % 2)]
#                 pygame.draw.rect(self.screen, color, pygame.Rect(column*60, row*60, 60, 60))

#     def __drawPieces(self):
#         """
#         Draws pieces in the chess
#         """
#         for i in range(64):
#             piece = self.board.piece_at(i)
#             if piece:
#                 row, col = divmod(i, 8)
#                 self.screen.blit(self.images[piece.symbol()], (col*60, row*60))

#     def __mainLoop(self):
#         """
#         Runs the loop for the gameplay
#         """
#         running = True
#         while running:
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     running = False
            
#             self.__drawBoard()
#             self.__drawPieces()
#             pygame.display.flip()
        
#         pygame.quit()
