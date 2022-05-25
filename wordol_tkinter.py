from tkinter import *
import tkinter.ttk as ttk
import os
import sys
import json
from tkscrolledframe import ScrolledFrame
from PIL import ImageTk, Image
import webbrowser

root = Tk()
root.title("WorDol Helper")


# pyinstaller를 위한 path 코드 (내장 파일)
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

icon = resource_path("icon.ico")
root.iconbitmap(default = icon)


# wordol 알고리즘
unit_list_file = './unit_list.json'
with open(unit_list_file, 'r', encoding='utf-8-sig') as f:
    unit_list = json.load(f)

cate = unit_list['속성']
unit_list = unit_list['유닛']

def check_include(unit, idols:list):
    for idol in idols:
        if idol not in unit:
            return False
    return True


def check_num_people(unit, length=0):
    if length == 0:
        return True

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


def search(include, exclude, length, categories):
    recommend = []
    for name, unit in unit_list.items():
        
        if not check_include(unit, include):
            continue
        if not check_exclude(unit, exclude):
            continue
        if not check_num_people(unit, length):
            continue
        if not check_category(unit, categories):
            continue
        recommend.append((name, unit))

        
    return recommend


# include = []
# exclude = ["아리사", "카나", "메구미"]
# lengths = [3]
# categories = {"프린세스":2, "페어리":0}

# 조건 입력창
# 포함
frame_include = LabelFrame(root, text='포함 아이돌(띄어쓰기로 구분)')
frame_include.pack(padx=5, pady=5, ipady=5, fill='x', side='top')
entry_include = Entry(frame_include, justify='left')
entry_include.pack(side='left', fill='x',padx=5, pady=5, ipady=4, expand=True)

# 제외
frame_exclude = LabelFrame(root, text='제외 아이돌(띄어쓰기로 구분)')
frame_exclude.pack(padx=5, pady=5, ipady=5, fill='x', side='top')
entry_exclude = Entry(frame_exclude, justify='left')
entry_exclude.pack(side='left', fill='x',padx=5, pady=5, ipady=4, expand=True)


# 숫자만 입력 받도록
def testVal(inStr,acttyp):
    if acttyp == '1': #insert
        if not inStr.isdigit():
            return False
    return True

# 속성
frame_cate = LabelFrame(root, text='속성별 아이돌 수')
frame_cate.pack(padx=5, pady=5, ipady=5, side='top', fill='x')


## 프린세스
label_prin = Label(frame_cate, text='프린세스')
label_prin.pack(side='left', padx=3, pady=5)

entry_prin = Entry(frame_cate, justify='left', width=5, validate="key")
entry_prin.pack(side='left', fill='x',padx=5, pady=5, ipady=4, expand=False)
entry_prin['validatecommand'] = (entry_prin.register(testVal),'%P','%d')


## 페어리
label_fairy = Label(frame_cate, text='페어리')
label_fairy.pack(side='left', padx=3, pady=5)

entry_fairy = Entry(frame_cate, justify='left', width=5, validate="key")
entry_fairy.pack(side='left', fill='x',padx=5, pady=5, ipady=4, expand=False)
entry_fairy['validatecommand'] = (entry_fairy.register(testVal),'%P','%d')


## 엔젤
label_angel = Label(frame_cate, text='엔젤')
label_angel.pack(side='left', padx=3, pady=5)

entry_angel = Entry(frame_cate, justify='left', width=5, validate="key")
entry_angel.pack(side='left', fill='x',padx=5, pady=5, ipady=4, expand=False)
entry_angel['validatecommand'] = (entry_angel.register(testVal),'%P','%d')




# 유닛의 아이돌 수
frame_length = LabelFrame(root, text='유닛의 아이돌 수')
frame_length.pack(padx=5, pady=5, ipady=5, side='top', fill='x')
entry_length = Entry(frame_length, justify='left', width=5, validate="key")
entry_length.pack(side='left', fill='x',padx=5, pady=5, ipady=4, expand=False)
entry_length['validatecommand'] = (entry_length.register(testVal),'%P','%d')

opt_length = ['=', '≥', '≤']
cmb_length = ttk.Combobox(frame_length, state='readonly', values=opt_length, width=4)
cmb_length.current(0)
cmb_length.pack(side='left', padx=1, pady=5)



# 탐색 버튼
## 진행 상황 progress bar
frame_progress = LabelFrame(root, text='진행 상황')
frame_progress.pack(fill='x', padx=5, pady=5, ipady=5)

p_var = DoubleVar()
progress_bar = ttk.Progressbar(frame_progress, maximum=100, variable=p_var)
progress_bar.pack(fill='x', padx=5, pady=5)

frame_run = Frame(root)
frame_run.pack(fill='x', padx=5, pady=5)

def close_program():
    root.destroy()
    root.quit()

lfs = []
def main(event=None):
    global lfs
    for lf in lfs:
        lf.destroy()
    sf.yview_moveto("0.0")
    root.update()

    try:
        include = entry_include.get().split()
    except:
        include = []
    
    try:
        exclude = entry_exclude.get().split()
    except:
        exclude = []

    try:
        lengths = int(entry_length.get())
    except:
        lengths = 0
    
    categories = {}
    if entry_prin.get():
        categories['프린세스'] = int(entry_prin.get())
    
    if entry_fairy.get():
        categories['페어리'] = int(entry_fairy.get())

    if entry_angel.get():
        categories['엔젤'] = int(entry_angel.get())
    
    recommend = []
    
    cond_len = cmb_length.get()
    
    if lengths and cond_len == '≥':
        for length in range(max(lengths, 1), 5+1):
            recommend += search(include, exclude, length, categories)
    elif lengths and cond_len == '≤':
        for length in range(1, lengths+1):
            recommend += search(include, exclude, length, categories)
    else:
        recommend += search(include, exclude, lengths, categories)
    
    for i, (name, unit) in enumerate(recommend):
        lf = LabelFrame(frame, text=name)
        lf.pack(side='top', fill='x', expand=True)
        lfs.append(lf)
        # Label(lf, text=', '.join(unit)).pack(expand=True, fill='x')
        for idol in unit:
            if idol in cate['프린세스']: color='#FF6DB9'
            if idol in cate['페어리']: color='#7390FF'
            if idol in cate['엔젤']: color='#FFF353'

            file_name = f'./images/{idol}.jpg'
            idol_img = ImageTk.PhotoImage(Image.open(file_name))
            border = Frame(lf, background=color)
            border.pack(side='left', padx=1, pady=1)
            imglabel = Label(border)
            imglabel.configure(image=idol_img)
            imglabel.image = idol_img
            imglabel.pack(side='left', padx=3, pady=3)
        p_var.set((i+1)/(len(recommend))*100)
        progress_bar.update()
    root.update()

btn_close = Button(frame_run, padx=5, pady=5, text='닫기', width=12, command=close_program)
btn_close.pack(side='right', padx=5, pady=5)

btn_start = Button(frame_run, padx=5, pady=5, text='실행', width=12, command=main)
btn_start.pack(side='right', padx=5, pady=5)

def open_web():
    webbrowser.open('https://app.39m.ltd/games/wordol/')
btn_wordol = Button(frame_run, padx=5, pady=5, text='워돌로 바로가기', width=12, command=open_web)
btn_wordol.pack(side='left', padx=5, pady=5)


# 결과 프레임
result_frame = LabelFrame(root, text='결과')
result_frame.pack(fill='both', padx=5, pady=5, expand=True, side='top')

sf = ScrolledFrame(result_frame, scrollbars="vertical")
sf.pack(side="top", expand=True, fill="both")

sf.bind_arrow_keys(result_frame)
sf.bind_scroll_wheel(result_frame)


frame = sf.display_widget(Frame, fit_width=True)

root.bind("<Return>", lambda event:main(event))

root.resizable(False, False)
root.geometry("600x720")

root.mainloop()
