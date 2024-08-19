import pygame
from .settings import COLOR, SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_COLOR, PLAYERCARD_POSITION
from .BaseClasses import Player, Casino, RollButton


class Board:
    def __init__(self):
        self.roll_button = None
        self.screen = None
        self.players = None
        self.casinos = None
        self.turn = None
        self.player_turn = None  # decides whose turn it is
        self.turn_state = None   # decides which action has to be done
        self.status = {     # what state can be done
            0: 'START',     # 턴 시작
            1: 'ROLL',      # 주사위 굴림
            2: 'CHOOSE'     # 주사위 배치함
        }
        self.match = None

    # initialize game
    def initialize(self):
        # initialize screen
        pygame.init()
        pygame.display.set_caption('Las Vegas Board Game')
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen.fill(COLOR['GREEN_DARK'])
        pygame.display.flip()

        # initialize entities
        self.players = [Player(PLAYER_COLOR[i], PLAYERCARD_POSITION[i]) for i in range(4)]
        self.casinos = [Casino(i) for i in range(1, 1 + 6)]
        self.player_turn = ['RED', 'GREEN', 'BLUE', 'YELLOW']
        self.turn = 0
        self.roll_button = RollButton(COLOR['GRAY'])
        self.match = 0

    def execute_turn(self):
        # set screen
        for player in self.players:
            player.update_screen(self.screen)
        for casino in self.casinos:
            casino.update_screen(self.screen)
        self.roll_button = RollButton(COLOR[self.player_turn[self.turn]])
        self.roll_button.draw(self.screen)
        pygame.display.flip()

    def run(self):
        self.initialize()
        self.execute_turn()

        i = 1
        while i:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 0
            i += 1
