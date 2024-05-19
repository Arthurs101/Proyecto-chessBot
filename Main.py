import pygame, threading, chess
from MMAgent import MinMaxAgent
from ChessGUI import GUI
from QLearner import DEEPQ


# chess board and agent
board = chess.Board()
minmax_agent = MinMaxAgent()
qlearning_agent = DEEPQ()
gui = GUI()
mode = gui.mode_selection_screen()
# main game loop
run = True
selected_piece = None
user_turn = True if mode.startswith("Player") else False

while run:
    gui.timer.tick(gui.fps)
    gui.screen.fill(gui.BACKGROUND_COLOR)
    gui.draw_board()
    gui.draw_pieces(board)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN and user_turn:
            x, y = gui.get_board_pos(pygame.mouse.get_pos())
            square = chess.square(x, y)  # adjust for 0-indexed board starting from top left
            if selected_piece is not None:
                move = chess.Move(selected_piece, square)
                if move in board.legal_moves:
                    board.push(move)
                    selected_piece = None
                    user_turn = False
                    print("User move made, Turn of the AI")
                else:
                    print("Invalid move, try again")
                    selected_piece = None # en caso se seleccione un movimiento que no es, dar esto
            else:
                if board.piece_at(square) and board.piece_at(square).color == chess.WHITE:
                    selected_piece = square

    if not user_turn:
        if mode == 'Player vs MinMAx':


            move = minmax_agent.pick_move(board)
            if move:
                board.push(move)

            user_turn = True
            print("AI made a move, user's turn")
        #TODO implement Qlearning vs Human
        elif mode == 'Player vs Q-Learning':
            ...

        #TODO implement Minmax vs Qlearning
        elif mode == 'MinMax vs Q-Learning':
            ...           

    pygame.display.flip()

pygame.quit()
