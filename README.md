schdule_class  
시간표의 경우의 수를 보여주는 프로그램입니다.    
python으로 작성되었으며, 주요 사용 알고리즘은 backtracking 알고리즘입니다.  
class_name.txt 파일에는 자신이 수강할 수업들을 입력합니다.  
각 선택지마다 같은 순번을 부여합니다.  
총 6개의 수업을 듣는다면 1~6번의 순번이 생기게 됩니다(중복가능)  
txt파일은 순서대로 순번-과목명-영어/한국어-교수님-수업시간(1시간 단위로 ,로 구분하여 작성) 입니다.
.exe 또는 .py파일을 통해 실행하면 아래와 같은 GUI가 출력됩니다.
![image](https://github.com/user-attachments/assets/985b9de3-b949-4bef-a0d3-1bff0df9cf11)
제일 상단에는 모든 경우의 수를 보여주며 NEXT, BEFORE 버튼을 통해 시간표들을 직접 확인할 수 있습니다.

요구사항  
python 3.10 이상  
pandas  
tkinter  
