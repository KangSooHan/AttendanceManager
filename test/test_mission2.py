from attendance import input_file
from mission2.new_attendance import *
import pytest

@pytest.fixture
def right_inputs():
    attendance_manager = AttendanceManager("test/attendance_weekday_500.txt")
    attendance_manager.execute()
    return attendance_manager.get_attendance_list(), attendance_manager.get_player_list()

@pytest.fixture
def wrong_inputs():
    attendance_manager = AttendanceManager("test/attendance_weekday_parse480_player470.txt")
    attendance_manager.execute()
    return attendance_manager.get_attendance_list(), attendance_manager.get_player_list()

def test_파일이_없을_때():
    with pytest.raises(Exception):
        attendance_manager = AttendanceManager("WRONG")

def test_setting_player_information_오류(right_inputs):
    attendance_manager = AttendanceManager("test/attendance_weekday_500.txt")
    with pytest.raises(Exception):
        attendance_manager.setting_player_information([(1, 2, 3)])


def test_기존_결과와_수정_결과가_같은지(capsys):
    input_file()
    captured = capsys.readouterr()
    original_output = captured.out.strip()

    attendance_manager = AttendanceManager()
    attendance_manager.execute()

    captured = capsys.readouterr()
    modified_output = captured.out.strip()
    assert original_output == modified_output, "출력이 다릅니다!"


def test_parse_attendance_입력_예시(right_inputs, wrong_inputs):
    attendance_list, _ = right_inputs
    assert len(attendance_list) == 500

    attendance_list, _ = wrong_inputs
    assert len(attendance_list) == 480

def test_setting_player_information_입력_예시(right_inputs, wrong_inputs):
    _, players = right_inputs

    total_cnt = 0
    for _, player in players.items():
        for day_cnt in player.attendance:
            total_cnt += day_cnt
    assert total_cnt == 500

    _, players = wrong_inputs

    total_cnt = 0
    for _, player in players.items():
        for day_cnt in player.attendance:
            total_cnt += day_cnt
    assert total_cnt == 470

def test_calculate_player_score(right_inputs, wrong_inputs):
    _, players = right_inputs
    answers = [48, 45, 61, 91, 23, 127, 44, 22, 54, 58, 38, 79, 8, 42, 6, 24, 36, 13, 1]

    assert len(players) == len(answers)
    for (_, player), answer in zip(players.items(), answers):
        assert player.point == answer

    _, players = wrong_inputs
    answers = [47, 43, 59, 78, 21, 122, 40, 73, 36, 57, 42, 6, 24, 53, 36, 17, 13, 7, 1]
    assert len(players) == len(answers)
    for (_, player), answer in zip(players.items(), answers):
        assert player.point == answer

def test_calculate_player_grade(right_inputs, wrong_inputs):
    _, players = right_inputs
    answers = [2, 2, 1, 1, 0, 1, 2, 0, 1, 1, 2, 1, 0, 2, 0, 0, 2, 0, 0]
    assert len(players) == len(answers)
    for (_, player), answer in zip(players.items(), answers):
        assert player.grade() == answer

    _, players = wrong_inputs
    answers = [2, 2, 1, 1, 0, 1, 2, 1, 2, 1, 2, 0, 0, 1, 2, 0, 0, 0, 0]
    assert len(players) == len(answers)
    for (_, player), answer in zip(players.items(), answers):
        assert player.grade() == answer

add_new_player_test_data = [
    ([chr(ord('a') + i) for i in range(26)], 26),
    ([chr(ord('a') + i) for i in range(26)] + [chr(ord('a') + i) for i in range(26)], 26),
]
@pytest.mark.parametrize("names, expected", add_new_player_test_data)
def test_add_new_player_test_case(names, expected):
    player_id_dict = {}
    for name in names:
        add_new_player(player_id_dict, name)
    assert len(player_id_dict) == expected

day_index_test_data = [
    ("monday", 0),
    ("tuesday", 1),
    ("wednesday", 2),
    ("thursday", 3),
    ("friday", 4),
    ("saturday", 5),
    ("sunday", 6),
    ("wrong", -1),
    (1, -1)
]
@pytest.mark.parametrize("day, expected", day_index_test_data)
def test_day_index_test_case(day, expected):
    assert day_index(day).value == expected

is_no_attendance_necessary_day_test_data = [
    ([0, 0, 0, 0, 0, 0, 0], True),
    ([0, 1, 0, 1, 1, 0, 0], True),
    ([100, 100, 0, 100, 100, 0, 0], True),
    ([0, 0, 1, 0, 0, 0, 0], False),
    ([0, 0, 1, 0, 0, 1, 0], False),
    ([0, 0, 1, 0, 0, 0, 1], False),
    ([0, 0, 1, 0, 0, 1, 1], False),
]
@pytest.mark.parametrize("inputs, expected", is_no_attendance_necessary_day_test_data)
def test_is_no_attendance_necessary_day_test_case(inputs, expected):
    from mission2.utils.validate import is_no_attendance_necessary_day
    assert is_no_attendance_necessary_day(0, inputs) == expected

from mission2.utils.grade import Normal, Silver, Gold
is_removed_player_test_data = [
    (Normal(), [0, 0, 0, 0, 0, 0, 0], True),
    (Normal(), [0, 1, 0, 1, 1, 0, 0], True),
    (Normal(), [0, 0, 1, 0, 0, 0, 0], False),
    (Gold(), [0, 0, 0, 0, 0, 0, 0], False),
    (Silver(), [0, 0, 0, 0, 0, 0, 0], False),
]
@pytest.mark.parametrize("grade, cnt, expected", is_removed_player_test_data)
def test_is_removed_player_test_case(grade, cnt, expected):
    assert is_removed_player(0, grade, cnt) == expected


calculate_grade_from_point_test_data = [
    (50, 1),
    (30, 2),
    (0, 0),
]
@pytest.mark.parametrize("score, grade", calculate_grade_from_point_test_data)
def test_calculate_grade_from_point_test_case(score, grade):
    assert calculate_grade_from_point(score)() == grade

calculate_point_test_data = [
    ([0,0,0,0,0,0,0], 0, 0),
    ([10,10,10,10,10,10,10], 110, 20),
    ([1,3,5,7,9,11,13], 83, 10)
]
@pytest.mark.parametrize("cnt, basic, bonus", calculate_point_test_data)
def test_calculate_point_test_case(cnt, basic, bonus):
    assert calculate_basic_point(cnt) == basic
    assert calculate_bonus_point(cnt) == bonus


is_valid_attendance_cnt_wrong_input = [
    ([0, 0, 0, 0, 0, 0]),
    ([-1, -1, -1, -1, -1, -1, -1]),
]
@pytest.mark.parametrize("inputs", is_valid_attendance_cnt_wrong_input)
def test_is_valid_attendance_cnt_잘못된_입력(inputs):
    from mission2.utils.validate import is_no_attendance_necessary_day
    with pytest.raises(Exception):
        is_no_attendance_necessary_day(0, inputs)
    with pytest.raises(Exception):
        calculate_basic_point(inputs)
    with pytest.raises(Exception):
        calculate_bonus_point(inputs)
    with pytest.raises(Exception):
        is_removed_player(0, Normal(), inputs)

is_valid_player_id_and_point_wrong_input = [
    (-1),
    ("wrong")
]
@pytest.mark.parametrize("value", is_valid_player_id_and_point_wrong_input)
def test_is_valid_player_id_and_point_잘못된_입력(value):
    from mission2.utils.validate import is_valid_player_id_and_point, is_no_attendance_necessary_day
    assert is_valid_player_id_and_point(value) == False

    with pytest.raises(Exception):
        calculate_grade_from_point(value)
    with pytest.raises(Exception):
        is_removed_player(value, [0], [0,0,0,0,0,0,0])
    with pytest.raises(Exception):
        is_no_attendance_necessary_day(value, [0,0,0,0,0,0,0])


