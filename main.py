import imaplib
import email
from email.header import decode_header

# account credentials
username = "enter_username"
password = "enter_password"
# counter for emails deleted
emails_deleted = 0

# create an IMAP4 class with SSL
imap = imaplib.IMAP4_SSL("imap.gmail.com")
# authenticate
imap.login(username, password)

# select the mailbox I want to delete in
# if you want SPAM, use imap.select("SPAM") instead
imap.select("INBOX")

# search for specific mails by sender
status, messages = imap.search(None, 'FROM "email@?.domain"')

# convert messages to a list of email IDs
messages = messages[0].split(b' ')

for mail in messages:
    _, msg = imap.fetch(mail, "(RFC822)")
    # you can delete the for loop for performance if you have a long list of emails
    # because it is only for printing the SUBJECT of target email to delete

    for response in msg:
        if isinstance(response, tuple):
            msg = email.message_from_bytes(response[1])
            # decode the email subject
            subject = decode_header(msg["Subject"])[0][0]
            if isinstance(subject, bytes):
                # if it's a bytes type, decode to str
                subject = subject.decode()
            print("Deleting", subject)
            emails_deleted += 1
    # # mark the mail as deleted

    imap.store(mail, "+FLAGS", "\\Deleted")

# permanently remove mails that are marked as deleted
# from the selected mailbox (in this case, INBOX)

print(f"\nDeleting all {emails_deleted} emails marked deleted")

imap.expunge()
# close the mailbox
imap.close()
# logout from the account
imap.logout()