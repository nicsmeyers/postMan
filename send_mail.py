from googleapiclient import errors
from gmail_connect import Create_Service
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time

CLIENT_SECRET_FILE = 'client_secret.json'
API_NAME = 'gmail'
API_VERSION = 'v1'
SCOPES = ['https://mail.google.com/']

page = 1
token = ""
donors = set()

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

while True:
    try:
        messages = service.users().messages().list(userId="me", pageToken=token).execute().get('messages', [])
        token = service.users().messages().list(userId="me", pageToken=token).execute().get('nextPageToken', [])

        for message in messages:
            content = service.users().messages().get(userId="me", id=message["id"]).execute()
            for donor in content["payload"]["headers"]:
                if donor["name"] == "From":
                    donors.add(donor["value"].split()[-1])
        print("Page %s finished" % page)
        page = page + 1
        time.sleep(2)
    except errors.HttpError:
        break

with open("donor_list.txt", "w") as file:
    for donor in donors:
        file.write("%s\n" % donor)
    file.close()
