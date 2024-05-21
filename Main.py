import json
import pygame, chess
from MMAgent import MinMaxAgent
from ChessGUI import GUI
from QLearner import DEEPQ
import time
import sys

# Initialize chess board and agents
board = chess.Board()
minmax_agent = MinMaxAgent(max_depth=2)
qlearning_agent = DEEPQ(general_moves='generalized_moves.json')
gui = GUI()
mode = gui.mode_selection_screen()


# Main game loop variables
run = True
selected_piece = None
user_turn = True if mode.startswith("Player") else False
last_mover = None  # Variable to track the last agent to make a move
next_on_check = False #next player/agent is on check

#Variables para realizar bucle para que entrene la IA
run = True
selected_piece = None
last_mover = None

resultados_file = 'resultados.json'
# Función para registrar los resultados
def registrar_resultado(result):
    try:
        with open(resultados_file, 'r') as file:
            resultados = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        resultados = {"MinMax": 0, "DEEPQ": 0, "Empate": 0}

    if result == "1-0":
        resultados["MinMax"] += 1
    elif result == "0-1":
        resultados["DEEPQ"] += 1
    else:
        resultados["Empate"] += 1

    with open(resultados_file, 'w') as file:
        json.dump(resultados, file)


def ai_move(agent, board):
    global last_mover
    try:
        if isinstance(agent, MinMaxAgent):
            move = agent.pick_move(board)
            if move:
                board.push(move)
                last_mover = "MinMaxAgent"
            print(f"AI ({agent.__class__.__name__}) made a move: {move}")
        
        elif isinstance(agent, DEEPQ):
            move = agent.pick_move(board, allow_epsilon=True)
            if move:
                board.push(move)
                last_mover = "DEEPQ"
            print(f"AI ({agent.__class__.__name__}) made a move: {move}")
    except AssertionError as e:
        # Catch the specific assertion error indicating a pseudo-legal move issue
        # print(e) 
        return False
    return True

# Main game loop
while run:
    gui.timer.tick(gui.fps)
    gui.screen.fill(gui.BACKGROUND_COLOR)
    gui.draw_board()
    
    gui.draw_pieces(board)

    if user_turn:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = gui.get_board_pos(pygame.mouse.get_pos())
                square = chess.square(x, y)  # Adjust for 0-indexed board starting from top left
                if selected_piece is not None:
                    move = chess.Move(selected_piece, square)
                    if move in board.legal_moves:
                        next_on_check = board.gives_check(move)
                        board.push(move)
                        selected_piece = None
                        user_turn = False
                        last_mover = "Player"
                        print("User move made, Turn of the AI")
                    elif chess.Move(selected_piece, square,promotion=5) in board.legal_moves:
                        #try a promotion, if valid then has to select the promotion
                        promotion =  gui.promo_selection_screen()
                        board.push(chess.Move(selected_piece, square,promotion=promotion))
                        user_turn = False
                        last_mover = "Player"
                        print("User move made, Turn of the AI")
                    else:
                        print("Invalid move, try again")
                        selected_piece = None  # Reset selected piece if an invalid move is made
                else:
                    if board.piece_at(square) and board.piece_at(square).color == chess.WHITE:
                        selected_piece = square
    else:
        if mode == 'Player vs MinMAx':
            if not ai_move(minmax_agent, board):
                print(last_mover + " wins!")
                run = False
            else:
                user_turn = True
                print("AI made a move, user's turn")
        elif mode == 'Player vs Q-Learning':
            if not ai_move(qlearning_agent, board):
                print(last_mover + " wins!")
                run = False
            else:
                user_turn = True
                print("AI made a move, user's turn")
        elif mode == 'MinMax vs Q-Learning':
            if board.turn == chess.WHITE:
                if not ai_move(minmax_agent, board):
                    print(last_mover + " wins!")
                    run = False
            else:
                if not ai_move(qlearning_agent, board):
                    print(last_mover + " wins!")
                    run = False
        elif mode == 'Q-Learning vs Q-Learning':
            if board.turn == chess.WHITE:
                if not ai_move(qlearning_agent, board):
                    print(last_mover + " wins!")
                    run = False
            else:
                if not ai_move(qlearning_agent, board):
                    print(last_mover + " wins!")
                    run = False
    # Check for game over
    if board.is_game_over():
        result = board.result()
        registrar_resultado(result)
        if result == "1-0":
            print("White wins!")
            gui.draw_board("White wins!")
        elif result == "0-1":
            print("Black wins!")
            gui.draw_board("Black wins!")
        else:
            print("Draw!")
            gui.draw_board("Draw!")
        gui.draw_pieces(board)
        run = False   
    pygame.display.flip()

def ejecutar_juego(mode):
    global run, board, selected_piece, last_mover
    run = True
    board.reset()
    while run:
        gui.timer.tick(gui.fps)
        gui.screen.fill(gui.BACKGROUND_COLOR)
        gui.draw_board()
        gui.draw_pieces(board)

        if mode == 'MinMax vs Q-Learning':
            if board.turn == chess.WHITE:
                if not ai_move(minmax_agent, board):
                    print(last_mover + " gana!")
                    run = False
            else:
                if not ai_move(qlearning_agent, board):
                    print(last_mover + " gana!")
                    run = False
        elif mode == 'Q-Learning vs Q-Learning':
            if board.turn == chess.WHITE:
                if not ai_move(qlearning_agent, board):
                    print(last_mover + " gana!")
                    run = False
            else:
                if not ai_move(qlearning_agent, board):
                    print(last_mover + " gana!")
                    run = False

        # Comprobar si el juego ha terminado
        if board.is_game_over():
            result = board.result()
            registrar_resultado(result)
            if result == "1-0":
                print("¡Gana MinMax!")
            elif result == "0-1":
                print("¡Gana DEEPQ!")
            else:
                print("¡Empate!")
            run = False
        pygame.display.flip()


if __name__ == "__main__":
    num_iteraciones = 200  # Número de iteraciones para entrenar
    modo_entrenamiento = '--train' in sys.argv

    if modo_entrenamiento:
        for _ in range(num_iteraciones):
            ejecutar_juego('MinMax vs Q-Learning')
        print("Entrenamiento completado")
        pygame.quit()
    else:
        mode = gui.mode_selection_screen()
        ejecutar_juego(mode)
        time.sleep(4)
        pygame.quit()


time.sleep(4)
pygame.quit()
