from config import *


def islevel2(file, level=2):
    with open(file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            if level == 2:
                if "Level II" in line or "Level III" in line:
                    return True
            if level == 3:
                if "Level III" in line:
                    return True
        return False


def islevel3(file):
    with open(file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            if "Level III" in line:
                return True
        return False