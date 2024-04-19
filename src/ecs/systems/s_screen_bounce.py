

import pygame, esper
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_enemy_tag import CTagEnemy

def sys_screen_bounce(world:esper.World, screen: pygame.Surface):
    components = world.get_components(CTransform, CVelocity, CSurface, CTagEnemy)
    screen_rect = screen.get_rect()
    c_v:CVelocity
    for _, (c_t, c_v, c_s, c_te) in components:
        cuad_rect = c_s.surf.get_rect(topleft=c_t.pos)
        
        # Si choca contra un limite invierte su velocidad para generar rebote
        if cuad_rect.left < 0 or cuad_rect.right >= screen_rect.width:
            c_v.vel.x *= -1
            # Mueve la recta del cuadrado dentro del cuadrado de la pantalla
            cuad_rect.clamp_ip(screen_rect)
            # Actualiza la posición del cuadrado con la de la recta 
            c_t.pos.x = cuad_rect.x

        if cuad_rect.top < 0 or cuad_rect.bottom > screen_rect.height:
            c_v.vel.y *= -1
            cuad_rect.clamp_ip(screen_rect)
            c_t.pos.y = cuad_rect.y