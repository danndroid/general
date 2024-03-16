import numpy as np

class Node:
    def __init__(self, node_type, value=None):
        
        self.type = node_type
        self.children = []
        self.level = 1
        
        if isinstance(value, list):
            self.probs = value
            self.value = 0
        else:
            self.value = value
        
        
    def describe(self):
        print(' '*4*self.level, self.level, 'DESCRIBE:',self.type, '->',self.value)
        for c in self.children:
            c.level = self.level + 1 
            c.describe()
        
        #self.level = 1
    
    
    def compute(self):
        val = 0
        
        if self.type == "T":
            print(' '*4*self.level + 'TYPE T')
            val = self.value
            print(' '*4*self.level + 'val', val)
       
    
    
        elif self.type == "C":
            print(' '*4*self.level + 'TYPE C')
            
            c_values = []
            for c in self.children:
                c.level += 1
                c_values.append(c.compute())
                
            for p,v in zip(self.probs, c_values):
                val += p*v
            print(' '*4*self.level + 'VALUE >>>',val)
                  
                
                
        elif self.type == "D":
            print(' '*4*self.level + 'TYPE C')
            d_values = [c.compute() for c in self.children]
            
            val = np.max(d_values)
            
            print(' '*4*self.level + 'VALUE >>>',val)
        
            
        self.value = val
        
        return val
    