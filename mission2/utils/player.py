from dataclasses import dataclass, field
from .grade import Grade, Normal
from .validate import is_valid_attendance_cnt, is_valid_player_id_and_point, is_no_attendance_necessary_day

@dataclass
class Player:
    id:int
    name:str
    attendance:list = field(default_factory=lambda: [0, 0, 0, 0, 0, 0, 0])
    point:int = 0
    grade:Grade = field(default_factory=lambda: Normal())

def add_new_player(player_id_dict: dict, name: str):
    new_player_id = len(player_id_dict) + 1
    player_id_dict[name] = Player(new_player_id, name)

def is_removed_player(player_id: int, player_grade:Grade, player_day_attendance_cnt:list) -> bool:
    try:
        if not is_valid_player_id_and_point(player_id):
            raise Exception
        if not is_valid_attendance_cnt(player_day_attendance_cnt):
            raise Exception
        return player_grade.is_normal_grade() \
            and is_no_attendance_necessary_day(player_id, player_day_attendance_cnt)
    except Exception as e:
        raise Exception(f"is_removed_player : 에러가 발생했습니다. {e}")