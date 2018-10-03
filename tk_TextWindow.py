"""
[TextThread Class]

- 동작
 TextWindow를 TextThread로 생성해서 start_window로 시작하고, append(string, end="", trace=True)로 내용추가한다.
"""
import tkinter.filedialog
from tk_ROText import ROText
import tkinter
from tkinter import *
import threading
import time


class TextWindow:
    __slots__ = ('master', 'frame1', 'Txt', 'btn', 'ysbar', 'xsbar',
                 'btn0', 'btn1', 'btn2', 'btn3', 'btn4',
                 )  # 속도상승을 위한 slots 설정

    def __init__(self, master: tkinter.Tk):
        # 기본 윈도우 요소 생성 및 구성
        width = 13
        self.master = master  # tkinter.Tk() #master
        # self.master.attributes("-toolwindow", 1)  # 최소화/최대화 버튼 삭제
        self.master.title("eigen window (by tkinter)")  # 윈도우 title
        self.master.geometry("510x350+10+10")  # "width x height + x_offset + y_offset"
        self.master.minsize(510, 78)  # 최소크기
        # 메뉴 구성 및 배치
        menubar = tkinter.Menu(master)
        file_menu = tkinter.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Exit", command=master.destroy)
        menubar.add_cascade(label="File", menu=file_menu)
        """ 나중에 메뉴추가용
        setting_menu = tkinter.Menu(menubar, tearoff=0)
        setting_menu.add_command(label="etc", command=lambda :print("etc"))
        menubar.add_cascade(label="Setting", menu=setting_menu)"""
        self.master.config(menu=menubar)
        # self.master.resizable(0, 0)  # 창의 x와 y 의 크기 조절 불가능
        self.frame1 = Frame(self.master, bd=2, relief=SUNKEN)
        self.Txt = ROText(self.frame1)  # ROText시 disable window / Text시 able window
        self.btn4 = Button(self.frame1, text="End Window", command=self.quit, width=width)
        self.ysbar = Scrollbar(self.frame1, orient=VERTICAL, command=self.Txt.yview)
        self.xsbar = Scrollbar(self.frame1, orient=HORIZONTAL, command=self.Txt.xview)
        self.Txt.config(yscrollcommand=self.ysbar.set, xscrollcommand=self.xsbar.set,
                        wrap=NONE,  # wrap 이 가로로 창을 넘어서 표시할지 안할지 정하는 값
                        )
        # 텍스트 배치 전 크기조정 설정  # master의 frame1과, frame1의 txt 확장  # non-zero weight여야 함
        Grid.columnconfigure(self.master, 0, weight=1)  # (0,0)의 frame1 grid를 늘리기 위해 설정
        Grid.rowconfigure(self.master, 0, weight=1)
        Grid.columnconfigure(self.frame1, 0, weight=1)
        Grid.rowconfigure(self.frame1, 0, weight=1)  # (0,0)의 txt grid를 늘리기 위해 설정
        # 윈도우 요소 배치 5*6  # sticky를 양쪽 다로 잡으면 확장과 동일.
        self.Txt.grid(column=0, row=0,
                      columnspan=5, rowspan=5, sticky=N + S + W + E)  # (0,0)에서부터 5x5을 배치
        self.ysbar.grid(column=5, row=0,
                        columnspan=1, rowspan=5, sticky=N + S)  # (5,0)에서부터 1x5으로 배치
        self.xsbar.grid(column=0, row=5,
                        columnspan=5, rowspan=1, sticky=W + E)  # (0,5)에서부터 5x1을 배치
        self.btn4.grid(column=4, row=6,
                       columnspan=2, rowspan=1, sticky=E)  # (4,6)에서부터 2x1을 배치
        ###################
        # 여유공간 테스트  # (0~3, 6) 사용가능
        # self.label = Label(self.frame1, text="hello")
        # self.label.grid(column=0, row=6, columnspan=1, rowspan=1, sticky=W)
        self.btn0 = Button(self.frame1, text="Open", command=None, width=width)
        self.btn0.grid(column=0, row=6, columnspan=1, rowspan=1, sticky=E)
        self.btn1 = Button(self.frame1, text="Replay", command=None, width=width)
        self.btn1.grid(column=1, row=6, columnspan=1, rowspan=1, sticky=E)
        self.btn2 = Button(self.frame1, text="Start", command=None, width=width)
        self.btn2.grid(column=2, row=6, columnspan=1, rowspan=1, sticky=E)
        self.btn3 = Button(self.frame1, text="Stop", command=None, width=width)
        self.btn3.grid(column=3, row=6, columnspan=1, rowspan=1, sticky=E)
        ###################
        # 프레임을 마스터에 붙이기 등등
        self.frame1.grid(row=0, column=0, sticky=W + E + N + S)  # frame1을 root에 붙이기
        self.master.protocol('WM_DELETE_WINDOW', self.quit)  # x 종료 버튼 작동 바꾸기 detroy->quit
        # button 콜백 및 update attribute 용 변수

    def open_file(self):
        filename = tkinter.filedialog.askopenfilename(
            initialdir="\\", title="Select file",
            filetypes=(("text files", "*.txt"), ("all files", "*.*")))
        return filename

    def button_excute(self, **kwargs):
        for key, item in kwargs.items():
            if key == 'btn0':
                self.btn0.configure(command=item)
            elif key == 'btn1':
                self.btn1.configure(command=item)
            elif key == 'btn2':
                self.btn2.configure(command=item)
            elif key == 'btn3':
                self.btn3.configure(command=item)
            elif key == 'btn4':
                self.btn4.configure(command=item)
            elif key == 'xbtn':
                self.master.protocol("WM_DELETE_WINDOW", item)

    def update_attribute(self, *args, **kwargs):
        for arg in args:
            if arg == 'iconic':
                self.state(arg)
            elif arg == 'normal':
                self.state(arg)
            elif arg == 'lift':
                self.master.lift()
        for key, item in kwargs.items():
            if key == 'btn1':
                self.btn1.configure(text=item)
            elif key == 'btn2':
                self.btn2.configure(text=item)
            elif key == 'btn3':
                self.btn3.configure(text=item)
            elif key == 'title':
                self.master.title(item)
            self.master.update()

    def show(self):
        self.master.update()  # 새로 만들어지는 창 최상단에 위치하도록.
        self.master.mainloop()  # mainloop를 하면 기본 최상단으로 나오나, update()로 누락되는 경우까지 체크.

    def append(self, *args, **kwargs):  # Txt 창에 마지막부분 END 로 메시지 붙여넣기
        string, trace, end = "", True, "\n"  # 따라가기. 기본은 따라가는걸로.
        for arg in args:
            string += str(arg)
        for key, value in kwargs.items():
            end = value if key == 'end' else end
            trace = False if key == 'trace' and not value else trace  # trace가 있으면.
        else:
            string += end
        self.Txt.insert(END, string)  # insert 커서, current 마우스, end 맨끝
        if trace:
            self.Txt.see("end")  # 화면을 맨 아래로 보여주는 명령어.

    def state(self, string=""):
        self.master.state(string)  # master.wm_state('iconic'), master.iconify(), master.state('normal')

    def quit(self):
        self.master.quit()
        return True


class TextThread(threading.Thread):
    __slots__ = ("_iswindow", '_txwin',
                 'daemon',)  # 클래스내 멤버 제한 / 속도상승을 위한 slots 설정

    def __init__(self, daemon=False):  # 기본값은 독립실행(daemon=False)
        self._iswindow = False
        self._txwin: TextWindow = None
        self.daemon = daemon
        threading.Thread.__init__(self, name="TextThread", daemon=self.daemon)

    def open_file(self):
        filename = self._txwin.open_file()
        # print(filename)
        return filename

    def _inner(self):  # thread의 target으로 지정할 수 있게, mainloop를 잡아서 받을 수 있는 하나의 함수로 만듬
        self._txwin: TextWindow = TextWindow(tkinter.Tk())  # 쓰레드 내부에서 생성된 함수를 클래스 멤버로 보냄
        self._iswindow = True
        self._txwin.show()
        self._iswindow = False

    def run(self):
        self._inner()

    def start_window(self):  # 그냥 start로 thread를 실행하면, _txwin이 실행되기 전에 접근할려는 접근오류가 날 수 있다.
        self.start()

        while self._txwin is None:  # _txwin : TextWindow 가 생성될 때까지 기다렸다가 return 한다.
            pass
        return

    def append(self, *args, **kwargs):  # 윈도우의 텍스트창에 텍스트 추가
        if self._iswindow:
            self._txwin.append(*args, **kwargs)
            return True
        return False

    def isthread_alive(self):  # 윈도우 살아있는지 확인
        if self._txwin is not None:
            return self.is_alive()
        return False

    def destroy(self):  # 윈도우 파괴
        if self.isthread_alive():
            self._txwin.quit()

    def set_button_action(self, **kwargs):
        if self._txwin is not None:
            self._txwin.button_excute(**kwargs)
            return True
        return False

    def update_window_attribute(self, *args, **kwargs):  # 실행한 창의 stete 와 버튼의 text 를 갱신.
        if self._txwin is not None:
            self._txwin.update_attribute(*args, **kwargs)
            return True
        return False


if __name__ == '__main__':
    tth = TextThread()
    tth.daemon = True

    tth.start()
    while True:
        if tth.append(end=""):
            [tth.append("hello world!" * 10, end="|\n") for x in range(100)]
            break
    import os

    tth.set_button_action(btn1=lambda: print("yes"))
    tth.set_button_action(btn3=lambda: os._exit(-1))  # 강제종료
    while True:
        print(threading.enumerate())
        # tth.update_window_attribute("iconic")
        time.sleep(1)
        # tth.update_window_attribute("normal")
        time.sleep(1)
        if tth.isthread_alive():
            tth.update_window_attribute(btn1="Replay_hello")
            tth.set_button_action(btn1=lambda: print("no"))
            print("use")
        if not tth.isthread_alive():
            print(threading.enumerate())
            tth.destroy()
            break
            # tth.start()  # 무한실행
            # tth.set_button_action(btn1=lambda: tth.append("hello"))
            # tth.set_button_action(btn3=lambda: os._exit(-1))  # 강제종료
        pass
