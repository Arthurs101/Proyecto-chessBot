'''
Clase encargada de decodificar la data del csv
'''
class Trainer(object):
    def __init__(self, elo=300):
        '''
        elo : objetivo de nivel de entrenamiento ( más alto = IA más inteligente max 2000)
        '''
        self.elo = elo
        