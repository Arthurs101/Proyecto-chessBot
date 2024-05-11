'''For the GUI of the Chess game'''

import pygame
import chess

# TODO check functionality and implementation 
class ChessGUI:

    def __init__(self, board: chess.Board):
        pygame.init() # initiate pygame
        self.screen = pygame.display.set_mode((480,480)) # set display mode for 480x480 px
        self.board = board
        self.__loadImages()
    
    def __loadImages(self):
        """
        Loads the images from the /images/ folder and converts them into 60x60 px images
        """
        self.images = {}
        pieces = ['pawn', 'knight', 'bishop', 'rook', 'queen', 'king']
        colors = ['w', 'b']
        for color in colors:
            for piece in pieces:
                self.images[color + piece] = pygame.transform.scale(pygame.image.load(f"images/{color}_{piece}.png"), (60,60))
    
    def __drawBoard(self):
        """
        Draws the board in a 8x8 grid
        """
        colors = [pygame.Color("white"), pygame.Color("gray")]
        for row in range(8):
            for column in range(8):
                color = colors[((row + column) % 2)]
                pygame.draw.rect(self.screen, color, pygame.Rect(column*60, row*60, 60, 60))

    def __drawPieces(self):
        """
        Draws pieces in the chess
        """
        for i in range(64):
            piece = self.board.piece_at(i)
            if piece:
                row, col = divmod(i, 8)
                self.screen.blit(self.images[piece.symbol()], (col*60, row*60))

    def __mainLoop(self):
        """
        Runs the loop for the gameplay
        """
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            self.__drawBoard()
            self.__drawPieces()
            pygame.display.flip()
        
        pygame.quit()
