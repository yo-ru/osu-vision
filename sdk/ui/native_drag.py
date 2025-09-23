import ctypes
from ctypes import wintypes

user32 = ctypes.windll.user32
WM_SYSCOMMAND = 0x0112
SC_MOVE       = 0xF010
HTCAPTION     = 0x0002
SC_DRAGMOVE   = SC_MOVE + HTCAPTION  # 0xF012

def sysmove(hwnd):
    user32.ReleaseCapture()
    user32.SendMessageW(wintypes.HWND(hwnd), WM_SYSCOMMAND, SC_DRAGMOVE, 0)