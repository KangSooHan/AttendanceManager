from attendance import input_file
from mission1.attendance import attendance_manager

def test_기존_결과와_수정_결과가_같은지(capsys):
    input_file()
    captured = capsys.readouterr()
    original_output = captured.out.strip()

    attendance_manager()
    captured = capsys.readouterr()
    modified_output = captured.out.strip()
    assert original_output == modified_output, "출력이 다릅니다!"