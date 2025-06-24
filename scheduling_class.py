import pandas as pd
from itertools import product
import sys
from tkinter import * 
from tkinter import messagebox
import tkinter as tk

sys.stdout.reconfigure(encoding="utf-8")

f = open("C:\\schedule_Class\\class_name.txt", "r",encoding = "utf-8")

txt = f.readlines()
f.close()
txt =txt[0:]
#분반-수업명-H/A-교수명-시간,시간,시간


for i in  range(len(txt)):
   txt[i] = txt[i].strip().split('-')
   txt[i][0] = int(txt[i][0])
   txt[i][4] = txt[i][4].split(',')

#리스트를 데이터프레임을 변환
info = pd.DataFrame(txt,columns = ['분반','수업명','영or한','교수명','시간'])

class_list = info['분반'].tolist()
class_list = list(set(class_list))
#class_list = list(set(info['분반'].tolist()))
info_list= []
for class_num in class_list:
    info_list.append(info[info['분반']==class_num].drop(['분반'],axis=1))

# 전역 리스트에 모든 경우의 수(각 경우는 course dict들의 리스트)를 저장
all_schedules = []
current_index = 0


#모든 경우의 수 탐색
def generate_schdules(courses, current_schdule=[], index = 0):
    if index == len(courses):
        #print("가능한 시간표:", [(c["분반"], c["교수명"], c["시간"]) for c in current_schdule])
        all_schedules.append(current_schdule)
        return
    
    course_num = courses[index]
    options = info[info['분반']== course_num].to_dict('records')

    for option in options:
        if is_valid(current_schdule, option):
            generate_schdules(courses, current_schdule + [option], index+1)


def is_valid(schedule, new_course):
    new_times = set(new_course["시간"])

    for selected in schedule:
        existing_times = set(selected["시간"])
        if new_times & existing_times:
            return False
    return True

generate_schdules(class_list)
#print("총 생성된 시간표 경우의 수:", len(all_schedules))


day_to_col = {"월": 1, "화": 2, "수": 3, "목": 4, "금": 5}
color_list = ["lightblue", "lightgreen", "lightyellow", "lightpink", "lavender", "peachpuff", "lightcyan", "lightgray", "mistyrose", "honeydew", "aliceblue", "thistle"]

def gui():
    global current_index
    window = Tk()
    # label = Label(window, text='시간표',width = 20, height=2, bg = "yellow",relief="solid")
    # label.pack()
    window.geometry("640x800+150+10")
    window.resizable(False,False)
    top_frame = Frame(window)
    top_frame.pack(pady=10)

    next_button = Button(top_frame, text='BEFORE', width=10, command=lambda: before_schedule())
    next_button.pack(side=LEFT, padx=10)
    title_label = Label(top_frame, text="시간표\n모든 경우의 수:"+str(len(all_schedules)), width=20, height=2, bg="yellow", relief="solid")
    title_label.pack(side=LEFT, padx=10)
    next_button = Button(top_frame, text='NEXT', width=10, command=lambda: next_schedule())
    next_button.pack(side=LEFT, padx=10)
    

    master_frame = Frame(window)
    master_frame.pack(pady=10)

    # 헤더: 첫 행에 "교시"와 요일 이름 표시
    header_label = Label(master_frame, text="교시", width=5, height=2, relief="solid")
    header_label.grid(row=0, column=0, padx=1, pady=1)
    days = ['월', '화', '수', '목', '금']
    for idx, day in enumerate(days):
        day_label = Label(master_frame, text=day, width=15, height=2, relief="solid")
        day_label.grid(row=0, column=idx+1, padx=1, pady=1)


    # 좌측 열: 1교시 ~ 12교시 라벨
    for period in range(1, 13):
        period_label = Label(master_frame, text=str(period) + "교시", width=5, height=3, relief="solid")
        period_label.grid(row=period, column=0, padx=1, pady=1)

    # 스케줄 셀 생성: (요일, 교시)마다 Label 생성하고 dictionary에 저장
    schedule_cells = {}
    for period in range(1, 13):
        for day in days:
            cell = Label(master_frame, text="", width=15, height=3, relief="ridge", anchor="center")
            cell.grid(row=period, column=day_to_col[day], padx=1, pady=1)
            schedule_cells[(day, period)] = cell

    def update_schdule(schedule):
        for cell in schedule_cells.values():
            cell.config(text="")
        for course in schedule:
            course_name = course["수업명"]
            professor = course["교수명"]
            eng_or_kor = course["영or한"]
            times = course["시간"]
            #course_color = color_list[hash(course_name) % len(color_list)]
            for time_str in times:
                if len(time_str)>=2:
                    day = time_str[0]
                    try:
                       period = int(time_str[1:])  # 나머지: 교시
                    except ValueError:
                        continue
                    if (day, period) in schedule_cells:
                        # 이미 값이 있으면 줄바꿈하여 추가
                        current_text = schedule_cells[(day, period)].cget("text")
                        new_text = f"{course_name}{eng_or_kor}\n{professor}"
                        if current_text:
                            new_text = current_text + "\n" + new_text
                        schedule_cells[(day, period)].config(text=new_text)
                    

    def next_schedule():
        global current_index
        if all_schedules:
            current_index = (current_index+1)%len(all_schedules)
            update_schdule(all_schedules[current_index])
        else:
            messagebox.showinfo("info","유효한 시간표 없습니다.")

    def before_schedule():
        global current_index
        if all_schedules:
            current_index = (current_index-1)%len(all_schedules)
            update_schdule(all_schedules[current_index])
        else:
            messagebox.showinfo("info","유효한 시간표 없습니다.")

    if all_schedules:
        update_schdule(all_schedules[current_index])
    else:
        messagebox.showinfo("info","유효한 시간표 없습니다.")
    
    window.mainloop()

def main():
    gui()


if __name__ == "__main__":
    main()