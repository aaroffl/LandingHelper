
import abc
from abc import ABC, abstractmethod
class LandingDataProvider(ABC):
    #@abc.abstractmethod
    def __init__(self,dataQ,errQ):
       self.dataQ = dataQ
       self.errQ = errQ
    @abc.abstractmethod
    def connect(self):
        raise NotImplementedError('user must define connect()')
    @abc.abstractmethod
    def disconnect(self):
        raise NotImplementedError('user must define disconnect()')
    @abc.abstractmethod
    def reset(self):
        raise NotImplementedError('user must define reset')
    @abc.abstractmethod
    def send(self,data):
        raise NotImplementedError('user must define send(command)')
    @abc.abstractmethod
    def read(self):
        raise NotImplementedError('user must define read.')