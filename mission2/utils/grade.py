from abc import ABC, abstractmethod
from .validate import is_valid_player_id_and_point

class Grade(ABC):
    @abstractmethod
    def print(self):
        pass

    @abstractmethod
    def is_normal_grade(self):
        pass

    @abstractmethod
    def __call__(self):
        pass

class Gold(Grade):
    def print(self):
        print("GOLD")
    def is_normal_grade(self):
        return False
    def __call__(self):
        return 1

class Silver(Grade):
    def print(self):
        print("SILVER")
    def is_normal_grade(self):
        return False
    def __call__(self):
        return 2

class Normal(Grade):
    def print(self):
        print("NORMAL")

    def is_normal_grade(self):
        return True
    def __call__(self):
        return 0

def calculate_grade_from_point(player_point:int) -> Grade:
    if not is_valid_player_id_and_point(player_point):
        raise Exception
    if player_point >= 50:
        return Gold()
    elif player_point >= 30:
        return Silver()
    else:
        return Normal()