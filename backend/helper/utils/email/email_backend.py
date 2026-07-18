import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.mime.base import MIMEBase
from django.conf import settings
import pathlib
import requests
import json

"""Declare function to get Email configuration"""


class EmailBackEnd:

    def sendEmail(self, template, receiverEmail, emailSubject):

        email_sender = settings.EMAIL_FROM

        msg = MIMEMultipart()
        msg['From'] = email_sender
        msg['To'] = receiverEmail
        msg['Subject'] = emailSubject

        msg.attach(MIMEText(template, 'html'))

        # msg.attach(part)

        try:
            server = smtplib.SMTP(settings.EMAIL_HOST, int(settings.EMAIL_PORT))
            server.ehlo()
            server.starttls()
            server.login(settings.EMAIL_USER, settings.EMAIL_PASS)
            text = msg.as_string()
            server.sendmail(email_sender, receiverEmail, text)
            print('email sent')
            server.quit()
        except:
            print("SMPT server connection error")
        return True

    def sendEmailWithFile(self, template, emailSubject, receiverEmail, pathToFile, docName):

        sender_email = settings.EMAIL_FROM
        username = settings.EMAIL_USER
        password = settings.EMAIL_PASS
        port = settings.EMAIL_PORT
        host = settings.EMAIL_HOST

        # Create a multipart message and set headers
        message = MIMEMultipart()
        message["From"] = settings.EMAIL_FROM
        message["To"] = receiverEmail
        message["Subject"] = emailSubject

        message.attach(MIMEText(template, "html"))


        # Open PDF file in binary mode
        with open(pathToFile, "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        # Encode file in ASCII characters to send by email
        encoders.encode_base64(part)
        file_extension = pathlib.Path(pathToFile).suffix
        # Add header as key/value pair to attachment part
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {docName}{file_extension}",
        )

        # Add attachment to message and convert message to string
        message.attach(part)
        text = message.as_string()

        # Log in to server using secure context and send email
        # context = ssl.create_default_context()
        if not settings.EMAIL_SSL:
            with smtplib.SMTP(host, port) as server:
                server.login(username, password)
                server.sendmail(sender_email, receiverEmail, text)
        else:
            with smtplib.SMTP_SSL(host, port) as server:
                server.login(username, password)
                server.sendmail(sender_email, receiverEmail, text)
        pass

    def send_grid(self, template, email, subject):

        url = "https://api.sendgrid.com/v3/mail/send"

        payload = json.dumps({
            "personalizations": [
                {
                    "to": [
                        {
                            "email": email
                        }
                    ],
                    "subject": subject
                }
            ],
            "content": [
                {
                    "type": "text/html",
                    "value": template
                }
            ],
            "from": {
                "email": "team@prembly.com",
                "name": "IdEnroll"
            },
            "reply_to": {
                "email": "team@prembly.com",
                "name": "IdEnroll"
            }
        })
        headers = {
            'Authorization': f'Bearer {settings.SENDGRID_API_KEY}',
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        if response.status_code == 202:
            print("Email sent")
        else:
            print(json.loads(response.text))
        pass

    def send_grid_icognito(self, template, email, subject, aws_data: dict):

        url = "https://api.sendgrid.com/v3/mail/send"

        payload = json.dumps({
            "personalizations": [
                {
                    "to": [
                        {
                            "email": email
                        }
                    ],
                    "subject": subject
                }
            ],
            "content": [
                {
                    "type": "text/html",
                    "value": template
                }
            ],
            "from": {
                "email": "team@prembly.com",
                "name": "IdEnroll"
            },
            "reply_to": {
                "email": "team@prembly.com",
                "name": "IdEnroll"
            }
        })
        headers = {
            'Authorization': f'Bearer {settings.SENDGRID_API_KEY}',
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        if response.status_code == 202:
            print("Email sent")
        else:
            print(json.loads(response.text))
        pass


