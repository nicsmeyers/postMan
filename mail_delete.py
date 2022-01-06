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

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

emails2keep = []
emails2delete = []

with open("donor_list.txt", "r") as file:
    emails = file.readlines()
    file.close()

for email in emails:
    while True:
        email = email.replace("\n", "")
        print(email)
        keep = input("Do you want to keep these emails? (Y/N): ")
        if keep.lower() == "y":
            emails2keep.append(email)
            break
        elif keep.lower() == "n":
            emails2delete.append(email)
            break
        else:
            print("Please enter a valid selection")

while True:
    try:
        messages = service.users().messages().list(userId="me", pageToken=token).execute().get('messages', [])
        token = service.users().messages().list(userId="me", pageToken=token).execute().get('nextPageToken', [])

        for message in messages:
            content = service.users().messages().get(userId="me", id=message["id"]).execute()
            for donor in content["payload"]["headers"]:
                for email in emails2delete:
                    if donor["name"] == "From":
                        if email == donor["value"].split()[-1]:
                            service.users().messages().trash(userId="me", id=message["id"]).execute()
        print("Page %s finished" % page)
        page = page + 1
        time.sleep(2)
    except errors.HttpError:
        break