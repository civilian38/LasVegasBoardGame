import math

import pygame
from .settings import COLOR, SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_COLOR, PLAYERCARD_POSITION, ROLL_BUTTON_POSITION, \
    ROLL_BUTTON_RADIUS, ROLL_BOARD_POSITION, CASINO_POSITION, CASINO_END_POSITION
from .BaseClasses import Player, Casino, RollButton, RollingBoard


class Board:
    def __init__(self):
        self.roll_button = None
        self.roll_board = RollingBoard()
        self.screen = None
        self.players = None
        self.casinos = None
        self.turn = None
        self.player_turn = None  # decides whose turn it is
        self.turn_state = None  # decides which action has to be done
        self.status = {  # what state can be done
            0: 'START',  # 턴 시작
            1: 'ROLL',  # 주사위 굴림
            2: 'CHOOSE'  # 주사위 배치함
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

    def draw(self):
        for player in self.players:
            player.update_screen(self.screen)
        for casino in self.casinos:
            casino.update_screen(self.screen)
        self.roll_button.draw(self.screen)
        pygame.display.flip()

    def execute_turn(self):
        # set roll button
        self.roll_button = RollButton(COLOR[self.player_turn[self.turn]])

        # set screen
        self.draw()

        # set status
        self.turn_state = self.status[0]

        # find player
        player = None
        for player in self.players:
            if player.get_color() == COLOR[self.player_turn[self.turn]]:
                break

        # roll the dice
        while self.turn_state == self.status[0]:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.turn_state = - 1

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    distance = math.sqrt(
                        (mouse_x - ROLL_BUTTON_POSITION[0]) ** 2 + (mouse_y - ROLL_BUTTON_POSITION[1]) ** 2
                    )

                    # clicks roll button
                    if distance < ROLL_BUTTON_RADIUS:
                        self.roll_button.disable()
                        dice = player.get_dice()

                        frame = self.roll_board.get_frame()
                        values = [[] for _ in range(6)]
                        ypos = [17 + 52 * i for i in range(6)]
                        for die in dice:
                            die.roll()
                            values[die.get_value() - 1].append(die)
                        for die in values:
                            y = ypos.pop()
                            for i in range(len(die)):
                                die[i].draw_dice(frame, 17 + 52 * i, y, size=48)
                        self.screen.blit(frame, ROLL_BOARD_POSITION)

                        self.turn_state = self.status[1]
            self.draw()

        # place dice
        while self.turn_state == self.status[1]:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.turn_state = - 1

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    casino = None
                    for i in range(1, 7):
                        if (CASINO_POSITION[i][0] <= mouse_x <= CASINO_END_POSITION[i][0] and
                                CASINO_POSITION[i][1] <= mouse_y <= CASINO_END_POSITION[i][1]):
                            casino = i
                            break

                    if casino and values[casino - 1]:
                        self.casinos[casino - 1].add_container(values[casino - 1], COLOR[self.player_turn[self.turn]])
                        player.remove_dice_by_number(casino)
                        self.turn_state = self.status[2]
            self.draw()

        # ending turn
        while self.turn_state == self.status[2]:
            if len(player.get_dice()) == 0:
                self.player_turn.remove(self.player_turn[self.turn])
                self.turn -= 1
            self.turn += 1
            if self.turn >= len(self.player_turn):
                self.turn = 0
            frame = self.roll_board.get_frame()
            self.screen.blit(frame, ROLL_BOARD_POSITION)
            self.draw()
            self.turn_state = 0

    def execute_match(self):
        while self.player_turn:
            self.execute_turn()
        self.match += 1

    def run(self):
        self.initialize()
        self.execute_match()

        i = 1
        while i:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 0
            i += 1
