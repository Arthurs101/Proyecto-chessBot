# Source code of python agent
import chess

class MinMaxAgent:
    chess_Scores = {
        'p': 1,
        'n': 3,
        'b': 3,
        'r': 5,
        'q': 9,
        'k': 13
        #el rey en sí no tiene valor, pero se le asigna este valor arbitrario , pues un valor 0 es casilla vacía
    }
    def __init__(self,max_depth=3):
        #more depth = more intelligent = more time to decide
        self.max_depth = max_depth 
    
    def pick_move(self ,board ):
        best_move_score = -1000000
        best_move = None
        for legal_move in board.legal_moves:
            move = chess.Move.from_uci(str(legal_move))
            board.push(move)
            score = max(best_move_score, self.__minMaxEval(board))
            board.pop()
            if score > best_move_score:
                best_move_score = score
                best_move = move
        return best_move
    
    def __minMaxEval(self,board: chess.Board,is_max=False,iter=1):
        """
        Returns the best possible move based on legals moves available

        ...
        
        Parameters
        -----------
        
        board: chess.Board instance 
            an instance of a board from chess core, used to acces the current state and possible legals moves available
        is_max: boolean default: False 
            indicates that is max or min node is being executed

        Returns
        -----------
        chess.Move : chess.Move instance 
            picekd move
        None: python type
            there is no move available to pick

        """
        if iter >= self.max_depth:
            return self.__score(board)
        #loop through all available moves
        best_score = -100000 if is_max else 100000
        for move in board.legal_moves:
            #generate the move instance
            m = chess.Move.from_uci(str(move))
            board.push(m)

            # calculating the min value for the particular node
            if is_max:    
                best_score = max(best_score, self.__minMaxEval(board, is_max=False , iter= iter + 1))
            else:
                best_score = min(best_score, self.__minMaxEval(board, is_max=True , iter= iter + 1))
                
            # undoing the last move, so that we can evaluate next legal moves
            board.pop()
        return best_score

    def __score(self, board:chess.Board):
        #scores the current state of the board
            i = 0
            evaluation = 0
            x = True
            try:
                x = bool(board.piece_at(i).color)
            except AttributeError as e:
                x = x
            while i < 63:
                i += 1
                evaluation = evaluation + (
                    self.__get_value_at(str(board.piece_at(i))) if x else -self.__get_value_at(str(board.piece_at(i))))
            return evaluation
    
    def __get_value_at(self,loc):
        if loc is None: return 0
        try: 
            return MinMaxAgent.chess_Scores[loc.lower()]
        except KeyError as _:
            return 0