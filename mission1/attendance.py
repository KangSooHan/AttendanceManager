import os

def attendance_manager():
    try:
        attendance_list = parse_attendance("attendance_weekday_500.txt")
        if attendance_list:
            player_id_dict, player_day_attendance_cnt = setting_player_information(attendance_list)
            player_points = calculate_player_score(player_id_dict, player_day_attendance_cnt)
            player_grades = calculate_player_grade(player_id_dict, player_points)
            print_result(player_id_dict, player_points, player_grades, player_day_attendance_cnt)

    except Exception as e:
        print(f"Attendance_Manager : 에러가 발생했습니다: {e}")

def parse_attendance(path:str) -> list[list]:
    try:
        lines = []
        if not os.path.exists(path):
            raise FileNotFoundError("parse_attendance : 파일을 찾을 수 없습니다.")

        with open(path, encoding='utf-8') as f:
            for _ in range(500):
                line = f.readline()
                if not line:
                    break
                parts = line.strip().split()
                if len(parts) == 2:
                    lines.append(parts)
                else:
                    print(f"parse_attendance : 잘못된 입력이 들어왔습니다. {parts}")
        return lines
    except Exception as e:
        raise Exception(f"parse_attendance : 에러가 발생했습니다: {e}")

def setting_player_information(attendance_list):
    player_id_dict = {}
    player_day_attendance_cnt = [[0 for _ in range(7)]]
    for info in attendance_list:
        try:
            name, day = info
            if name not in player_id_dict:
                add_new_player(player_id_dict, name)
                player_day_attendance_cnt.append([0 for _ in range(7)])
            player_id = player_id_dict[name]
            index = day_index(day)
            if index == -1:
                print(f"setting_player_information : 잘못된 날짜 입력 ({day}) 이 발생했습니다.")
                continue
            player_day_attendance_cnt[player_id][index] += 1
        except:
            print(f"setting_player_information : {info}에서 에러가 발생했습니다.")
    return player_id_dict, player_day_attendance_cnt

def calculate_player_score(player_id_dict:dict, player_attendance_cnt:list):
    if not is_valid_attendance_cnt(player_attendance_cnt):
        raise Exception
    player_points = [0 for _ in range(len(player_id_dict) + 1)]
    for name, player_id in player_id_dict.items():
        try:
            player_points[player_id] += calculate_basic_point(player_attendance_cnt[player_id])
            player_points[player_id] += calculate_bonus_point(player_attendance_cnt[player_id])
        except:
            print(f"calculate_score_and_grade : Bonus Point 계산 시 오류가 발생했습니다.")
    return player_points

def calculate_basic_point(attendance_cnt) -> int:
    if not is_valid_attendance_cnt:
        raise Exception
    point = 0
    for i in range(7):
        if i == 2:
            point += attendance_cnt[i] * 3
        elif i == 5 or i == 6:
            point += attendance_cnt[i] * 2
        else:
            point += attendance_cnt[i]
    return point

def add_new_player(player_id_dict: dict, name: str):
    try:
        new_player_id = len(player_id_dict) + 1
        player_id_dict[name] = new_player_id
    except Exception as e:
        raise Exception(f"add_new_player : 에러가 발생했습니다. {e}")

def day_index(day:str) -> (int, int):
    if day == "monday":
        return 0
    elif day == "tuesday":
        return 1
    elif day == "wednesday":
        return 2
    elif day == "thursday":
        return 3
    elif day == "friday":
        return 4
    elif day == "saturday":
        return 5
    elif day == "sunday":
        return 6
    else: return -1

def calculate_bonus_point(attendance_cnt:list) -> int:
    if not is_valid_attendance_cnt:
        raise Exception
    bonus_point = 0
    if attendance_cnt[2] > 9:
        bonus_point += 10
    if attendance_cnt[5] + attendance_cnt[6] > 9:
        bonus_point += 10
    return bonus_point


def calculate_grade_from_point(player_point:int) -> int:
    if not is_valid_player_id_and_point(player_point):
        raise Exception
    if player_point >= 50:
        return 1
    elif player_point >= 30:
        return 2
    else:
        return 0

def calculate_player_grade(player_id_dict: dict, player_points:list) -> list:
    player_grades = [0 for _ in range(len(player_id_dict)+1)]
    for name, player_id in player_id_dict.items():
        try:
            player_grades[player_id] = calculate_grade_from_point(player_points[player_id])
        except Exception as e:
            print(f"calculate_player_grade : Grade 계산 시 오류가 발생했습니다. {e}")
    return player_grades

def print_result(player_id_dict: dict, player_points:list, player_grades:list, player_day_attendance_cnt:list):
    print_player_point_and_grade(player_id_dict, player_points, player_grades)
    print_removed_player(player_id_dict, player_points, player_grades, player_day_attendance_cnt)

def print_player_point_and_grade(player_id_dict:dict, player_points: list, player_grades: list) -> None:
    for player_name, player_id in player_id_dict.items():
        print(f"NAME : {player_name}, POINT : {player_points[player_id]}, GRADE : ", end="")
        player_grade = player_grades[player_id]
        if player_grade == 1:
            print("GOLD")
        elif player_grade == 2:
            print("SILVER")
        else:
            print("NORMAL")

def print_removed_player(player_id_dict: dict, player_points: list, player_grades: list, player_day_attendance_cnt:list) -> None:
    print("\nRemoved player")
    print("==============")
    for name, player_id in player_id_dict.items():
        if is_removed_player(player_id, player_grades, player_day_attendance_cnt):
            try:
                print(name)
            except:
                continue

def is_removed_player(player_id: int, player_grades:list, player_day_attendance_cnt:list) -> bool:
    try:
        if not is_valid_player_id_and_point(player_id):
            raise Exception
        if not is_valid_attendance_cnt(player_day_attendance_cnt):
            raise Exception
        return player_grades[player_id] == 0 \
            and is_no_attendance_necessary_day(player_id, player_day_attendance_cnt)
    except Exception as e:
        raise Exception(f"is_removed_player : 에러가 발생했습니다. {e}")

def is_no_attendance_necessary_day(player_id: int, player_day_attendance_cnt:list)-> int:
    try:
        if not is_valid_player_id_and_point(player_id):
            raise Exception
        if not is_valid_attendance_cnt(player_day_attendance_cnt):
            raise Exception
        return player_day_attendance_cnt[player_id][5] + player_day_attendance_cnt[player_id][6] == 0 \
                and player_day_attendance_cnt[player_id][2] == 0
    except Exception as e:
        raise Exception(f"is_no_attendance_necessary_day : 에러가 발생했습니다. {e}")

def is_valid_player_id_and_point(value: int):
    if not isinstance(value, int):
        return False
    if value < 0:
        return False
    return True

def is_valid_attendance_cnt(player_day_attendance_cnt:list):
    for player_attendance_cnt in player_day_attendance_cnt:
        if len(player_attendance_cnt) != 7:
            return False
        for day_attendance_cnt in player_attendance_cnt:
            if day_attendance_cnt < 0:
                return False
    return True

if __name__ == "__main__":
    attendance_manager()
