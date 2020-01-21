import pickle
import time
import os.path
import settings
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import base64
import email
from apiclient import errors

class snippet_reader():

    def __init__(self):
        self.SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
        self.creds = None
        self.service = None

    def wait(self, given_time):
        time.sleep(given_time)

    def get_code(self, salt_number=1):
        #pre-emptive filter by only finding the message addressed to the specific SALTed email.
        toSaltEmail = 'to:'+ settings.EMAIL + '+' + str(salt_number) + '@gmail.com'
        #toSaltEmail = 'akrerollingacc@gmail.com'

        messages = []

        try:
            while len(messages) == 0:

                results = self.service.users().messages().list(userId='me', q=toSaltEmail).execute()
                messages = results.get('messages', [])
                    #yostar email binding is identical for both initial binding and redemption. uh...
                    #ideally only one message though.
                if len(messages) !=0:
                    msg = self.service.users().messages().get(userId='me', id=messages[0]['id'], format='full').execute()
                    #msg_str = base64.urlsafe_b64decode(msg['payload']['body'][0]['body']['data'])
                    #print(msg_str)
                    #msg is a dict
                    #at some point i will go "fk it" and just use snippet since the email is short enough.
                    #fk this I'm using snippets.
                    msg = msg['snippet']
                    code = msg[76:82:1] #substring of snippet containing code.
                    return code

                    #if (message.get['payload'].headers['Subject'] == 'Verification Code'):
                    #['payload']['headers']['subject']

                self.wait(10) #so we don't go crazy pinging servers.
        except KeyboardInterrupt:
            print('\n')


    def main(self):
        self.creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('gmail', 'v1', credentials=creds)



if __name__ == '__main__':
    m = snippet_reader()
    m.main()
