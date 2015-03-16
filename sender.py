import smtplib
import socket
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate

cur_time = formatdate(timeval=None, localtime=True)


def send_mail(send_to, subject, text, files=None, send_from=socket.gethostname(), server='localhost'):
    # Forming e-mail headers.
    msg = MIMEMultipart('application', 'base64')
    msg['Subject'] = subject
    msg['From'] = send_from
    msg['To'] = send_to

    msg.attach(MIMEText(text))

    with open(files, "rb") as attach_file:
        part = MIMEApplication(attach_file.read())
        part.add_header('Content-Disposition', 'attachment', filename=basename(files))
        msg.attach(part)

    smtp = smtplib.SMTP(server)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()