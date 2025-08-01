from .player import Player
from .validate import is_valid_attendance_cnt


def calculate_basic_point(attendance:list) -> int:
    if not is_valid_attendance_cnt(attendance):
        raise Exception
    point = 0
    for i in range(7):
        if i == 2:
            point += attendance[i] * 3
        elif i == 5 or i == 6:
            point += attendance[i] * 2
        else:
            point += attendance[i]
    return point

def calculate_bonus_point(attendance:list) -> int:
    if not is_valid_attendance_cnt(attendance):
        raise Exception
    bonus_point = 0
    if attendance[2] > 9:
        bonus_point += 10
    if attendance[5] + attendance[6] > 9:
        bonus_point += 10
    return bonus_point