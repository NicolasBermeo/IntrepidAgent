mport smtplib
import ssl
import sys
import os
​
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
​
from configure import get_config
​
def mail(msg):
    try:
        emails = (get_config('mail'))
    except (IOError):
        print('\n\nAn existing mail configuration file could not be found at:\n' + os.getcwd() +
            'config/\n\n')
        sys.exit(0) 
​
    port = 465
    sender = 'pipoller.alert@gmail.com'
    password = ('pipollermail123')
​
​
    message = MIMEMultipart("alternative")
    message["Subject"] = "multipart test"
    message["From"] = sender
​
    text = """\
        Hello,
        {}""".format(msg)
​
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
​
    message.attach(part1)
    message.attach(part2)
​
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', port, context=context) as server:
        server.login(sender, password)
​
        for x in range (0, int(len(emails))):
            message["To"] = emails[x]
            server.sendmail(sender, emails[x], message.as_string())
