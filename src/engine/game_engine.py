import pygame, esper
import json
from src.create.cuad_create import create_bullet, create_input_player, cuad_create, player_cuad_create, spawn_entity_create
from src.ecs.components.c_enemy_spawn import CEnemySpawner
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_velocity import CVelocity
from src.ecs.systems.s_collition_bullet_screen import sys_screen_bullet_collition
from src.ecs.systems.s_collition_bullet_enemy import sys_collition_bullet_enemy
from src.ecs.systems.s_collition_player_enemy import sys_collition_player_enemy
from src.ecs.systems.s_enemy_spawn import sys_enemy_spawn
from src.ecs.systems.s_movement import sys_movement
from src.ecs.systems.s_player_input import sys_player_input
from src.ecs.systems.s_player_limits import sys_player_limits
from src.ecs.systems.s_rendering import sys_rendering
from src.ecs.systems.s_screen_bounce import sys_screen_bounce
class GameEngine:
    
    def cargar_datos(self):
        with open('assets/cfg/window.json') as f:
            self.window_cfg = json.load(f)
        with open('assets/cfg/level_01.json') as f:
            self.level_cfg = json.load(f)
        with open('assets/cfg/enemies.json') as f:
            self.enemies_cfg = json.load(f)
        with open('assets/cfg/player.json') as f:
            self.player_cfg = json.load(f)  
        with open('assets/cfg/bullet.json') as f:
            self.bullet_cfg = json.load(f)        
            
    
    """
    Clase base para crear un juego con Pygame
    cuando se crea una instancia de esta clase, se inicializa pygame y esta clase con
    los atributos self definidos en __init__.
    """
    def __init__(self) -> None:
        pygame.init()
        self.cargar_datos()
        self.is_running = False # Indica si el juego esta ejecutandose
        pygame.display.set_caption(self.window_cfg["window"]["title"])
        screen_width = self.window_cfg['window']['size']['w']
        screen_height = self.window_cfg['window']['size']['h']
        self.screen = pygame.display.set_mode((640, 360), pygame.SCALED) # Pygame crea la ventana
        self.clock = pygame.time.Clock() # Pygame tiene un reloj incluido para controlar el tiempo
        self.framerate = self.window_cfg['window']['framerate'] # Framerate del juego
        self.delta_time = 0 # Tiempo que ha pasado desde la ultima vuelta del game loop
        self.total_time = 0
        self.ecs_world = esper.World()
        

    """
    Game loop del juego
    """
    def run(self) -> None:
        #Inicia
        self._create()
        # Cambia estado de juego a ejecutando
        self.is_running = True
        #Mientras se este ejecutando el juego
        while self.is_running:
            #Calcula tiempo
            self._calculate_time()
            #Procesa eventos
            self._process_events()
            #Actuaaliza la información
            self._update()
            #Dibuja la informacion actualizada en pantalla
            self._draw()
        # Al dejar de ejecutar, se limpia la pantalla   
        self._clean()

    """
    Crear los elementos del juego
    """
    def _create(self):
        spawn_entity_create(self.ecs_world, self.level_cfg)
        self._player_entity = player_cuad_create(self.ecs_world, self.player_cfg, self.level_cfg)
        self.player_c_v = self.ecs_world.component_for_entity(self._player_entity, CVelocity)
        create_input_player(self.ecs_world)

    def _calculate_time(self):
        # Hace tick en el reloj y hace que vaya a la velocidad del framerate
        self.clock.tick(self.framerate)
        
        # Tiempo entre un frame y otro en milisegundos, por eso se divide entre 1000 y queda en segundos
        self.delta_time = self.clock.get_time() / 1000.0
    
        

    def _process_events(self):
        
        # Por cada evento que se registre en pygame se devuelve una lista de eventos
        # Esto sucede en cada vuelta del game loop
        for event in pygame.event.get():
            sys_player_input(self.ecs_world, event, self.do_action)
            if event.type == pygame.QUIT:
                self.is_running = False


    def _update(self):
        
        # Sistema de movimiento
        sys_movement(self.ecs_world, self.delta_time)
        
        # Sistema de rebote 
        sys_screen_bounce(self.ecs_world, self.screen)
        sys_player_limits(self.ecs_world, self.screen)
        
        # Sistema de spawns
        sys_enemy_spawn(self.ecs_world, self.delta_time, self.enemies_cfg)
        
        # Sistema de colisiones
        sys_collition_player_enemy(self.ecs_world, self._player_entity, self.level_cfg)
        sys_screen_bullet_collition(self.ecs_world, self.screen)
        sys_collition_bullet_enemy(self.ecs_world)
        
        # Limpiar entidades
        self.ecs_world._clear_dead_entities()
        
            
    """
    Esta funcion se encarga de limpiar la pantalla, dibujar la informacion actualizada y mostrarlo la pantalla
    1. Limpia
    2. Dibuja
    3. Muestra
    """
    def _draw(self):
        
        # Se pinta la pantalla
        r = self.window_cfg['window']['bg_color']['r']
        g = self.window_cfg['window']['bg_color']['g']
        b = self.window_cfg['window']['bg_color']['b']
        self.screen.fill((r, g, b))
        
        # Sistema de renderizado
        sys_rendering(self.ecs_world, self.screen)
        # Muestra la pantalla con la informacion actualizada
        pygame.display.flip()

    """
    Limpia la pantalla despues de terminar de ejecutar el juego
    """
    def _clean(self):
        self.ecs_world.clear_database()
        pygame.quit()
        
    def do_action(self, c_input: CInputCommand):
        if c_input.name == 'PLAYER_LEFT':
            if c_input.phase == CommandPhase.START:
                self.player_c_v.vel.x -= self.player_cfg['input_velocity']
            elif c_input.phase == CommandPhase.END:
                self.player_c_v.vel.x += self.player_cfg['input_velocity']
        elif c_input.name == 'PLAYER_RIGHT':
            if c_input.phase == CommandPhase.START:
                    self.player_c_v.vel.x += self.player_cfg['input_velocity']
            elif c_input.phase == CommandPhase.END:
                    self.player_c_v.vel.x -= self.player_cfg['input_velocity']
        elif c_input.name == 'PLAYER_UP':
            if c_input.phase == CommandPhase.START:
                self.player_c_v.vel.y -= self.player_cfg['input_velocity']
            elif c_input.phase == CommandPhase.END:
                self.player_c_v.vel.y += self.player_cfg['input_velocity']
        elif c_input.name == 'PLAYER_DOWN':
            if c_input.phase == CommandPhase.START:
                self.player_c_v.vel.y += self.player_cfg['input_velocity']
            elif c_input.phase == CommandPhase.END:
                self.player_c_v.vel.y -= self.player_cfg['input_velocity']
                
        elif c_input.name == 'PLAYER_FIRE':
            if c_input.phase == CommandPhase.START:
                mouse_x = pygame.mouse.get_pos()[0]
                mouse_y = pygame.mouse.get_pos()[1]
                mouse_pos = pygame.Vector2(mouse_x, mouse_y)
                create_bullet(self.ecs_world, self.bullet_cfg, self._player_entity, mouse_pos, self.level_cfg)
                    
            elif c_input.phase == CommandPhase.END:
                pass