"""
[python win32 module / hooking and replaying]

- 동작
 open -> 파일열기
 replay -> log 파일로 재생
 hook -> hook 시작
 stop -> replay 및 hook 중지
 end -> 프로그램 종료
"""
import win32gui
import win32con
from ctypes import byref, windll, WinDLL, CFUNCTYPE, c_int, POINTER, c_void_p
from ctypes.wintypes import MSG
from python_Hook_Macro_win32.tk_TextWindow import TextThread
from python_Hook_Macro_win32.c_HookingThread import HookingThread
from python_Hook_Macro_win32.c_Replayer import ReplayThread
from python_Hook_Macro_win32.VK_CODE import VK_CODE
import time
import threading
import queue


class HookingMacroWin32:
    def __init__(self, log_path="c:\\keymouselog.txt"):
        #####
        # initialize classes
        self.log_path = log_path
        self.text_thread = TextThread()
        self.hooking_thread = HookingThread(log_path=log_path)
        self.replay_thread = ReplayThread(log_path=log_path)
        #####
        # set append thread
        self.ender = False
        self.append_hook_thread = threading.Thread(
            target=self.append_manager_hook, daemon=False, name='AppendHookThread')
        self.append_replay_thread = threading.Thread(
            target=self.append_manager_replay, daemon=False, name='AppendReplayThread')
        # set keyinput thread
        self.user32 = WinDLL('user32', use_last_error=True)  # user32 = windll.user32
        self.kernel32 = windll.kernel32
        self.keychk_thread = threading.Thread(target=self._keychk_runner, daemon=False, name="KeychkThread")
        #####
        # class flag setting
        self._ismain = False

    def start_main(self):
        if not self.text_thread.is_alive():  # text_window 실행 및 설정
            # 창 실행
            self.text_thread.start_window()  # start로 하면 _txwin에 대한 접근오류 날 수 있다. start_window로 실행할 것.
            # 창 설정
            self.text_thread.update_window_attribute(title="Keyboard and Mouse Hooker - python 3.6")  # 창 title
            self.text_thread.update_window_attribute(btn2="Hook")  # button2 setting
            # 버튼 실행
            self.text_thread.set_button_action(btn0=lambda: self._push_open_button())  # 버튼0 실행
            self.text_thread.set_button_action(btn1=lambda: self._start_replay_thread())  # 버튼1 실행
            self.text_thread.set_button_action(btn2=lambda: self._start_hooking_thread())  # 버튼2 실행
            self.text_thread.set_button_action(btn3=lambda: self._stop_sub())  # 버튼3 실행
            self.text_thread.set_button_action(btn4=lambda: self.stop_main())  # 버튼4 실행
            self.text_thread.set_button_action(xbtn=lambda: self.stop_main())  # x 버튼 실행 설정
        if not self.append_hook_thread.is_alive():  # text_window에 값을 전달하는 append thread
            self.append_hook_thread.start()
        if not self.append_replay_thread.is_alive():  # text_window에 값을 전달하는 append thread
            self.append_replay_thread.start()
        if not self.keychk_thread.is_alive():  # 입력된 키값을 모니터링하는 key_thread 시작
            self.keychk_thread.start()
        self._ismain = True
        # 시작 메시지
        self.text_thread.append(
            "--------------------------------------------------------------------\n",
            " Hello! This is hooking and Replaying Program.\n",
            " - If you want to hook, press HOOK button or 'F2'\n",
            " - If you want to replay hooked action, press REPLAY button or 'F3'\n",
            " - When you wanna stop your action, press STOP button or 'ESC'\n",
            " - If you need to disable viewing hooked command, press 'F4'\n"
            "--------------------------------------------------------------------\n",
        )
        self.text_thread.append("default log_path : ", self.log_path)

    def stop_main(self):
        self.text_thread.destroy()  # 창 정지
        self.hooking_thread.stop_hookThread()  # 후커 정지
        self.replay_thread.stop_replay()  # 리플레이 정지
        self.ender = True  # append 정지
        self._uninstall_keychk()  # keychk uninstall 및 정지
        self._ismain = False  # main 종료 표시
        import os
        os._exit(1)  # append thread를 정상적으로 종료할 수 없어서 사용하는 임시방편

    def is_main(self):
        return self._ismain

    def _stop_sub(self):
        if self.hooking_thread.ishookThread():
            self.hooking_thread.stop_hookThread()
        if self.replay_thread.is_replay():
            self.replay_thread.stop_replay()
        return

    def _start_hooking_thread(self):
        if self.hooking_thread.ishookThread():
            return
        elif self.replay_thread.is_replay():
            self.text_thread.append("Relplayer is alive")
        else:
            self.hooking_thread.start_hookThread(log_path=log_path)

    def _start_replay_thread(self):
        if self.replay_thread.is_replay():
            return
        elif self.hooking_thread.ishookThread():
            self.text_thread.append("Hook is alive")
        else:
            self.replay_thread.start_replay(log_path=log_path)

    def _push_open_button(self):
        filename: str = self.text_thread.open_file()
        filename = filename.replace("/", u"\\")
        self.log_path = filename
        self.text_thread.append("set new log_path : ", self.log_path)
    ###############################

    def append_manager_hook(self):
        send_queue = self.hooking_thread.get_sendQueue()
        while True:
            try:
                get_queue = send_queue.get(block=True, timeout=5)
                args, kwargs = get_queue
                if self.text_thread.is_alive():
                    self.text_thread.append(*args, *kwargs)
            except queue.Empty as e:
                print(e.args)

    def append_manager_replay(self):
        send_queue = self.replay_thread.get_sendQueue()
        while True:
            try:
                get_queue = send_queue.get(block=True, timeout=5)
                args, kwargs = get_queue
                if self.text_thread.is_alive():
                    self.text_thread.append(*args, *kwargs)
            except queue.Empty as e:
                print(e.args)
    ###############################

    def _keychk_proc(self, nCode, wParam, lParam):  # replay중 runner를 종료시키기 위한 프로시져
        if wParam is not win32con.WM_KEYDOWN:  # keydown 만 처리
            return self.user32.CallNextHookEx(self.hooked, nCode, wParam, lParam)
        if VK_CODE['esc'] == int(lParam[0]):
            self.text_thread.append("ESC inputed")
            self._stop_sub()
        elif VK_CODE['F2'] == int(lParam[0]):
            self.text_thread.append("F2 inputed")
            self._start_hooking_thread()
        elif VK_CODE['F3'] == int(lParam[0]):
            self.text_thread.append("F3 inputed")
            self._start_replay_thread()
        elif VK_CODE['F4'] == int(lParam[0]):
            self.text_thread.append("F4 inputed")
            if self.hooking_thread.action_visible:
                self.hooking_thread.action_visible = False
                self.text_thread.append("hooked command view is disabled")
            else:
                self.hooking_thread.action_visible = True
                self.text_thread.append("hooked command view is abled")
        #####
        return self.user32.CallNextHookEx(None, nCode, wParam, lParam)

    def _keychk_runner(self):
        cmp_func = CFUNCTYPE(c_int, c_int, c_int, POINTER(c_void_p))
        pointer = cmp_func(self._keychk_proc)
        self.hooked = self.user32.SetWindowsHookExA(  # 키보드 후커
            win32con.WH_KEYBOARD_LL,  # 후킹 타입. 13 0xD
            pointer,  # 후킹 프로시저
            self.kernel32.GetModuleHandleA(None),  # 앞서 지정한 후킹 프로시저가 있는 핸들
            0  # thread id. 0일 경우 글로벌로 전체를 후킹한다.
        )  # hook 인스톨
        msg = MSG()
        b = self.user32.GetMessageW(byref(msg), None, 0, 0)  # 메시지 받기 시작. byref가 있어야 에러 발생 안함.

    def _uninstall_keychk(self):
        if self.hooked is not None:
            self.user32.UnhookWindowsHookEx(self.hooked)
            self.hooked = None
        if self.keychk_thread.is_alive():
            win32gui.PostThreadMessage(self.keychk_thread.ident, win32con.WM_CLOSE, 0, 0)  # WM_QUIT 말고 WM_CLOSE로.


if __name__ == '__main__':
    log_path = "c:\\KeyMouseLog.txt"
    main_class = HookingMacroWin32(log_path=log_path)
    main_class.start_main()

    while True:
        time.sleep(1)
        print(threading.enumerate())
        if not main_class.is_main():
            break

    print("main end")
