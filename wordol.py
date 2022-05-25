import json

with open('./WorDol/unit_list.json', 'r', encoding='utf-8-sig') as f:
    unit_list = json.load(f)

cate = unit_list['속성']
unit_list = unit_list['유닛']

def check_include(unit, idols:list):
    for idol in idols:
        if idol not in unit:
            return False
    return True


def check_num_people(unit, lengths:list):
    if len(lengths) == 0:
        return True

    for length in lengths:
        if len(unit) == length:
            return True
    return False


def check_exclude(unit, idols:list):
    for idol in idols:
        if idol in unit:
            return False
    return True


def check_category(unit, categories:dict):
    unit_category = {"프린세스":0, "페어리":0, "엔젤":0}

    for idol in unit:
        if idol in cate['프린세스']:
            unit_category['프린세스'] += 1
        elif idol in cate['페어리']:
            unit_category['페어리'] += 1
        else:
            unit_category['엔젤'] += 1

    for cat, num in categories.items():
        if num != unit_category[cat]:
            return False
    return True


include = []
exclude = ["아리사", "카나", "메구미"]
lengths = [3]
categories = {"프린세스":2, "페어리":0}


recommend = []
for name, unit in unit_list.items():
    if not check_include(unit, include):
        continue
    if not check_exclude(unit, exclude):
        continue
    if not check_num_people(unit, lengths):
        continue
    if not check_category(unit, categories):
        continue
    recommend.append((name, unit))

for name, unit in recommend:
    print(name, unit)