import pygame
from .settings import WIDTH, HEIGHT


class Board:
    def __init__(self):
        self.screen = None

    def run(self):
        pygame.init()
        pygame.display.set_caption('Las Vegas Board Game')
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
