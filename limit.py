from math import *
from abc import ABC, abstractmethod
#import numpy as np
#import matplotlib as plt

class Distributinon(ABC):
    @abstractmethod
    def __init__(self,input,returnProbs):
        '''инициализация'''
        self.input = input
        self.returnProbs = returnProbs


    @abstractmethod
    def isValidInput(self):
        "проверяет корректность инпута"


    @abstractmethod
    def calcProbs(self):
        '''вычисляет вероятности'''


    @abstractmethod
    def ret(self):
        '''возвращает'''

class Geometric(Distributinon):
    def __init__(self, input="", returnProbs=False):
        super().__init__(input=input, returnProbs=returnProbs)
        self.n, self.p = int(self.input.split()[0]) ,int(self.input.split()[1]) # хрень
        self.q = 1-self.p
        self.probs = []


    @abstractmethod
    def isValidInput(self):
        if  1 <= self.p<0: 
            #raise ValueError("p isn't correct")
            return False
        return True


    def calcProbs(self):
        '''вычисляет вероятности'''
        for i in range(1, self.n):
            self.probs.append(self.p*self.q**(i-1))

    
    def ret(self):
        '''возвращает'''
        if self.returnProbs:
            return self.probs #(probs, range(1, N+1))
        #else:
            #pd.DataFrame(probs, columns=['P']).plot()



if __name__ == "__main__":
    a = Geometric("10 0 1")
    print(a)



        