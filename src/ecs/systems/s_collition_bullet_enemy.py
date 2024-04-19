import pygame, esper
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_bullet_tag import CTagBullet
from src.ecs.components.tags.c_enemy_tag import CTagEnemy

def sys_collition_bullet_enemy(world:esper.World):
    bullet_components = world.get_components(CTransform, CSurface, CTagBullet)
    enemy_components = world.get_components(CTransform, CSurface, CTagEnemy)
    c_sb:CSurface
    for bullet_entity, (c_tb, c_sb, _b) in bullet_components:
        bullet_rect = c_sb.surf.get_rect(topleft=c_tb.pos)
        for enemy_entity, (c_te, c_se, _e) in enemy_components:
            enemy_rect = c_se.surf.get_rect(topleft=c_te.pos)
            if bullet_rect.colliderect(enemy_rect):
                world.delete_entity(bullet_entity)
                world.delete_entity(enemy_entity)