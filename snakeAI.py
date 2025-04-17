import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np

pygame.init()

font = pygame.font.SysFont('arial', 25)

#hay que añadir al juego las siguientes funciones para implementar al agente:
#resetear el juego
#reward al agente
#accion
#iteracion

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x, y')
BLOCK_SIZE = 20
SPEED = 20

#Paleta
score_color= (255, 255, 255)
food= (252, 122, 87)
snk_color1= (167, 201, 87)
snk_color2= (106, 153, 78)
bckgrnd_color= (53, 53, 53)

class SnakeGameAI:
    def __init__(self, w=640, h=480):
        self.width = w
        self.height = h
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()
        self.reset()
    
    def reset(self):
        
        self.direction = Direction.RIGHT
        self.score = 0
        self.head = Point(self.width // 2, self.height // 2)
        self.snake = [self.head, Point(self.head.x-BLOCK_SIZE, self.head.y), Point(self.head.x-2*BLOCK_SIZE, self.head.y)]
        self.food = None
        self._place_food()
        self.frame_iteration = 0
    
    def _place_food(self):
        x = random.randint(0, (self.width - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.height - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()
    
    def play_step(self):
        self.frame_iteration += 1
        #leer evento
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        #obtener la accion del agente        
        self._move(accion)
        self.snake.insert(0, self.head)
        
        #verificar si el juego ha terminado
        #si el juego ha terminado, devolver la puntuacion y reiniciar el juego
        #si el juego no ha terminado, verificar si la serpiente ha comido la comida
        reward = 0
        game_over = False
        if self._is_collision() or self.frame_iteration > 100*len(self.snake):
            #recompensa negativa
            game_over = True
            reward = -10
            return reward, game_over, self.score
        
        if self.head == self.food:
            #recompensa positiva
            self.score += 1
            reward = 10
            self._place_food()
        else:
            self.snake.pop()
        
        self._update_ui()
        self.clock.tick(SPEED)
        
        return reward, game_over, self.score
    
    def _is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        if pt.x < 0 or pt.x > self.width - BLOCK_SIZE or pt.y < 0 or pt.y > self.height - BLOCK_SIZE:
            return True
        if pt in self.snake[1:]:
            return True
        return False
    
    def _update_ui(self):
        self.display.fill(bckgrnd_color)
        for pt in self.snake:
            pygame.draw.rect(self.display, snk_color1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, snk_color2, pygame.Rect(pt.x + 5, pt.y + 5, BLOCK_SIZE - 10, BLOCK_SIZE - 10))
        
        pygame.draw.rect(self.display, food, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
        
        score_text = font.render(f'SCORE: {self.score}', True, score_color)
        self.display.blit(score_text, [0, 0])
        
        pygame.display.flip()
    
    def _move(self, accion):
        # [forward, right, left]
        clockwise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clockwise.index(self.direction)
        
        if np.array_equal(accion, [1, 0, 0]):
            new_dir = clockwise[idx] # forward
        elif np.array_equal(accion, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_dir = clockwise[next_idx] # right E -> S -> W -> N
        elif np.array_equal(accion, [0, 0, 1]):
            next_idx = (idx - 1) % 4
            new_dir = clockwise[next_idx] # left E -> N -> W -> S
        
        self.direction = new_dir
        
        x = self.head.x
        y = self.head.y
        
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        
        self.head = Point(x, y)