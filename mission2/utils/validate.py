from .day import Day

def is_no_attendance_necessary_day(player_id: int, player_day_attendance_cnt:list)-> int:
    try:
        if not is_valid_player_id_and_point(player_id):
            raise Exception
        if not is_valid_attendance_cnt(player_day_attendance_cnt):
            print("DEBUG")
            raise Exception
        return player_day_attendance_cnt[Day.saturday.value] + player_day_attendance_cnt[Day.sunday.value] == 0 \
                and player_day_attendance_cnt[Day.wednesday.value] == 0
    except Exception as e:
        raise Exception(f"is_no_attendance_necessary_day : 에러가 발생했습니다. {e}")

def is_valid_player_id_and_point(value: int):
    if not isinstance(value, int):
        return False
    if value < 0:
        return False
    return True

def is_valid_attendance_cnt(player_day_attendance_cnt:list):
    if len(player_day_attendance_cnt) != 7:
        return False
    for day_attendance_cnt in player_day_attendance_cnt:
        if day_attendance_cnt < 0:
            return False
    return True