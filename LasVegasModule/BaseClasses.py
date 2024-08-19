import random

import pygame
from pygame import font

from .settings import COLOR, CASINO_COLOR, CASINO_POSITION, CASINO_WIDTH, CASINO_HEIGHT, PLAYERCARD_WIDTH, PLAYERCARD_HEIGHT, ROLL_BUTTON_POSITION, ROLL_BUTTON_RADIUS


class Dice:
    def __init__(self, color):
        self.color = color
        self.value = random.randint(1, 6)

    def roll(self):
        self.value = random.randint(1, 6)

    def get_value(self):
        return self.value

    def get_color(self):
        return self.color

    def draw_dice(self, frame, x, y, size=32):
        pygame.draw.rect(frame, COLOR['WHITE'], pygame.Rect(x, y, size, size), border_radius=10)

        radius = size // 8
        margin = size // 4

        # 주사위 점의 위치 설정 (주사위 내부 좌표)
        positions = {
            1: [(x + size // 2, y + size // 2)],
            2: [(x + margin, y + margin), (x + size - margin, y + size - margin)],
            3: [(x + margin, y + margin), (x + size // 2, y + size // 2), (x + size - margin, y + size - margin)],
            4: [(x + margin, y + margin), (x + size - margin, y + margin),
                (x + margin, y + size - margin), (x + size - margin, y + size - margin)],
            5: [(x + margin, y + margin), (x + size - margin, y + margin),
                (x + size // 2, y + size // 2),
                (x + margin, y + size - margin), (x + size - margin, y + size - margin)],
            6: [(x + margin, y + margin), (x + size - margin, y + margin),
                (x + margin, y + size // 2), (x + size - margin, y + size // 2),
                (x + margin, y + size - margin), (x + size - margin, y + size - margin)]
        }

        # 주사위 숫자에 맞는 점 그리기
        for pos in positions[self.value]:
            pygame.draw.circle(frame, self.color, pos, radius)


class Player:
    def __init__(self, color, card_position):
        self.money = 0
        self.color = COLOR[color]
        self.dice = [Dice(color) for _ in range(8)] + [Dice(COLOR['BLACK']) for _ in range(2)]
        self.card_position = card_position

    def get_black_dice_number(self):
        dice_number = len(self.dice)
        black_dice_number = 0
        while (black_dice_number < dice_number and
               self.dice[-(black_dice_number + 1)].get_color() == COLOR['BLACK']):
            black_dice_number += 1
        return black_dice_number

    def get_my_dice_number(self):
        return len(self.dice) - self.get_black_dice_number()

    def get_money(self):
        return self.money

    def add_money(self, money):
        self.money += money

    def update_screen(self, screen):
        card = pygame.Surface((PLAYERCARD_WIDTH, PLAYERCARD_HEIGHT))
        card.fill(self.color)

        # 점수 입력
        text_font = font.SysFont(None, 30)
        text_surface = text_font.render(str(self.money), True, COLOR['BLACK'])
        text_rect = text_surface.get_rect()
        text_rect.topleft = (5, 5)
        card.blit(text_surface, text_rect)

        # 주사위 표시
        for i in range(len(self.dice)):
            self.dice[i].draw_dice(card, 4 + (40 * (i % 5)), 40 + (40 * (i // 5)))

        # 스크린에 프레임 버퍼 그리기
        screen.blit(card, self.card_position)


class Casino:
    def __init__(self, number):
        self.number = number
        self.color = COLOR[CASINO_COLOR[number]]
        self.card_position = CASINO_POSITION[number]
        self.container = {  # storing each color's number of dices
            COLOR['RED']: 0,
            COLOR['GREEN']: 0,
            COLOR['BLUE']: 0,
            COLOR['YELLOW']: 0,
            COLOR['BLACK']: 0,
        }

    def update_screen(self, screen):
        card = pygame.Surface((CASINO_WIDTH, CASINO_HEIGHT))
        card.fill(self.color)

        # 카지노 번호 입력
        text_font = font.SysFont(None, 32)
        text_surface = text_font.render(str(self.number), True, COLOR['BLACK'])
        text_rect = text_surface.get_rect()
        text_rect.bottomright = (CASINO_WIDTH - 5, CASINO_HEIGHT - 5)

        # 프레임 버퍼 완성
        card.blit(text_surface, text_rect)

        # 스크린에 프레임 버퍼 그리기
        screen.blit(card, self.card_position)


class RollButton:
    def __init__(self, color):
        self.color = color
        self.enable = True

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, ROLL_BUTTON_POSITION, ROLL_BUTTON_RADIUS)
        text_font = font.SysFont(None, 32)
        if self.enable:
            text_surface = text_font.render('ROLL', True, COLOR['WHITE'])
        else:
            text_surface = text_font.render('ROLL', True, COLOR['GRAY'])
        text_rect = text_surface.get_rect(center=ROLL_BUTTON_POSITION)
        screen.blit(text_surface, text_rect)

    def disable(self):
        self.enable = False
