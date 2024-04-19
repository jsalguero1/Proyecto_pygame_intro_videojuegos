

from enum import Enum


class CInputCommand:
    def __init__(self, name:str, key:int) -> None:
        
        #Nombre de la accion
        self.name = name
        
        #La tecla que se presionó
        self.key = key
        
        #La fase en la que se encuentra
        self.phase = CommandPhase.NA
        
class CommandPhase(Enum):
    # Para iniciar, no se sabe en que estado esta
    NA = 0
    
    #Comienza una accion
    START = 1
    
    # Termina una accion
    END = 2
    
class CInputCommandMouse:
    def __init__(self, name:str, button:int) -> None:
        #Nombre de la accion
        self.name = name
        
        #La tecla que se presionó
        self.button = button
        
        #La fase en la que se encuentra
        self.phase = CommandPhase.NA
        
    