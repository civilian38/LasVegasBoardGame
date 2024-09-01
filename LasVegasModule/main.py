import math
import random

import pygame
from pygame import font

from .settings import COLOR, SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_COLOR, PLAYERCARD_POSITION, ROLL_BUTTON_POSITION, \
    ROLL_BUTTON_RADIUS, ROLL_BOARD_POSITION, CASINO_POSITION, CASINO_END_POSITION, TOTAL_ROUND
from .BaseClasses import Player, Casino, RollButton, RollingBoard, Money


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
        self.money_card = None

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
        self.money_card = [Money(100) for _ in range(6)] + [Money(200) for _ in range(8)] + [Money(300) for _ in range(8)] + [Money(400) for _ in range(6)] + [Money(500) for _ in range(6)] + [Money(600) for _ in range(5)] + [Money(700) for _ in range(5)] + [Money(800) for _ in range(5)] + [Money(900) for _ in range(5)]

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
        # 매치 사전 설정
        random.shuffle(self.money_card)
        for casino in self.casinos:
            while casino.get_rewards_sum() < 1000:
                casino.add_rewards(self.money_card.pop())
            casino.sort_rewards()

        # 매치 진행
        while self.player_turn:
            self.execute_turn()

        # 점수 계산
        for casino in self.casinos:
            dice = casino.get_container()
            for key in dice.keys():
                dice[key] = len(dice[key])

            # 중복되는 값 모두 확인
            count = dict()
            for value in dice.values():
                count[value] = count.get(value, 0) + 1

            rank = list()
            for key, value in sorted(dice.items(), key=lambda x: x[1], reverse=True):
                if value != 0 and count[value] == 1 and key != 'BLACK':
                    rank.append(key)

            for player_color in rank:
                # find player
                player = None
                for player in self.players:
                    if player.get_color() == player_color:
                        break
                if player.get_color() == player_color:
                    if casino.get_rewards():
                        player.add_money(casino.get_rewards().pop().get_money())

            for money in casino.get_rewards():
                self.money_card.append(money)


        # 턴 초기화
        for player in self.players:
            player.reset()
        for casino in self.casinos:
            casino.reset()
        self.player_turn = ['RED', 'GREEN', 'BLUE', 'YELLOW']
        self.turn = 0

        self.match += 1

    def run(self):
        self.initialize()
        while self.match < TOTAL_ROUND:
            self.execute_match()
        first = (self.players[0], PLAYER_COLOR[0])
        for i in range(1, len(self.players)):
            if self.players[i].get_money() > first[0].get_money():
                first = (self.players[i], PLAYER_COLOR[i])

        rect = pygame.Rect(SCREEN_WIDTH * 0.1, SCREEN_HEIGHT * 0.1, SCREEN_WIDTH * 0.8, SCREEN_HEIGHT * 0.8)
        pygame.draw.rect(self.screen, COLOR['DARK_PINK'], rect)

        text_font = font.SysFont(None, 64)
        text_surface = text_font.render(first[1] + " WINS!", True, COLOR['WHITE'])
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2) * 0.8))
        self.screen.blit(text_surface, text_rect)

        rank_table = str()
        for i in range(0, len(self.players)):
            rank_table += PLAYER_COLOR[i] + ": " + str(self.players[i].get_money())
            if i != len(self.players) - 1:
                rank_table += " | "
        text_font = font.SysFont(None, 24)
        text_surface = text_font.render(rank_table, True, COLOR['WHITE'])
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, (SCREEN_HEIGHT // 2) * 1.2))

        self.screen.blit(text_surface, text_rect)
        pygame.display.flip()

        game = True
        while game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game = False
        pygame.quit()
