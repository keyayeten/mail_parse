import aioimaplib
import email
from email.header import decode_header


async def mail_receiving(username, password):
    mail = aioimaplib.IMAP4_SSL("imap.gmail.com")
    await mail.wait_hello_from_server()

    await mail.login(username, password)

    await mail.select("inbox")

    status, messages = await mail.search(None, "ALL")
    messages = messages[0].split()

    for mail_id in messages:
        res, msg = await mail.fetch(mail_id, "(RFC822)")
        for response_part in msg:
            if isinstance(response_part, tuple):
                email_message = email.message_from_bytes(response_part[1])
                subject, encoding = decode_header(email_message["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding)

                yield {
                    "Subject": subject,
                    "From": email_message.get("From"),
                    "To": email_message.get("To"),
                    "Date": email_message.get("Date")
                }

    await mail.logout()
