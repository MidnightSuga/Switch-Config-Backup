import smtplib
from email.message import EmailMessage


class Email:
    @staticmethod
    def sendemail(emailaddress):
        msg = EmailMessage()
        msg.set_content("Switch Config Backup finished successfully.")

        msg['Subject'] = 'Backup Script Finished'
        msg['From'] = '<FROMADDRESS>'
        msg['To'] = emailaddress

        s = smtplib.SMTP('<SMTPSERVER>')
        s.send_message(msg)
        s.quit()
