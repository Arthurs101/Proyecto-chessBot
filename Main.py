from  MMAgent import MinMaxAgent
import chess.engine

board = chess.Board()
minmanx = MinMaxAgent()
move = minmanx.pick_move(board)

print(board)
move = minmanx.pick_move(board)
if move:
    board.push(move)
print(board)