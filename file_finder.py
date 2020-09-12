import os
def search(fname):
    for i, fl in enumerate(os.walk('C:\\')):
        if i % 10000 == 0:
            print(i)
            print(fl, fl[0][fl[0].rfind('\\')+1:])
        if fl[0][fl[0].rfind('\\')+1:] == fname:
            return fl[0]
print(search('chrome.exe'))
