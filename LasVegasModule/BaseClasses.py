import random
from .settings import COLOR, CASINO_COLOR


class Dice:
    def __init__(self, color):
        self.color = COLOR(color)
        self.value = None

    def roll(self):
        self.value = random.randint(1, 6)

    def get_value(self):
        return self.value

    def get_color(self):
        return self.color


class Player:
    def __init__(self, color):
        self.money = 0
        self.color = COLOR(color)
        self.dice = [Dice(color) for _ in range(8)] + [Dice(COLOR['BLACK']) for _ in range(2)]

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


class Casino:
    def __init__(self, number):
        self.number = number
        self.color = COLOR[CASINO_COLOR[number]]
        self.container = {  # storing each color's number of dices
            COLOR['RED']: 0,
            COLOR['GREEN']: 0,
            COLOR['BLUE']: 0,
            COLOR['YELLOW']: 0,
            COLOR['BLACK']: 0,
        }
