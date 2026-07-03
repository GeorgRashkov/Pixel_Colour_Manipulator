import numpy as np
from typing import Callable

class Dynamic_variable:

    def __init__(self, id:int, frequency:int, start:float, end:float, step:str, modulo_loop:bool=False):
        
        self.id = id
        self.initial_frequency = frequency
        self.frequency = self.initial_frequency
        self.start = min(start,end)
        self.end = max(start,end)

        self.current_value = start

        self.step_str = f"lambda v=[0]: {step}"
        self.step:Callable[[list[float]], float] = eval(self.step_str)

        self.modulo_loop = modulo_loop
    
    def get_current_value(self):
        return self.current_value

    def get_value(self, v:list[float]) -> float:
        
        if(self.frequency > 0):
            return self.current_value
        
        try:
            self.current_value = self.step(v=v)
        except ZeroDivisionError:
            return 1

        if(self.current_value < self.start):
            
            if(self.modulo_loop == False):
                self.current_value = self.end

            elif(self.end > -0.000_001 and self.end < 0.000_001):                
                self.current_value = self.end
            else:
                self.current_value %= self.end
            

        elif(self.current_value > self.end):
            
            if(self.modulo_loop == False):
                self.current_value = self.start

            elif( self.start > -0.000_001 and self.start < 0.000_001):
                
                self.current_value = self.start
            else:
                self.current_value %= self.start
            
        
        return self.current_value
    


    def update_frequency(self):

        if(self.frequency > 0):
            self.frequency-=1
        else:
            self.frequency = self.initial_frequency
    
    def reset_value_and_frequency(self):

        self.frequency = self.initial_frequency
        self.current_value = self.start

