from mission2.utils.player import add_new_player, is_removed_player, Player
from mission2.utils.grade import calculate_grade_from_point
from mission2.utils.point import calculate_bonus_point, calculate_basic_point
from mission2.utils.day import day_index, is_error_day
from mission2.utils.parser import parse_attendance

class AttendanceManager:
    def __init__(self, path:str ="attendance_weekday_500.txt"):
        self.attendance_list = parse_attendance(path)
        self.player_list:dict = {}
        self.setting_player_information(self.attendance_list)

    def get_player_list(self):
        return self.player_list

    def get_attendance_list(self):
        return self.attendance_list

    def setting_player_information(self, attendance_list:list):
        for info in attendance_list:
            try:
                name, day_string = info
                if name not in self.player_list:
                    add_new_player(self.player_list, name)

                day = day_index(day_string)
                if is_error_day(day):
                    print(f"setting_player_information : 잘못된 날짜 입력 ({day}) 이 발생했습니다.")
                    continue
                self.player_list[name].attendance[day.value] += 1
            except:
                raise Exception(f"setting_player_information : {info}에서 에러가 발생했습니다.")

    def calculate_player_score(self):
        for name, player in self.player_list.items():
            player.point += calculate_basic_point(player.attendance)
            player.point += calculate_bonus_point(player.attendance)

    def calculate_player_grade(self):
        for name, player in self.player_list.items():
            player.grade = calculate_grade_from_point(player.point)

    def print_result(self):
        for name, player in self.player_list.items():
            self.print_player_point_and_grade(player)
        self.print_removed_player()


    def execute(self):
        self.calculate_player_score()
        self.calculate_player_grade()
        self.print_result()

    def print_player_point_and_grade(self, player:Player) -> None:
        print(f"NAME : {player.name}, POINT : {player.point}, GRADE : ", end="")
        player.grade.print()

    def print_removed_player(self) -> None:
        print("\nRemoved player")
        print("==============")
        for name, player in self.player_list.items():
            if is_removed_player(player.id, player.grade, player.attendance):
                print(name)