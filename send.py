import csv
import os
from smtplib import SMTP
import markdown
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


def get_msg(csv_file_path, template):
    with open(csv_file_path, 'r') as file:
        headers = file.readline().split(',')
        headers[len(headers) - 1] = headers[len(headers) - 1][:-1]
    # i am opening the csv file two times above and below INTENTIONALLY, changing will cause error
    with open(csv_file_path, 'r') as file:
        data = csv.DictReader(file)
        for row in data:
            required_string = template
            for header in headers:
                value = row[header]
                required_string = required_string.replace(f'${header}', value)
            yield row['EMAIL'], required_string







def send_emails(server: SMTP, template,SENDER_EMAIL, displayname):

    sent_count = 0

    for receiver, message in get_msg('data.csv', template):

        multipart_msg = MIMEMultipart("alternative")

        multipart_msg["Subject"] = message.splitlines()[0]
        multipart_msg["From"] = displayname + f' <{SENDER_EMAIL}>'
        multipart_msg["To"] = receiver

        text = message
        html = markdown.markdown(text)

        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        multipart_msg.attach(part1)
        multipart_msg.attach(part2)



        try:
            server.sendmail(SENDER_EMAIL, receiver,
                            multipart_msg.as_string())
        except Exception as err:
            print(f'Problem occurend while sending to {receiver} ')
            print(err)
            input("PRESS ENTER TO CONTINUE")
        else:
            sent_count += 1

    print(f"Sent {sent_count} emails")


def send(SENDER_EMAIL, PASSWORD, displayname):
    host = "smtp.gmail.com"
    port = 587  # TLS replaced SSL in 1999

    with open('compose.md') as f:
        template = f.read()

    server = SMTP(host=host, port=port)
    server.connect(host=host, port=port)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(user=SENDER_EMAIL, password=PASSWORD)

    send_emails(server, template, SENDER_EMAIL, displayname)

    server.quit()
    time.sleep(300)


