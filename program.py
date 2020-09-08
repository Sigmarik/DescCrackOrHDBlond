import smtplib
import time
import imaplib
import email
import sys
import os
import time

f_path = open('path_to_false_file.txt', 'r')
os.startfile(f_path.read())

ORG_EMAIL   = "@gmail.com"
FROM_EMAIL  = "proect.board.22" + ORG_EMAIL
FROM_PWD    = "q1w2e3r4t5y6u7i8o9p0[-]="
SMTP_SERVER = "imap.gmail.com"
SMTP_PORT   = 993

out = open('output.txt', 'w')
try:
    file = open('last_ind.txt', 'r')
except:
    file = open('last_ind.txt', 'w')
    file.write('0')
    file.close()
    file = open('last_ind.txt', 'r')
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
            file = open('last_ind.txt', 'w')
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
                            return 0
                        if email_subject == 'MINECRAFTFLOW':
                            return 1
                    else:
                        print('ERR')
    return -1

m_path = open('path_to_minecraft.txt', 'r')
print('Reading GMAIL', FROM_EMAIL)
while True:
    res = read_email_from_gmail()
    if res == 0:
        print('Поиграем в майнкрафт?')
        os.startfile(m_path.read())
    if res == 1:
        print('МАЙНКРАФТ МОЯ ЖИИЗНЬ!!!')
        for i in range(10):
            os.startfile(m_path.read())
out.close()
