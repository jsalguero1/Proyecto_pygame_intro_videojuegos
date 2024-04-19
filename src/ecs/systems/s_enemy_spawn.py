import random
import pygame, esper
from src.create.cuad_create import cuad_create, enemy_cuad_create
from src.ecs.components.c_enemy_spawn import CEnemySpawner

def sys_enemy_spawn(world:esper.World, delta_time:float, enemies_cfg:dict):
    
    components = world.get_component(CEnemySpawner)
    c_es:CEnemySpawner
    
    for _, (c_es) in components:
        
        for i in range(0, len(c_es.level_conf)):
            
            # Evento de spawn
            event = c_es.level_conf
            
            # Se compara si el tiempo es mayor a alguno de los eventos que aun no han sido spawneados
            if c_es.total_time > event[i]['time'] and i not in c_es.index_list:
                event = event[i]
                #Se identifica el tipo de enemigo y se extrae su configuracion 
                enemy_type = event['enemy_type']
                
                # Crea un cuadrado enemigo
                enemy_cuad_create(world, enemy_type, enemies_cfg, event)
                
                # Se añade la lista de eventos que ya han spawneado
                c_es.index_list.append(i)

        # Se actualiza el delta time
        c_es.total_time += delta_time
        
            
    
     