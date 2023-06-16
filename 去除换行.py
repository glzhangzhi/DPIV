import clipboard
from time import sleep

s = ""
while 1:
    sleep(1)
    n_s = clipboard.paste()
    if n_s != s:
        s = n_s.replace('\r\n', ' ')
        clipboard.copy(s)