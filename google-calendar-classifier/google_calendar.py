
import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def get_events(secrets, calendar_id, start_date, end_date):
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(secrets["oauthUserTokenFile"]):
        creds = Credentials.from_authorized_user_file(secrets["oauthUserTokenFile"], SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(secrets["oauthApiTokenFile"], SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(secrets["oauthUserTokenFile"], 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        print('Getting the events')
        events_result = service.events().list(
            calendarId=calendar_id, 
            maxResults=2500,
            orderBy="startTime",
            timeMin=start_date, 
            timeMax=end_date, 
            singleEvents=True,
        ).execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
            return

        # Prints the start and name of the next 10 events
        return events

    except HttpError as error:
        print('An error occurred: %s' % error)
        raise

