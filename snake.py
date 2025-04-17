import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np

pygame.init()

font = pygame.font.SysFont('arial', 25)

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

class SnakeGame:
    def __init__(self, w=640, h=480):
        self.width = w
        self.height = h
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()
        self.direction = Direction.RIGHT
        self.score = 0
        self.head = Point(self.width // 2, self.height // 2)
        self.snake = [Point(self.head.x-BLOCK_SIZE, self.head.y), Point(self.head.x-2*BLOCK_SIZE, self.head.y)]
        self.food = None
        self._place_food()
    
    def _place_food(self):
        x = random.randint(0, (self.width - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.height - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()
    
    def play_step(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.direction != Direction.DOWN:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN and self.direction != Direction.UP:
                    self.direction = Direction.DOWN
                elif event.key == pygame.K_LEFT and self.direction != Direction.RIGHT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT and self.direction != Direction.LEFT:
                    self.direction = Direction.RIGHT
        
        self._move(self.direction)
        self.snake.insert(0, self.head)
        
        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score
        if self.head == self.food:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()
        
        self._update_ui()
        self.clock.tick(SPEED)
        
        return game_over, self.score
    
    def _is_collision(self):
        if self.head.x < 0 or self.head.x > self.width - BLOCK_SIZE or self.head.y < 0 or self.head.y > self.height - BLOCK_SIZE:
            return True
        if self.head in self.snake[1:]:
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
    
    def _move(self, direction):
        x = self.snake[0].x
        y = self.snake[0].y
        
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
        
        self.head = Point(x, y)

if __name__ == '__main__':
    game = SnakeGame()
    while True:
        game_over, score = game.play_step()
        if game_over == True:
            print(f'Puntaje final: {score}')
            break
    pygame.quit()