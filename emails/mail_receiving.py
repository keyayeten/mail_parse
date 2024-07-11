import imaplib
import email
from email.header import decode_header


def mail_receiving(username, password):
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(username, password)

    mail.select("inbox")

    status, messages = mail.search(None, "ALL")
    messages = messages[0].split()

    for mail_id in messages:
        res, msg = mail.fetch(mail_id, "(RFC822)")
        for response_part in msg:
            if isinstance(response_part, tuple):
                email_message = email.message_from_bytes(response_part[1])
                subject, encoding = decode_header(email_message["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding)
                yield {
                    "subject:": subject,
                    "sender:": email_message.get("From"),
                    "shortDescription:": email_message.get("To"),
                    "date:": email_message.get("Date")
                }
    mail.close()
    mail.logout()

# {
#     "subject": "Subject 3",
#     "sender": "sender3@example.com",
#     "date": "2023-07-12",
#     "shortDescription": "Description 3"
# }
