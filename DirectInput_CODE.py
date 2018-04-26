DI_REVERSE_CODE = {
    0X1: 'esc', 0X2: '1', 0X3: '2', 0X4: '3', 0X5: '4', 0X6: '5', 0X7: '6', 0X8: '7', 0X9: '8', 0XA: '9', 0XB: '0',
    0XC: '-', 0XD: '=', 0XE: 'backspace', 0XF: 'tab', 0X10: 'q', 0X11: 'w', 0X12: 'e', 0X13: 'r', 0X14: 't', 0X15: 'y',
    0X16: 'u', 0X17: 'i', 0X18: 'o', 0X19: 'p', 0X1A: '[', 0X1B: ']', 0X1C: 'enter', 0X1D: 'left_control', 0X1E: 'a',
    0X1F: 's', 0X20: 'd', 0X21: 'f', 0X22: 'g', 0X23: 'h', 0X24: 'j', 0X25: 'k', 0X26: 'l', 0X27: ';', 0X28: "'",
    0X29: '`', 0X2A: 'left_shift', 0X2B: '\\', 0X2C: 'z', 0X2D: 'x', 0X2E: 'c', 0X2F: 'v', 0X30: 'b', 0X31: 'n',
    0X32: 'm', 0X33: ', ', 0X34: '.', 0X35: ' / ', 0X36: 'right_shift', 0X37: ' * (Numpad)', 0X38: 'left_alt',
    0X39: 'spacebar', 0X3A: 'caps_lock', 0X3B: 'F1', 0X3C: 'F2', 0X3D: 'F3', 0X3E: 'F4', 0X3F: 'F5', 0X40: 'F6',
    0X41: 'F7', 0X42: 'F8', 0X43: 'F9', 0X44: 'F10', 0X45: 'num_lock', 0X46: 'scroll_lock', 0X47: '7(Numpad)',
    0X48: '8(Numpad)', 0X49: '9(Numpad)', 0X4A: ' - (Numpad)', 0X4B: '4(Numpad)', 0X4C: '5(Numpad)', 0X4D: '6(Numpad)',
    0X4E: ' + (Numpad)', 0X4F: '1(Numpad)', 0X50: '2(Numpad)', 0X51: '3(Numpad)', 0X52: '0(Numpad)', 0X53: '.(Numpad)',
    0X57: 'F11', 0X58: 'F12', 0X64: 'F13', 0X65: 'F14', 0X66: 'F15', 0X9C: 'Enter(Numpad)', 0X9D: 'right_control',
    0XB5: ' / (Numpad)', 0XB7: 'sys Rq', 0XB8: 'right_alt', 0XC5: 'pause', 0XC7: 'home', 0XC8: 'up_arrow',
    0XC9: 'page_up', 0XCB: 'left_arrow', 0XCD: 'right_arrow', 0XCF: 'end', 0XD0: 'down_arrow', 0XD1: 'page_down',
    0XD2: 'insert', 0XD3: 'delete', 0XDB: 'left_window_key', 0XDC: 'right_window_key', 0XDD: 'menu_key',
    0XDE: 'power_key', 0XDF: 'windows',
}
"""
0x70	:DIK_KANA	Kana	Japenese Keyboard
0x79	:DIK_CONVERT Convert	Japenese Keyboard
0x7B	:DIK_NOCONVERT No Convert	Japenese Keyboard
0x7D	:DIK_YEN		Japenese Keyboard
0x8D	:DIK_NUMPADEQUALS	NEC PC-98
0x90	:DIK_CIRCUMFLEX	^	Japenese Keyboard
0x91	:DIK_AT	@	NEC PC-98
0x92	:DIK_COLON	:	NEC PC-98
0x93	:DIK_UNDERLINE	_	NEC PC-98
0x94	:DIK_KANJI	Kanji	Japenese Keyboard
0x95	:DIK_STOP	Stop	NEC PC-98
0x96	:DIK_AX	(Japan AX)	
0x97	:DIK_UNLABELED	(J3100)
0xB3	:DIK_NUMPADCOMMA	, (Numpad)	NEC PC-98
"""
#for key, value in DI_REVERSE_CODE.items():
#    print("'{0}' :{1:#X},".format(value, key), end=" ")

DI_CODE = {
    'esc': 0X1, '1': 0X2, '2': 0X3, '3': 0X4, '4': 0X5, '5': 0X6, '6': 0X7, '7': 0X8, '8': 0X9, '9': 0XA, '0': 0XB,
    '-': 0XC, '=': 0XD, 'backspace': 0XE, 'tab': 0XF, 'q': 0X10, 'w': 0X11, 'e': 0X12, 'r': 0X13, 't': 0X14, 'y': 0X15,
    'u': 0X16, 'i': 0X17, 'o': 0X18, 'p': 0X19, '[': 0X1A, ']': 0X1B, 'enter': 0X1C, 'left_control': 0X1D, 'a': 0X1E,
    's': 0X1F, 'd': 0X20, 'f': 0X21, 'g': 0X22, 'h': 0X23, 'j': 0X24, 'k': 0X25, 'l': 0X26, ';': 0X27, "'": 0X28,
    '`': 0X29, 'left_shift': 0X2A, '\\': 0X2B, 'z': 0X2C, 'x': 0X2D, 'c': 0X2E, 'v': 0X2F, 'b': 0X30,
    'n': 0X31, 'm': 0X32, ', ': 0X33, '.': 0X34, ' / ': 0X35, 'right_shift': 0X36, ' * (Numpad)': 0X37,
    'left_alt': 0X38, 'spacebar': 0X39, 'caps_lock': 0X3A, 'F1': 0X3B, 'F2': 0X3C, 'F3': 0X3D, 'F4': 0X3E, 'F5': 0X3F,
    'F6': 0X40, 'F7': 0X41, 'F8': 0X42, 'F9': 0X43, 'F10': 0X44, 'num_lock': 0X45, 'scroll_lock': 0X46,
    '7(Numpad)': 0X47, '8(Numpad)': 0X48, '9(Numpad)': 0X49, ' - (Numpad)': 0X4A, '4(Numpad)': 0X4B, '5(Numpad)': 0X4C,
    '6(Numpad)': 0X4D, ' + (Numpad)': 0X4E, '1(Numpad)': 0X4F, '2(Numpad)': 0X50, '3(Numpad)': 0X51, '0(Numpad)': 0X52,
    '.(Numpad)': 0X53, 'F11': 0X57, 'F12': 0X58, 'F13': 0X64, 'F14': 0X65, 'F15': 0X66, 'Enter(Numpad)': 0X9C,
    'right_control': 0X9D, ' / (Numpad)': 0XB5, 'sys Rq': 0XB7, 'right_alt': 0XB8, 'pause': 0XC5, 'home': 0XC7,
    'up_arrow': 0XC8, 'page_up': 0XC9, 'left_arrow': 0XCB, 'right_arrow': 0XCD, 'end': 0XCF, 'down_arrow': 0XD0,
    'page_down': 0XD1, 'insert': 0XD2, 'delete': 0XD3, 'left_window_key': 0XDB, 'right_window_key': 0XDC,
    'menu_key': 0XDD, 'power_key': 0XDE, 'windows': 0XDF,
}
