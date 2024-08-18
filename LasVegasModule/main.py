import pygame
from .settings import COLOR, SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_COLOR, PLAYERCARD_POSITION
from .BaseClasses import Player, Casino


class Board:
    def __init__(self):
        self.screen = None
        self.players = None
        self.casinos = None

    def run(self):
        pygame.init()
        pygame.display.set_caption('Las Vegas Board Game')
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen.fill(COLOR['GREEN_DARK'])
        self.players = [Player(PLAYER_COLOR[i], PLAYERCARD_POSITION[i]) for i in range(4)]
        self.casinos = [Casino(i) for i in range(1, 1 + 6)]

        i = 1

        while i:
            if i == 1000000:
                for player in self.players:
                    player.update_screen(self.screen)
                for casino in self.casinos:
                    casino.update_screen(self.screen)
                pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 0
            i += 1
