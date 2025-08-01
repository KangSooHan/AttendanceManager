import os
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