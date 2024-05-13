'''
Clase constructora para el agente inteligente
'''
import chess
import random
import json
import operator
import numpy as np
import pickle 
from keras.models import Sequential      # One layer after the other
from keras.layers import Dense  
import tensorflow as tf
import argparse
import os
from keras.models import load_model
from MMAgent import MinMaxAgent
class DEEPQ:
    prices={
            'p':1,
            'P':-1,
            'q':9,
            'Q':-9,
            'n':3,
            'N':-3,
            'r':5,
            'R':-5,
            'b':3,
            'B':-3,
            'k':90,
            'K':-90,
            'None':0
        }
    def __init__(self,epsilon=0.9,gamma=0.005,epsilon_decrease=0.0002,existing_model = None,general_moves = None):
        '''
        For simplifiaction sake, the states is a 1d array of values for each square
        the value is given by the prices dictionary
        '''
        self.epsilon_decrease = epsilon_decrease
        self.gamma = gamma
        self.epsilon = epsilon
        self.graph = tf.compat.v1.get_default_graph()
        self.state =  np.zeros((1,65))
        #initalize the Neural Network
        if not general_moves:
            self.general_moves = {}  
        else:
            json_file = open(general_moves)
            json_str = json_file.read()
            self.general_moves=json.loads(json_str)
        if not existing_model:
            self.model = Sequential()
            self.model.add(Dense(20, input_shape=(65,) , activation='relu'))
            self.model.add(Dense(18, activation='relu'))
            self.model.add(Dense(18,  activation='relu'))
            self.model.add(Dense(18,  activation='relu'))
            self.model.add(Dense(18,  activation='relu'))
            self.model.add(Dense(10,  activation='relu'))
            self.model.add(Dense(10,  activation='relu'))
            self.model.add(Dense(1,  activation='relu'))    # Same number of outputs as possible actions
            self.model.compile(loss='mse', optimizer='adam', metrics=['accuracy']) #Compiling the model
        else:
            self.model = load_model(existing_model)
            self.model.compile(loss='mse', optimizer='adam', metrics=['accuracy'])
            self.model.make_predict_function()
    def pick_move(self,board:chess.Board,allow_epsilon=False):
        '''
        returns the best move based on the current board state
        ...

        Params
        ------
        board : chess.Board
        allow_epsilon: boolean
            default False
            allows epsilon to be used for random moves
        train_mode : boolean
            bypasses the usage of tesnroflow graph when predicting moves
        Returns
        ------
        move : chess.Move object to be pushed to the board
        None: there is no move to be pushed ( extremely unlikely )
        '''
        if allow_epsilon:
            if np.random.rand() <= self.epsilon:
                t = np.random.randint(0,board.legal_moves.count())
                p = 0
                for _ in board.legal_moves:
                    if p == t:
                        return _
                    p+=1
        #factor
        Q = {} #the q table for the movements
        factor = 1 if board.turn else -1 
        # uptade the current board state
        for i in chess.SQUARES:
            self.state[0][i] = factor*DEEPQ.prices[str(board.piece_at(i))]
        # check the legal moves
        for move in board.legal_moves:
            self.state[0][64] = self._get_move_id(str(move))
            Q[str(move)] = self.model.predict(self.state)

        best = max(Q.items(),key=operator.itemgetter(1))[0]
        return chess.Move.from_uci(best)
    def fit_finisher(self,win_states, win_actions, l_states, l_actions,win_weights=1, l_weights=-1.2): 
        '''
        fit the model given the states and moves
        it will punish any move on the looser input
        effectively avoiding them
        ...

        Params
        -----

        win_states : np.array (1,65) 
            represent the board as a np array of weighs given the piece of the winner
        win_actions : python list[string]
            represent the move as uci , example a7b6 , move from a7 to b6 , the boeard handles the piece and it's legallity 

        l_states : np.array (1,65) 
            represent the board as a np array of weighs given the piece of the looser
        l_actions : python list[string]
            represent the move as uci , example a7b6 , move from a7 to b6 , the boeard handles the piece and it's legallity 

        '''
        #reward all the moves that lead to victory
        for i in range(len(win_states)):
            win_states[i][0][64]=self._get_move_id(win_actions[i])
            self.model.train_on_batch(np.array(win_states[i]),self.model.predict(np.array(win_states[i]))+win_weights*(self.gamma*i))
        for i in range(len(l_states)):
            l_states[i][0][64]=self._get_move_id(l_actions[i])
            self.model.train_on_batch(np.array(l_states[i]),self.model.predict(np.array(l_states[i]))+l_weights*(self.gamma*i))
        self.epsilon -= self.epsilon_decrease
    def _get_move_id(self, move:str):
        #giving the id of the move as int value for the neural network
        try:
            return self.general_moves[move]
        except KeyError:
            self.general_moves[move] = len(self.general_moves)
            return self.general_moves[move]
    def _export_self(self):
        with open('generalized_moves.json', 'w') as fp:   # Save the mapping Move/Index to be used on developement
            json.dump(self.general_moves, fp)
        self.model.save("Qlearner.keras")

    def train_self(self,iterations=1000):
        board = chess.Board()
        for i in range(iterations):
            white_states = []
            white_moves = []
            black_states = []
            black_moves = []
            while not board.is_game_over():
                move = self.pick_move(board,allow_epsilon=True)
                if board.turn:
                    white_moves.append(str(move))
                    white_states.append(np.array(self.state,copy=True))
                else: #train against a min max
                    black_moves.append(str(move))
                    black_states.append(np.array(self.state,copy=True))
                board.push(chess.Move.from_uci(str(move)))
            if board.result()=="1-0":
                self.fit_finisher(white_states, white_moves, black_states, black_moves)
            elif board.result()=="0-1":
                self.fit_finisher(black_states, black_moves, white_states, white_moves)
            board.reset_board()
        self._export_self()

# tmodel = DEEPQ()
# tmodel.train_self()

#TESTING THE IMPORT 
# board = chess.Board()
# model = DEEPQ(existing_model='Qlearner.keras',general_moves='generalized_moves.json')
# move = model.pick_move(board)
# board.push(move)
# print(board)