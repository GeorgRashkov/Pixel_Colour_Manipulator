import numpy as np

class Dynamic_variable:

    def __init__(self, id:int, frequency:int, start:float, end:float, step:str):
        
        self.id = id
        self.initial_frequency = frequency
        self.frequency = self.initial_frequency
        self.start = min(start,end)
        self.end = max(start,end)

        self.current_value = start
        
        self.step_str = f"lambda v=0: {step}"
        self.step = eval(self.step_str)
    

    def get_variable(self, v:list[float]) -> float:
        
        if(self.frequency > 0):
            return self.current_value
        
        self.current_value = self.step(v=v)

        if(self.current_value < self.start):
            self.current_value = self.end

        elif(self.current_value > self.end):
            self.current_value = self.start
        
        return self.current_value
    


    def update_frequency(self):

        if(self.frequency > 0):
            self.frequency-=1
        else:
            self.frequency = self.initial_frequency

