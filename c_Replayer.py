"""
[ReplayThread : 읽기 및 키보드/마우스 재생]

- 요구패키지
pypiwin32

- 보완할점
1. 특정 상황에서 kor/en_eky 반환값이 -127로 바뀐다.
"""
import csv
import queue
import time
import win32api
import win32con
import threading
from python_Hook_Macro_win32.c_HookingThread import HookingThread
from python_Hook_Macro_win32.tk_TextWindow import TextThread
from python_Hook_Macro_win32.VK_CODE import VK_CODE


class ReplayThread:
    def __init__(self, log_path="c:\\KeyMouseLog.txt"):
        # for replayer
        self.log_path = log_path
        self.run_th = None
        self.stopper = False
        # for append
        self.send_queue = queue.Queue()

    def get_sendQueue(self):
        return self.send_queue

    def print1(self, *args, **kwargs):  # window 종료시 대비한 에러방지
        self.send_queue.put((args, kwargs))
        print(*args, **kwargs)

    def _get_cmdlist(self):  # log파일에서 cmd 불러와서 list(OrderDict (any, any)) 로 읽어들인다.
        with open(self.log_path, 'r', encoding='utf-8') as f:
            cmdlist = [w for w in csv.DictReader(f, delimiter=',')]
            f.close()
        return cmdlist

    def replay_runner(self, pace_time=0.01):  # 진짜로 replay 를 하는 부분 / pace_time은 동작과 동작 사이에 최소시간.
        self.print1("start replay..")
        # 파일에서 커맨드를 읽어서 실행한다
        cmdlist = self._get_cmdlist()  # 파일 전체의 OrderedDict 값을 받아온다. type 등의 키값은 자동으로 제외.
        print(cmdlist)
        # 초기값인 Start 처리 / state key 들을 확인해서 입력한다
        cmd = cmdlist.pop(0)  # start 뽑아낸다
        start_pace = float(cmd['time'])
        start_time = time.time()
        """ 시작키 설정이 os 종류에 따라 제대로 받아지지가 않는다. 사실 필요없기도 함.
        state_keys = ['caps_lock', 'num_lock', 'scroll_lock', 'kor/en_key']  # state_key 설정
        if cmd['type'] == 'state_keys':
            for i in range(len(state_keys)):
                if cmd['info'][i] == '1':
                    win32api.keybd_event(VK_CODE[state_keys[i]], 0, 0, 0)
                win32api.keybd_event(VK_CODE[state_keys[i]], 0, win32con.KEYEVENTF_KEYUP, 0)
        """
        # Start 이후 본 내용 처리
        while True:
            if (time.time() - start_time) > (float(cmd['time']) - start_pace):
                if cmd['type'] == 'end':  # 마지막인지 체크.
                    print("sttoper1")
                    break
                # 키보드 입력 처리
                if cmd['type'] == 'keyboard':
                    if cmd['info'] == "keydown":  # while문 자체에서 시간지연 있으므로, time.sleep() 안넣어도 됨.
                        win32api.keybd_event(VK_CODE[cmd['input']], 0, 0, 0)
                    elif cmd['info'] == "keyup":
                        win32api.keybd_event(VK_CODE[cmd['input']], 0, win32con.KEYEVENTF_KEYUP, 0)
                # 마우스 입력 처리
                elif cmd['type'] == 'mouse':
                    win32api.SetCursorPos([int(pos) for pos in cmd['info'].split('|')])  # 언패킹한 위치로 마우스 이동
                    if cmd['input'] == "LBUTTONUP":
                        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0)
                    elif cmd['input'] == "LBUTTONDOWN":
                        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0)
                    elif cmd['input'] == "RBUTTONUP":
                        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0)
                    elif cmd['input'] == "RBUTTONDOWN":
                        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0)  # 마우스 입력
                # 입력하고 cmd 확인해서 앞에서부터 pop으로 꺼내기
                if len(cmdlist) == 0:
                    print("sttoper2")
                    break  # cmdlist 를 다 실행했을 경우, 종료.
                cmd = cmdlist.pop(0)
            else:
                if self.stopper:  # 중간에 멈추는거 체크. 작동시간 우려로 input 다음에 배치.
                    print("sttoper3")
                    self.stopper = False
                    break  # replay thread 종료
                time.sleep(pace_time)  # pace_time 의 간격 사이에 명령이 다 이루어져야, 다음 pace_time을 지난다.
        print("sttope4")
        self.print1("replay ended")
        return

    def start_replay(self, log_path="c:\\KeyMouseLog.txt"):  # thread setting
        self.log_path = log_path
        self.stopper = False
        if self.run_th is None or not self.run_th.is_alive():  # runner thread 가 없거나 실행되지 않았을 경우
            self.run_th = threading.Thread(target=self.replay_runner,
                                           args=(), name="RunnerThread")  # 기록한 키&마우스 로그 실행.
            self.run_th.start()

    def is_replay(self):
        if self.run_th is None:
            return False
        return self.run_th.is_alive()

    def stop_replay(self):
        self.stopper = True

    ################################

    def macro(self):
        self.print1("macro pushed")


if __name__ == '__main__':
    log_path = "C:/KeyMouseLog.txt"
    txwindow = TextThread()  # 창 쓰레드 준비
    txwindow.start_window()
    txwindow.update_window_attribute(btn2="Start", btn3="Stop")
    hooker = HookingThread(log_path=log_path)  # 창 쓰레드 시작 및 후커 쓰레드 준비
    replayer = ReplayThread()  # 리플레이 동작 준비


    def start_replay_thread():
        if replayer.is_replay():
            pass
        if hooker.ishookThread():
            txwindow.append("hooker is alive")
        else:
            replayer.start_replay()
            txwindow.update_window_attribute('iconify')


    def start_hook_thread():
        if hooker.ishookThread():
            pass
        elif replayer.is_replay():
            txwindow.append("replayer is alive")
        else:
            hooker.start_hookThread()


    def stop_tread():
        txwindow.append("stop threads")
        hooker.stop_hookThread()
        replayer.stop_replay()


    def append_thread():  # queue checking error -> need change
        while True:
            get_q1 = hooker.get_sendQueue()
            get_q2 = replayer.get_sendQueue()
            if not get_q1.empty():
                args, kwags = get_q1.get()
                txwindow.append(*args, **kwags)
            if not get_q2.empty():
                args, kwags = get_q2.get()
                txwindow.append(*args, **kwags)


    txwindow.set_button_action(
        btn1=lambda: start_replay_thread(),
        btn2=lambda: start_hook_thread(),
        btn3=lambda: stop_tread(),
    )
    threading.Thread(target=lambda: append_thread(), name="append thread").start()

    while True:
        time.sleep(1)
        print(threading.enumerate())
        if not txwindow.is_alive():  # 윈도우 종료시 후킹도 종료되게. 현재 윈도우와 후킹 클래스를 독립해서 만들었으므로.
            hooker.stop_hookThread()
            replayer.stop_replay()
            print("window end , hooker killed")
            import os
            os._exit(1)
            break

    print("__main__ end")
