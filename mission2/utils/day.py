from enum import Enum

class Day(Enum):
    monday = 0
    tuesday = 1
    wednesday = 2
    thursday = 3
    friday = 4
    saturday = 5
    sunday = 6
    error = -1

def day_index(day:str) -> (int, int):
    if day == "monday":
        return Day.monday
    elif day == "tuesday":
        return Day.tuesday
    elif day == "wednesday":
        return Day.wednesday
    elif day == "thursday":
        return Day.thursday
    elif day == "friday":
        return Day.friday
    elif day == "saturday":
        return Day.saturday
    elif day == "sunday":
        return Day.sunday
    else: return Day.error

def is_error_day(day:Day)->bool:
    if day == Day.error:
        return True
    return False