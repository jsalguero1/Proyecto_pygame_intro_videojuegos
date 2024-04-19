
import random
import esper, pygame

from src.ecs.components.c_enemy_spawn import CEnemySpawner
from src.ecs.components.c_input_command import CInputCommand, CInputCommandMouse
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_bullet_tag import CTagBullet
from src.ecs.components.tags.c_enemy_tag import CTagEnemy
from src.ecs.components.tags.c_player_tag import CTagPlayer

"""
Recibe los parametros para crear un rectangulo
"""
def cuad_create(world:esper.World, 
                size: pygame.Vector2, 
                color: pygame.Color, 
                vel:pygame.Vector2, 
                pos: pygame.Vector2) -> int:
    
    cuad_entity = world.create_entity()
    world.add_component(cuad_entity, CTransform(pos))
    world.add_component(cuad_entity, CSurface(size, color))
    world.add_component(cuad_entity, CVelocity(vel))
    return cuad_entity

def sprite_create(world:esper.World, pos:pygame.Vector2, 
                  vel:pygame.Vector2, surface: pygame.Surface) -> int:
    sprite_entity = world.create_entity()
    world.add_component(sprite_entity, CTransform(pos))
    world.add_component(sprite_entity, CVelocity(vel))
    world.add_component(sprite_entity, CSurface.from_surface(surface))
    return sprite_entity

"""
Recibe un evento y la configuracion de enemigos
"""
def enemy_cuad_create(world:esper.World, enemy_type:str, enemies_cfg:dict, event:dict):
        
    # Selecciona la velocidad y escoge un valor aleatorio entre los limites
    vel_max = enemies_cfg[enemy_type]['velocity_max']
    vel_min = enemies_cfg[enemy_type]['velocity_min']
    vel = random.randint(vel_min, vel_max)
    velocity = pygame.Vector2(vel,vel)
    
    # Se asigna una posición
    pos = pygame.Vector2(event['position']['x'], event['position']['y'])
    
    enemy_surface =  pygame.image.load(enemies_cfg[enemy_type]['image']).convert_alpha()  
    # Se pasa la configuracion para crear un rectangulo
    enemy = sprite_create(world, velocity, pos, enemy_surface)
    world.add_component(enemy, CTagEnemy())
    
    
def player_cuad_create(world:esper.World, player_cfg:dict, player_level_cfg:dict):
    size = pygame.Vector2(player_cfg['size']['x'], player_cfg['size']['y'])
    color = pygame.Color(player_cfg['color']['r'],player_cfg['color']['g'],player_cfg['color']['b'])
    pos = pygame.Vector2(player_level_cfg['player_spawn']['position']['x'] - (size.x/2), player_level_cfg['player_spawn']['position']['y']-(size.y/2))
    vel = pygame.Vector2(0,0)
    player = cuad_create(world, size, color, vel, pos)
    world.add_component(player, CTagPlayer())
    return player
    
def spawn_entity_create(world:esper.World, level_config:dict):
    spawn_entity = world.create_entity()
    world.add_component(spawn_entity, CEnemySpawner(level_config))
    
def create_input_player(world:esper.World):
    input_left = world.create_entity()
    input_right = world.create_entity()
    input_up = world.create_entity()
    input_down = world.create_entity()
    input_left_click = world.create_entity()
    world.add_component(input_left, CInputCommand('PLAYER_LEFT', pygame.K_LEFT))
    world.add_component(input_right, CInputCommand('PLAYER_RIGHT', pygame.K_RIGHT))
    world.add_component(input_up, CInputCommand('PLAYER_UP', pygame.K_UP))
    world.add_component(input_down, CInputCommand('PLAYER_DOWN', pygame.K_DOWN))
    world.add_component(input_left_click, CInputCommandMouse('PLAYER_FIRE', pygame.BUTTON_LEFT))
    
def create_bullet(world:esper.World, bullet_cfg:dict, player_entity:int, mouse_pos:pygame.Vector2, level_cfg:dict):
    bullet_sprite = pygame.image.load(bullet_cfg['image'])
    c_s = world.component_for_entity(player_entity, CSurface)
    c_t = world.component_for_entity(player_entity, CTransform)
    player_rect = c_s.surf.get_rect(topleft = c_t.pos)
    player_center = player_rect.center
    pos = pygame.Vector2(player_center[0], player_center[1])
    mouse_pos1 = pygame.Vector2(mouse_pos.x-pos.x, mouse_pos.y-pos.y)
    mouse_pos1 = mouse_pos1.normalize()
    velocity = pygame.Vector2(bullet_cfg['velocity']* mouse_pos1.x, bullet_cfg['velocity']* mouse_pos1.y)
    components = world.get_components(CTagBullet)
    if len(components) < level_cfg['player_spawn']['max_bullets']:
        bullet_entity = sprite_create(world, pos, velocity, bullet_sprite)
        world.add_component(bullet_entity, CTagBullet())
        