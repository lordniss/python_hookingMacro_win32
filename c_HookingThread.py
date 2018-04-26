"""-----
[cTypes hooking Class]

- 문제점 : kor/en_key 값이 -127로 받아짐. 확인할 수 없음.

http://ifyourfriendishacker.tistory.com/5 : 아스키코드
-----"""
import csv
import time
import queue
import threading
import win32api
import win32con
import win32gui
from ctypes import byref, windll, WinDLL, CFUNCTYPE, c_int, POINTER, c_void_p
from ctypes.wintypes import MSG
from python_Hook_Macro_win32.VK_CODE import VK_CODE, VK_REVERSE_CODE
from python_Hook_Macro_win32.tk_TextWindow import TextThread


class HookingThread:
    __slots__ = (
        'hooked', 'hooked2', 'user32', 'kernel32',
        'hookThread', 'hookThread_name', 'starttime', 'endtime', 'stateget',
        'log_path', 'keymouselog', 'send_queue', 'action_visible',
    )  # 속도상승을 위한 slots 설정

    def __init__(self, log_path="C:/KeyMouseLog.txt", send_queue: queue.Queue = None):
        # 후킹준비하기
        self.hooked, self.hooked2 = None, None  # 키보드 후킹 핸들러 전달용, 마우스 후킹 핸들러 전달용
        self.user32 = WinDLL('user32', use_last_error=True)  # user32 = windll.user32
        self.kernel32 = windll.kernel32
        # 쓰레드 준비하기
        self.hookThread, self.hookThread_name = None, None
        # 로그파일 경로
        self.log_path = log_path
        self.keymouselog = []
        self.stateget = []
        self.starttime = 0
        # 창에 append 전달용 queue
        self.send_queue = send_queue
        self.action_visible = True

    def print1(self, *args, **kwargs):
        # print("append queue")
        # print(*args, **kwargs)
        self.send_queue.put((args, kwargs))

    def _getFPTR(self, fn):  # 포인터로 만들어줌.
        CMPFUNC = CFUNCTYPE(c_int, c_int, c_int, POINTER(c_void_p))  # CMPFUNC 가 포인터로 만들어주는 함수.
        return CMPFUNC(fn)  # 입력받은 fn을 가리키는 포인터 생성

    def _hookProc(self, nCode, wParam, lParam):  # 키보드 프로시저, 콜백함수로 후킹에 사용되는 부분
        # self.print1("[wParam:", wParam, " lParam[0]:", lParam[0], ",", type(lParam[0]), " : ", nCode, "]")
        # keyup 이벤트 처리
        hooked_key, key_info = "", ""
        if wParam == win32con.WM_KEYUP:  # 257 key_up
            hooked_key = VK_REVERSE_CODE[lParam[0]]
            key_info = "keyup"
        # keydown, syskeydown 이벤트 처리
        elif wParam == win32con.WM_KEYDOWN or wParam == win32con.WM_SYSKEYDOWN:  # 256 key_up # 260 syskey_down
            if VK_CODE['esc'] == int(lParam[0]):  # esc는 기록하지 않는다.
                return self.user32.CallNextHookEx(None, nCode, wParam, lParam)
            hooked_key = VK_REVERSE_CODE[lParam[0]]
            key_info = "keydown"
        # keylog 기록
        dd = ['keyboard', hooked_key, key_info, str(time.time()-self.starttime)]
        self.keymouselog.append(dd)
        if self.action_visible:
            self.print1(self.keymouselog[-1])  # 창에 가장 최신의 keymouselog 입력정보 출력
        return self.user32.CallNextHookEx(self.hooked, nCode, wParam, lParam)

    def _hookProc2(self, nCode, wParam, lParam):  # 마우스 프로시져
        # self.print1("nCode:", nCode, " wParam:", wParam, "lParam[0]:", lParam[0])
        # MouseButtonDown 처리 및 mouselog 기록
        if wParam == win32con.WM_LBUTTONDOWN or \
                wParam == win32con.WM_RBUTTONDOWN:  # win32con을 따르지 않는다. 작동안함 -> 아님, is와 ==의 차이.
            dd = ['mouse',
                  "LBUTTONDOWN" if wParam == win32con.WM_LBUTTONDOWN else "RBUTTONDOWN",
                  str(lParam[0]) + "|" + str(lParam[1]),
                  str(time.time()-self.starttime)]  # lParam[0], lParam[1] 은 각각 x좌표, y좌표이다. 그 이상은 없음.
            self.keymouselog.append(dd)
            if self.action_visible:
                self.print1(self.keymouselog[-1])  # 창에 가장 최신의 keymouselog 입력정보 출력
        # MouseButtonUp 처리 및 mouselog 기록
        elif wParam == win32con.WM_LBUTTONUP or \
                wParam == win32con.WM_RBUTTONUP:
            dd = ['mouse',
                  "LBUTTONUP" if wParam == win32con.WM_LBUTTONUP else "RBUTTONUP",
                  str(lParam[0]) + "|" + str(lParam[1]),
                  str(time.time()-self.starttime)]  # lParam[0], lParam[1] 은 각각 x좌표, y좌표이다. 그 이상은 없음.
            self.keymouselog.append(dd)
            if self.action_visible:
                self.print1(self.keymouselog[-1])  # 창에 가장 최신의 keymouselog 입력정보 출력
        return self.user32.CallNextHookEx(self.hooked2, nCode, wParam, lParam)

    def _msg_loop(self, keyboard=True, mouse=True):  # 쓰레드 대상
        if keyboard == True:
            pointer1 = self._getFPTR(self._hookProc)
            self.hooked = self.user32.SetWindowsHookExA(  # 키보드 후커
                win32con.WH_KEYBOARD_LL,  # 후킹 타입. 13 0xD
                pointer1,  # 후킹 프로시저
                self.kernel32.GetModuleHandleA(None),  # 앞서 지정한 후킹 프로시저가 있는 핸들
                0  # thread id. 0일 경우 글로벌로 전체를 후킹한다.
            )  # hook 인스톨
        if mouse == True:
            pointer2 = self._getFPTR(self._hookProc2)
            self.hooked2 = self.user32.SetWindowsHookExA(  # 키보드 후커
                win32con.WH_MOUSE_LL,  # 후킹 타입. 13 0xD
                pointer2,  # 후킹 프로시저
                self.kernel32.GetModuleHandleA(None),  # 앞서 지정한 후킹 프로시저가 있는 핸들
                0  # thread id. 0일 경우 글로벌로 전체를 후킹한다.
            )  # hook2
        if keyboard == False and mouse == False:
            self.print1("no hooker installed")
            return
        self.print1("hooker installed")
        msg = MSG()
        while True:
            bRet = self.user32.GetMessageW(byref(msg), None, 0, 0)  # 메시지 받기 시작. byref가 있어야 에러 발생 안함.
            if bRet == 1:
                break
            if bRet == -1:
                # print(bRet, " raise WinError(get_last_error())")
                # raise WinError(get_last_error())
                break
            self.user32.TranslateMessage(byref(msg))
            self.user32.DispatchMessageW(byref(msg))

    def saveKeyMouseLog(self):
        with open(self.log_path, 'w', encoding='UTF-8', newline='') as f:
            keys = ('type', 'input', 'info', 'time')
            cwrite = csv.DictWriter(f, fieldnames=keys)  # DictWriter 사용
            # print(stateget)  # 마지막 네번째 kor/en_key 값이 이상함.
            cwrite.writeheader()
            cwrite.writerow({'type': 'start', 'input': 'state_keys',  # start log 시작
                             'info': ''.join(self.stateget), 'time': str(self.starttime-self.starttime)})
            for log in self.keymouselog:
                kk = list(keys)
                tmpdic = {kk.pop(0): x for x in log}
                cwrite.writerow(tmpdic)
            cwrite.writerow({'type': 'end', 'input': '',  # end log 끝
                             'info': '', 'time': str(self.endtime-self.starttime)})
            self.keymouselog = []  # log 초기화
            f.close()  # Logging 기록

    def start_hookThread(self, log_path=None, keyboard=True, mouse=True):  # 훅쓰레드 실행.
        state_keys = ['caps_lock', 'num_lock', 'scroll_lock', 'kor/en_key']  # state_key 설정, 시작설정
        self.stateget = [str(win32api.GetKeyState(VK_CODE[key])) for key in state_keys]  # 키값 받아 0/1로 저장
        self.starttime = time.time()
        if log_path is not None:
            self.log_path = log_path
        if self.hookThread_name is None:  # 생성했으면 참, 이미 있으면 거짓
            self.hookThread = threading.Thread(target=self._msg_loop, args=(keyboard, mouse),
                                               daemon=True, name="HookingKeyboardMouseThread")  # 키보드/마우스 동시후킹
            self.hookThread.start()  # 쓰레드 시작
            self.hookThread_name = self.hookThread.ident  # 쓰레드 살아있는지 여부 저장 / is_alive는 느릴 수 있음
            return True
        return False

    def _uninstallHooker(self):
        self.endtime = time.time()
        if self.hooked is not None:
            self.user32.UnhookWindowsHookEx(self.hooked)
        if self.hooked2 is not None:  # 이걸 체크하지 않아서 속도가 느려졌던것. 당연히 체크했어야 했다.
            self.user32.UnhookWindowsHookEx(self.hooked2)
        self.hooked, self.hooked2 = None, None
        if self.ishookThread():
            win32gui.PostThreadMessage(self.hookThread.ident, win32con.WM_CLOSE, 0, 0)  # WM_QUIT 말고 WM_CLOSE로.
        self.print1("hooker uninstalled")
        self.hookThread_name = None  # 쓰레드 죽은걸로 갱신 / is_alive보다 빠르게 정보 접근

    def stop_hookThread(self):  # 클래스내의 메인쓰레드 파괴
        if self.ishookThread():
            self._uninstallHooker()  # 언인스톨 -> WM_CLOSE 메시지 전달 -> GetMessage에서 멈춘 thread 진행 및 종료
            self.saveKeyMouseLog()  # log에 저장 / log는 다 날라가버림
            # self.print1("hooker stopped")
            return True
        return False

    def ishookThread(self):  # 쓰레드 살아있으면 True/False, 쓰레드 생성 자체가 안됐으면 None
        if self.hookThread_name is not None:
            return True
        return False

    def get_log_path(self):  # 키보드, 마우스 입력 로그 저장 경로 반환
        return self.log_path

    def set_log_path(self, set_log_path):  # 키보드, 마우스 입력 로그 저장 경로 설정 / replay에서 읽는 로그경로도 같이 변경
        self.log_path = set_log_path

    def get_stop_hookThread(self):
        return self.stop_hookThread


if __name__ == '__main__':
    log_path = "C:/KeyMouseLog.txt"
    txwindow = TextThread()  # 창 쓰레드 준비
    txwindow.start_window()  # 창 쓰레드 시작. start가 아니라 start_window로 실행할 것.
    send_queue = queue.Queue()
    hooker = HookingThread(log_path=log_path, send_queue=send_queue)  # 창 쓰레드 시작 및 후커 쓰레드 준비
    hooker.start_hookThread()  # 후커 쓰레드 시작

    txwindow.set_button_action(btn2=hooker.start_hookThread)  # 버튼1 실행
    txwindow.set_button_action(btn3=hooker.stop_hookThread)  # 버튼2 실행
    txwindow.set_button_action(btn1=lambda: print("hooker.stop_hookThread"))  # 버튼2 실행


    def append_manager(*args, **kwargs):
        while True:
            # if not send_queue.empty: 을 하게 되면 오히려 queue의 block이 해제되어 버리므로, if문은 넣지 말아야 한다.
            try:
                args, kwargs = send_queue.get(timeout=5)  # queue가 empty이면 get 되지 않으며, 대기하게 된다.
                txwindow.append(*args, **kwargs)
            except queue.Empty as e:
                print(e.args)


    append_thread = threading.Thread(target=append_manager, daemon=True, name='AppendThread')
    append_thread.start()

    while True:
        time.sleep(1)
        print(threading.enumerate(), time.ctime())
        time.sleep(1)
        print(threading.enumerate(), time.ctime())
        if not txwindow.is_alive():  # 윈도우와 후커가 독립되어 있으므로, 따로 종료해준다
            print("stop hookTread by destoried txwindow")
            hooker.stop_hookThread()
            break
    ###