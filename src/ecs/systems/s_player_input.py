
from typing import Callable
import esper, pygame

from src.ecs.components.c_input_command import CInputCommand, CInputCommandMouse, CommandPhase

def sys_player_input(world:esper.World, event: pygame.Event, do_action:Callable[[CInputCommand], None]):
    components = world.get_component(CInputCommand)
    mouseComponents = world.get_component(CInputCommandMouse)
    
    for _, c_input in components:
        if event.type == pygame.KEYDOWN and c_input.key == event.key:
            c_input.phase = CommandPhase.START
            do_action(c_input)
            
        elif event.type == pygame.KEYUP and c_input.key == event.key:
            c_input.phase = CommandPhase.END
            do_action(c_input)
            
            
    for _, c_input in mouseComponents:
        if event.type == pygame.MOUSEBUTTONDOWN and c_input.button == event.button:
            c_input.phase = CommandPhase.START
            do_action(c_input)
        elif event.type == pygame.MOUSEBUTTONUP and c_input.button == event.button:
            c_input.phase = CommandPhase.END
            do_action(c_input)