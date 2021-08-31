import tkinter as tk
from tkinter import font  as tkfont
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox
from tkinter import * # __all__
from tkinter import filedialog
# from PIL import ImageTk, Image
import time
import analysis_def
import pymysql

# local
# conn = pymysql.connect(host='localhost', user='outside', password='outP@ssw0rd1!',
#                        db='login', charset='utf8')
# AWS
conn = pymysql.connect(host='db-2.cjfiturksrlr.ap-northeast-2.rds.amazonaws.com', user='yeschan', password='yeschan119',
                       db='PV_DB', charset='utf8')

curs = conn.cursor()
sql= 'select * from login'
curs.execute(sql)
rows = curs.fetchall()

user = {}
limit = {}
tp = {}
for id, email, pw, type, cnt in rows:
    user[email] = pw
    limit[email] = cnt
    tp[email] = type
print(user)

x = None

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Malgun Gothic', size=18, weight="bold")
        # self.geometry("300x300+100+100")
        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        controller.title('품목갱신 원시자료 분석')
        controller.option_add('*Font','나눔고딕 10')
        # controller.iconbitmap('C:/Users/User/Documents/_지선/02.프로젝트진행/03.PV팀/github/update/daewoong.ico')
        self.cnt = 0
        label = tk.Label(self, text="로그인", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        # win = Tk()
        # win.title("로그인")
        # win.geometry("600x300+500+500")
        # win.option_add("*Font", "나눔고딕 10")
        # win.resizable(False, False)

        # img = ImageTk.PhotoImage(Image.open('update_20210724/대웅.png'))
        # lab = Label(self, image=img)
        # lab.pack()

        lab1 = Label(self, text="ID")
        lab2 = Label(self, text="PW")

        ent1 = Entry(self)
        ent1.insert(0,'이메일을 입력해주세요.')
        def clear(event):
            if ent1.get()=='이메일을 입력해주세요.':
                ent1.delete(0,len(ent1.get()))
        ent1.bind('<Button-1>',clear)
        lab1.pack()
        ent1.pack()

        ent2 = Entry(self)
        ent2.config(show='*')
        lab2.pack()
        ent2.pack()
        
        def login():
            my_id = ent1.get()
            my_pwd = ent2.get()
            print(my_id,my_pwd)
            # 로그인 불가할 때
            if len(my_id)==0 or user[my_id]!=my_pwd:
                msgbox.showinfo('알림','아이디/비밀번호가 틀렸습니다.')
                self.cnt = 0
            # 로그인 되었을 때
            else:
                msgbox.showinfo("알림", "로그인되었습니다.")
                global x
                x = ent1.get()
                self.cnt = 1
                controller.show_frame('PageOne')
        def callback(event):
            login()

        btn = tk.Button(self, text="로그인", command=login)
        btn.pack()

        # controller.bind('<Return>', callback)

        # button1 = tk.Button(self, text="login",
        #                     command=lambda: controller.show_frame("PageOne"))
        # button2 = tk.Button(self, text="Go to Page Two",
        #                     command=lambda: controller.show_frame("PageTwo"))
        # button1.pack()
        # button2.pack()


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        # 파일 프레임 (파일 추가, 선택 삭제)
        self.controller.file_frame = Frame(self)
        self.controller.file_frame.pack(fill="x", padx=5, pady=5) # 간격 띄우기

        self.controller.btn_add_file = Button(self.controller.file_frame, padx=5, pady=5, width=12, text="파일추가", command=self.add_file)
        self.controller.btn_add_file.pack(side="left")

        self.controller.btn_del_file = Button(self.controller.file_frame, padx=5, pady=5, width=12, text="선택삭제", command=self.del_file)
        self.controller.btn_del_file.pack(side="right")

        # 리스트 프레임
        self.controller.list_frame = Frame(self)
        self.controller.list_frame.pack(fill="both", padx=5, pady=5)

        scrollbar = Scrollbar(self.controller.list_frame)
        scrollbar.pack(side="right", fill="y")

        self.controller.list_file = Listbox(self.controller.list_frame, selectmode="extended", height=15, yscrollcommand=scrollbar.set)
        self.controller.list_file.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.controller.list_file.yview)

        # 저장 경로 프레임
        self.controller.path_frame = LabelFrame(self, text="저장경로")
        self.controller.path_frame.pack(fill="x", padx=5, pady=5, ipady=5)

        self.controller.txt_dest_path = Entry(self.controller.path_frame)
        self.controller.txt_dest_path.pack(side="left", fill="x", expand=True, padx=5, pady=5, ipady=4) # 높이 변경

        self.controller.btn_dest_path = Button(self.controller.path_frame, text="찾아보기", width=10, command=self.browse_dest_path)
        self.controller.btn_dest_path.pack(side="right", padx=5, pady=5)

        # 옵션 프레임
        self.controller.frame_option = LabelFrame(self, text="옵션")
        self.controller.frame_option.pack(padx=5, pady=5, ipady=5)

        # 1. 제품 코드 옵션
        # 제품 코드 레이블
        self.controller.lab1 = Label(self.controller.frame_option, text="제품코드", width=8, anchor = "nw")
        self.controller.lab1.grid(row=1,column=1,sticky=W,pady=5)

        # 제품 코드 엔트리
        self.controller.ent1 = Entry(self.controller.frame_option)
        self.controller.ent1.insert(0, "********")
        def clear(event):
            if self.controller.ent1.get() == ("********"):
                self.controller.ent1.delete(0, len(self.controller.ent1.get()))

        self.controller.ent1.bind("<Button-1>", clear)
        self.controller.ent1.grid(row=1,column=2)

        # 2. 파일 포맷 옵션
        # 파일 포맷 옵션 레이블
        lab2 = Label(self.controller.frame_option, text="종류", width=8, anchor = "w")
        lab2.grid(row=1,column=3,sticky=W,pady=5)

        # 파일 포맷 옵션 콤보
        opt_format = ["line listing", "summary tabulation"]
        self.controller.cmb_format = ttk.Combobox(self.controller.frame_option, state="readonly", values=opt_format, width=16)
        self.controller.cmb_format.current(0)
        self.controller.cmb_format.grid(row=1,column=4)

        # 3. 보고기한

        # 시작일자 엔트리
        lab3_1 = Label(self.controller.frame_option, text="시작일자", width=8, anchor="w")
        lab3_1.grid(row=3,column=1,sticky=W,pady=5)

        self.controller.ent_start = Entry(self.controller.frame_option)
        self.controller.ent_start.insert(0, "********")
        def clear(event):
            if self.controller.ent_start.get() == ("********"):
                self.controller.ent_start.delete(0, len(self.controller.ent_start.get()))

        self.controller.ent_start.bind("<Button-1>", clear)
        self.controller.ent_start.grid(row=3,column=2,sticky=W,pady=5)

        # 종료일자 엔트리
        lab3_2 = Label(self.controller.frame_option, text="종료일자", width=8, anchor="w")
        lab3_2.grid(row=3,column=3,sticky=W,pady=5)

        self.controller.ent_end = Entry(self.controller.frame_option)
        self.controller.ent_end.insert(0, "********")
        def clear(event):
            if self.controller.ent_end.get() == ("********"):
                self.controller.ent_end.delete(0, len(self.controller.ent_end.get()))

        self.controller.ent_end.bind("<Button-1>", clear)
        self.controller.ent_end.grid(row=3,column=4,sticky=W,pady=5)

        # 4. 진행상황
        # 진행상황 Progress Bar
        self.controller.frame_progress = LabelFrame(self, text="진행상황")
        self.controller.frame_progress.pack(fill="x", padx=5, pady=5, ipady=5)

        p_var = DoubleVar()
        self.controller.progress_bar = ttk.Progressbar(self.controller.frame_progress, maximum=100, mode='determinate')
        self.controller.progress_bar.pack(fill="x", padx=5, pady=5)

        # 실행 프레임
        self.controller.frame_run = Frame(self)
        self.controller.frame_run.pack(fill="x", padx=5, pady=5)

        self.controller.btn_close = Button(self.controller.frame_run, padx=5, pady=5, text="닫기", width=12, command=parent.destroy)
        self.controller.btn_close.pack(side="right", padx=5, pady=5)

        self.controller.btn_start = Button(self.controller.frame_run, padx=5, pady=5, text="시작", width=12, command=self.start)
        self.controller.btn_start.pack(side="right", padx=5, pady=5)

        def callback(event):
            self.start()
        # controller.bind('<Return>', callback)

    # 파일 추가
    def add_file(self):
        files = filedialog.askopenfilenames(title="Open Data files 모든 데이터 파일을 업로드해주세요.", \
                                        filetypes=(("data files", "*.txt"), ("모든 파일", "*.*")), \
                                        initialdir=r"C:\Users\User\Kids")
                                            # 최초에 사용자가 지정한 경로를 보여줌
        
        # 사용자가 선택한 파일 목록
        lists = []
        for f in files:
            self.controller.list_file.insert(END, f)
            # print(f)
        print('list_file:',self.controller.list_file.get(0,self.controller.list_file.size()))

    # 선택 삭제
    def del_file(self):
        # print(list_file.curselection())
        for index in reversed(self.controller.list_file.curselection()):
            self.controller.list_file.delete(index)

    # 저장 경로 (폴더)
    def browse_dest_path(self):
        folder_selected = filedialog.askdirectory()
        print('선택된폴더:',folder_selected)
        if folder_selected == '': # 사용자가 취소를 누를 때
            # print("폴더 선택 취소")
            return
        # print("folder_selected")
        self.controller.txt_dest_path.delete(0, END)
        self.controller.txt_dest_path.insert(0, folder_selected)
        
    # 자료 분석
    def code_summary(self):
        # 필요한 기본정보 세팅

        # 파일리스트 불러오기
        files = self.controller.list_file.get(0,self.controller.list_file.size())
        check = 0
        for i in files:
            if 'GROUP.txt' in i:
                check+=1
            elif 'ADR_INFO_REPORT.txt' in i:
                check+=1
            elif 'ADR_REPORT_BASIC.txt' in i:
                check+=1
            elif 'ASSESSMENT_ADR.txt' in i:
                check+=1
            elif 'DRUG_INFO_ADR.txt' in i:
                check+=1
            # elif 'MedDRA 영문_한글화.xlsx' in i:
            #     check+=1

        if check==5:
            # 폴더, 보고일자, 코드 불러오기
            folder = self.controller.txt_dest_path.get()
            startdate = int(self.controller.ent_start.get())
            enddate = int(self.controller.ent_end.get())
            drug_cd = int(self.controller.ent1.get())

            for i in range(1,61):
                time.sleep(0.03)
                self.controller.progress_bar['value']+= i
                self.controller.progress_bar.update()

            # "line listing" "summary tabulation" 선택 후 파일 저장
            lt = analysis_def.analysis(files, folder, startdate, enddate, drug_cd)
            if self.controller.cmb_format.get()=='line listing':
                num = lt.linelisting()
            elif self.controller.cmb_format.get()=='summary tabulation':
                num = lt.summary()

            if num == 0:
                self.controller.progress_bar['value']=0
                self.controller.progress_bar.update()
                msgbox.showinfo("알림", "해당 제품코드의 이상사례가 없습니다.")
                return

            # print(list_file.get(0, END))
            # summary = [open(x) for x in list_file.get(0, END)]

        #     try:
                # 포맷
            # code_format = cmb_format.get().lower() # XLS, DOC, HWP 값을 받아와서 소문자로 변경

            self.controller.progress_bar['value']+= 20
            self.controller.progress_bar.update()
            
                # 포맷 옵션 처리
            # file_name = "SUMMARY." + code_format
            msgbox.showinfo("알림", "작업이 완료되었습니다.")
            self.controller.progress_bar['value']=0
            self.controller.progress_bar.update()
        #     except Exception as err: #  예외처리
        #         msgbox.showerror("에러", err)

        else:
            self.controller.progress_bar['value'] = 0
            self.controller.progress_bar.update()
            msgbox.showinfo("알림", "파일이 누락되었습니다. 다시 확인 부탁드립니다.")

    # 시작
    def start(self):
        # 각 옵션들 값을 확인
    #     print("제품코드 : ", ent1.get())
    #     print("포맷 : ", cmb_format.get())
        self.controller.btn_start.config(state=tk.DISABLED)
        # 파일 목록 확인
        if self.controller.list_file.size() == 0:
            msgbox.showwarning("경고", "텍스트 파일을 추가하세요")
            self.controller.btn_start.config(state=tk.NORMAL)
            return
        
        # 저장 경로 확인
        if len(self.controller.txt_dest_path.get()) == 0:
            msgbox.showwarning("경고", "저장 경로를 선택하세요")
            self.controller.btn_start.config(state=tk.NORMAL)
            return
        
        # 제품코드 확인
        if len(self.controller.ent1.get()) == 0 or self.controller.ent1.get()=='********':
            msgbox.showwarning("경고", "제품코드를 입력하세요")
            self.controller.btn_start.config(state=tk.NORMAL)
            return

        # 시작일자 확인
        if len(self.controller.ent_start.get()) != 8 or self.controller.ent_start.get()=="********":
            msgbox.showwarning("경고", "시작일자를 확인해주세요\nex. YYYYMMDD")
            self.controller.btn_start.config(state=tk.NORMAL)
            return
        
        # 종료일자 확인
        if len(self.controller.ent_end.get()) != 8 or self.controller.ent_end.get()=='********':
            msgbox.showwarning("경고", "종료일자를 확인해주세요\nex. YYYYMMDD")
            self.controller.btn_start.config(state=tk.NORMAL)
            return

        # limit 횟수가 0이 될 경우
        global x
        print(x)
        if limit[x] == 0:
            msgbox.showwarning("경고", "남은 횟수가 없어 진행이 불가합니다.")
            self.controller.btn_start.config(state=tk.NORMAL)
            return

        # 분석 작업 w/progress bar
        for i in range(1,41):
            time.sleep(0.02)
            self.controller.progress_bar['value'] += i
            self.controller.progress_bar.update()
            
        self.code_summary()
        self.controller.btn_start.config(state=tk.NORMAL)
        # limit 횟수 감소 후 db 저장 필요
        if tp[x] == 'user':
            sql = "UPDATE user SET cnt = '{}' where email = '{}'".format(limit[x]-1, x)
            limit[x]=limit[x]-1
            curs.execute(sql)
            result = curs.fetchall()
            conn.commit()

            print("\n정보 변경이 완료되었습니다.")

# class PageTwo(tk.Frame):

#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)
#         self.controller = controller
#         label = tk.Label(self, text="This is page 2", font=controller.title_font)
#         label.pack(side="top", fill="x", pady=10)
#         button = tk.Button(self, text="Go to the start page",
#                            command=lambda: controller.show_frame("StartPage"))
#         button.pack()


if __name__== "__main__":
    app = SampleApp()
    app.mainloop()
