from constants import WINDOW_WIDTH, WINDOW_HEIGHT, FPS
from renderer import GameRenderer
from game import Game
import pygame


pygame.init()
pygame.display.set_caption('Get Jiggy by Nick Sciarretta')

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

game = Game()
renderer = GameRenderer(window, game)

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        else:
            game.handle_event(event)

    elapsed = clock.tick(FPS)
    game.update(elapsed)
    renderer.draw()
    pygame.display.update()

pygame.quit()
