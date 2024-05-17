from  MMAgent import MinMaxAgent
# from ChessGUI import ChessGUI
import chess.engine

board = chess.Board()
minmanx = MinMaxAgent()
# gui = ChessGUI(board)
# gui._ChessGUI__mainLoop()

# sigue = True
# move = minmanx.pick_move(board)
# while sigue:
#     print(board)
#     move = minmanx.pick_move(board)
#     if move:
#         board.push(move)
#     print(board)

print(board)
move = minmanx.pick_move(board)
if move:
    board.push(move)
    print(board)