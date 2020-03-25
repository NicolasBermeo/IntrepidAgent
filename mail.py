import smtplib
import ssl
import sys
import os

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from configure import get_config

# --- MAILING FUNCTION ---
'''
    This function is used to mail a list of recipients when a camera is marked as offline.

    mail() receives a message from the polling function and uses it to form an email. This email
    is then sent out to all addresses contained in mail.json.
        It does not return any value.
'''
# ------------------------
def mail(msg):
    try:
        emails = get_config('mail')
        auth = get_config('auth')
    except (IOError):
        print('\n\nAn existing mail and/or auth configuration file could not be found at:\n' + os.getcwd() +
            '\config\n\n')
        sys.exit(0)

    port = 465
    sender = str(auth[0])
    password = str(auth[1])


    message = MIMEMultipart("alternative")
    message["Subject"] = "Camera Down!"
    message["From"] = sender

    text = """\
        Hello,
        {}""".format(msg)

    html = """\
        <html>
            <body>
                <p>Hello,<br>
                    {}
                </p>
            </body>
        </html>
    """.format(msg)

    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    message.attach(part1)
    message.attach(part2)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', port, context=context) as server:
        
        try:
            server.login(sender, password)
        except (smtplib.SMTPAuthenticationError):
            print('\n\nAn invalid auth configuration file has been found. Now exiting...\n\n')
            sys.exit(1)   

        for x in range (0, int(len(emails))):
            message["To"] = emails[x]
            try:
                server.sendmail(sender, emails[x], message.as_string())
            except smtplib.SMTPRecipientsRefused:
                print('\n\nAn invalid mail configuration file has been found. Now exiting...\n\n')
                sys.exit(1)
