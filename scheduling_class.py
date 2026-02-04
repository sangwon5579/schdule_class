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

#분반-수업명-H/A-교수명-시간,시간,시간
for i in range(len(txt)):
    txt[i] = txt[i].strip().split('-')
    txt[i][0] = int(txt[i][0])
    txt[i][4] = txt[i][4].split(',')

info = pd.DataFrame(txt,columns = ['분반','수업명','영or한','교수명','시간'])

class_list = list(set(info['분반'].tolist()))

info_list= []
for class_num in class_list:
    info_list.append(info[info['분반']==class_num].drop(['분반'],axis=1))

all_schedules = []
current_index = 0


# 모든 경우의 수 탐색
def generate_schdules(courses, current_schdule=[], index=0):
    if index == len(courses):
        all_schedules.append(current_schdule)
        return
    
    course_num = courses[index]
    options = info[info['분반']==course_num].to_dict('records')

    for option in options:
        if is_valid(current_schdule, option):
            generate_schdules(courses, current_schdule+[option], index+1)


def is_valid(schedule, new_course):
    new_times = set(new_course["시간"])
    for selected in schedule:
        if new_times & set(selected["시간"]):
            return False
    return True


generate_schdules(class_list)


day_to_col = {"월":1,"화":2,"수":3,"목":4,"금":5}

color_list = [
    "lightblue","lightgreen","lightyellow","lightpink","lavender",
    "peachpuff","lightcyan","lightgray","mistyrose","honeydew",
    "aliceblue","thistle"
]


def gui():
    global current_index

    window = Tk()
    window.geometry("640x800+150+10")
    window.resizable(False,False)

    course_colors = {}
    unique_courses = info["수업명"].unique()

    for i, cname in enumerate(unique_courses):
        course_colors[cname] = color_list[i % len(color_list)]

    top_frame = Frame(window)
    top_frame.pack(pady=10)

    Button(top_frame,text='BEFORE',width=10,
           command=lambda: before_schedule()).pack(side=LEFT,padx=10)

    schedule_label = Label(
        top_frame,
        text=f"시간표 {current_index+1}/{len(all_schedules)}\n모든 경우의 수:{len(all_schedules)}",
        width=20,height=2,bg="yellow",relief="solid"
    )
    schedule_label.pack(side=LEFT,padx=10)

    Button(top_frame,text='NEXT',width=10,
           command=lambda: next_schedule()).pack(side=LEFT,padx=10)


    master_frame = Frame(window)
    master_frame.pack(pady=10)

    Label(master_frame,text="교시",width=5,height=2,
          relief="solid").grid(row=0,column=0)

    days=['월','화','수','목','금']

    for idx,day in enumerate(days):
        Label(master_frame,text=day,width=15,height=2,
              relief="solid").grid(row=0,column=idx+1)

    for period in range(1,13):
        Label(master_frame,text=str(period)+"교시",
              width=5,height=3,relief="solid"
        ).grid(row=period,column=0)

    schedule_cells={}
    for period in range(1,13):
        for day in days:
            cell=Label(master_frame,text="",width=15,height=3,
                       relief="ridge",anchor="center",bg="white")
            cell.grid(row=period,column=day_to_col[day])
            schedule_cells[(day,period)]=cell


    def update_schdule(schedule):
        # 초기화
        for cell in schedule_cells.values():
            cell.config(text="", bg="white")

        for course in schedule:
            cname=course["수업명"]
            professor=course["교수명"]
            eng=course["영or한"]
            times=course["시간"]

            course_color = course_colors.get(cname,"white")

            for time_str in times:
                if len(time_str)>=2:
                    day=time_str[0]
                    try:
                        period=int(time_str[1:])
                    except:
                        continue

                    if (day,period) in schedule_cells:
                        cell=schedule_cells[(day,period)]

                        current_text=cell.cget("text")
                        new_text=f"{cname}{eng}\n{professor}"

                        if current_text:
                            new_text=current_text+"\n"+new_text

                        cell.config(
                            text=new_text,
                            bg=course_color 
                        )


    def next_schedule():
        global current_index
        if all_schedules:
            current_index=(current_index+1)%len(all_schedules)
            update_schdule(all_schedules[current_index])
            schedule_label.config(text=f"시간표 {current_index+1}/{len(all_schedules)}\n모든 경우의 수:{len(all_schedules)}")
        else:
            messagebox.showinfo("info","유효한 시간표 없습니다.")


    def before_schedule():
        global current_index
        if all_schedules:
            current_index=(current_index-1)%len(all_schedules)
            update_schdule(all_schedules[current_index])
            schedule_label.config(text=f"시간표 {current_index+1}/{len(all_schedules)}\n모든 경우의 수:{len(all_schedules)}")
        else:
            messagebox.showinfo("info","유효한 시간표 없습니다.")


    if all_schedules:
        update_schdule(all_schedules[current_index])
    else:
        messagebox.showinfo("info","유효한 시간표 없습니다.")

    window.mainloop()


def main():
    gui()

if __name__=="__main__":
    main()
