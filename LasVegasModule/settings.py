"""
화면 크기 설정
FHD(1920 * 1080) 기준 가로, 세로 0.6배
"""

SCREEN_WIDTH = 1152  # 1920 * 0.6
SCREEN_HEIGHT = 648  # 1080 * 0.6

"""
색상 설정
플레이어 색상: 빨강, 초록, 파랑11
방해꾼 색상: 검정
"""

COLOR = {
    'WHITE': (255, 255, 255),
    'BLACK': (0, 0, 0),                 # for disruptor
    'RED': (255, 0, 0),                 # for player 1
    'GREEN': (0, 255, 0),               # for player 2
    'BLUE': (0, 0, 255),                # for player 3
    'YELLOW': (255, 255, 0),            # for player 4
    'HEAVY YELLOW': (235, 180, 52),     # for casino 1
    'TURQUOISE': (64, 224, 208),        # for casino 2
    'LIME GREEN': (50, 205, 50),        # for casino 3
    'GOLD': (255, 215, 0),              # for casino 4
    'Lavender': (230, 230, 250),        # for casino 5
    'CORAL': (255, 127, 80),            # for casino 6
    'GREEN_DARK': (56, 128, 34),
    'GRAY': (128, 128, 128),
    'DARK_PINK': (112, 29, 57),
}

"""
프레임 넓이 설정
카지노: 250 * 220
플레이어 카드: 180 * 120
주사위판: 300 * 400
"""

CASINO_WIDTH = 250
CASINO_HEIGHT = 220

PLAYERCARD_WIDTH = 200
PLAYERCARD_HEIGHT = 120

ROLL_BOARD_WIDTH = 300
ROLL_BOARD_HEIGHT = 400

MONEY_WIDTH = 40
MONEY_HEIGHT = 25

"""
프레임 위치 설정
카지노 1: (20,22)
카지노 2: (290,22)
카지노 3: (560,22)
카지노 4: (20,263)
카지노 5: (290,263)
카지노 6: (560,263)

플레이어 카드 1: (20,528)
플레이어 카드 2: (235,528)
플레이어 카드 3: (450,528)
플레이어 카드 4: (665,528)

Roll 버튼: (915,470)
Roll 판: (830,22)
"""

CASINO_POSITION = {
    1: (20, 22),
    2: (290, 22),
    3: (560, 22),
    4: (20, 263),
    5: (290, 263),
    6: (560, 263)
}

CASINO_END_POSITION = dict()
for i in range(1, 7):
    CASINO_END_POSITION[i] = (CASINO_POSITION[i][0] + CASINO_WIDTH, CASINO_POSITION[i][1] + CASINO_HEIGHT)

PLAYERCARD_POSITION = {
    0: (20, 528),
    1: (235, 528),
    2: (450, 528),
    3: (665, 528)
}

ROLL_BUTTON_RADIUS = 65
ROLL_BUTTON_POSITION = (915 + ROLL_BUTTON_RADIUS, 470 + ROLL_BUTTON_RADIUS)

ROLL_BOARD_POSITION = (830, 22)

"""
카지노 번호별 색상 설정
"""
CASINO_COLOR = {
    1: 'HEAVY YELLOW',
    2: 'TURQUOISE',
    3: 'LIME GREEN',
    4: 'GOLD',
    5: 'Lavender',
    6: 'CORAL'
}

"""
플레이어 번호별 색상 설정
"""
PLAYER_COLOR = {
    0: "RED",
    1: "GREEN",
    2: "BLUE",
    3: "YELLOW",
}
