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
from keras.layers import Dense, Flatten  # Dense layers are fully connected layers, Flatten layers flatten out multidimensional inputs
import tensorflow as tf
import argparse
import os
from keras.models import model_from_json



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
    def __init__(self,epsilon=0.9,existing_model = None):
        '''
        For simplifiaction sake, the states is a 1d array of values for each square
        the value is given by the prices dictionary
        '''
        self.epsilon = epsilon
        self.state =  np.zeros((1,65))
        #initalize the Neural Network
        if not existing_model:
            self.model = Sequential()
            self.model.add(Dense(20, input_shape=(65,) , init='uniform', activation='relu'))
            self.model.add(Dense(18, init='uniform', activation='relu'))
            self.model.add(Dense(18, init='uniform', activation='relu'))
            self.model.add(Dense(18, init='uniform', activation='relu'))
            self.model.add(Dense(18, init='uniform', activation='relu'))
            self.model.add(Dense(10, init='uniform', activation='relu'))
            self.model.add(Dense(10, init='uniform', activation='relu'))
            self.model.add(Dense(1, init='uniform', activation='relu'))    # Same number of outputs as possible actions
            self.model.compile(loss='mse', optimizer='adam', metrics=['accuracy']) #Compiling the model
        else:
            self.model = model_from_json(existing_model)
    def pick_moves(self,board:chess.Board):
        '''
        returns the best move based on the current board state
        ...

        Params
        ------
        board : chess.Board

        Returns
        ------
        move : chess.Move object to be pushed to the board
        None: there is no move to be pushed ( extremely unlikely )
        '''
        #factor
        factor = 1 if board.turn else -1 
        # uptade the current board state
        for i in range(chess.SQUARES):
            self.state = factor*DEEPQ.prices[str(board.piece_at(i))]
        # check the legal moves
        for move in board.legal_moves:
            self.state[0][64] = gener
