

import pygame, esper
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_bullet_tag import CTagBullet

def sys_screen_bullet_collition(world:esper.World, screen: pygame.Surface):
    components = world.get_components(CTransform,CSurface, CTagBullet)
    screen_rect = screen.get_rect()
    c_v:CVelocity
    for bullet_entity, (c_t, c_s, c_te) in components:
        bullet_rect = c_s.surf.get_rect(topleft=c_t.pos)
        
        if bullet_rect.left < 0 or bullet_rect.right >= screen_rect.width:
            world.delete_entity(bullet_entity)

        if bullet_rect.top < 0 or bullet_rect.bottom > screen_rect.height:
            world.delete_entity(bullet_entity)