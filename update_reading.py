import numpy as np
from datetime import datetime
from he_level_read import he_read

import os.path

# Google dependences
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# Setup google credentials for the app
SCOPES = ["https://www.googleapis.com/auth/drive.file"]
creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())


def update_values(spreadsheet_id, range_name, value_input_option, values):
  """
  Writes the value to the google sheet specified by the id
  Function as in the demo from Google
  """
  try:
    service = build("sheets", "v4", credentials=creds)
    
    body = {"values": values}
    result = (
        service.spreadsheets()
        .values()
        .update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption=value_input_option,
            body=body,
        )
        .execute()
    )
    print(f"{result.get('updatedCells')} cells updated.")
    return result
  except HttpError as error:
    print(f"An error occurred: {error}")
    return error


def main():
   """
   Write the inquired He level to the specific cell in specified google sheet.
   """
   
   # Get the current time and write it as a string
   timenow = datetime.now()
   timestr = timenow.strftime("%H:%M:%S %Y/%m/%d")
   # Get the helium level through the read function (and convert to string)
   he_level = str(he_read())
   print(he_level)
   print(timestr)

   # Write to the online sheet
   sheet_id = "10o_22Zw1_0WNf7BgEj3T8pjgc0lL05E-6jaVjInOhUI"
   update_values(
      sheet_id,
      "A2:B2",
      "USER_ENTERED",
      [[he_level, timestr]],
   )


if __name__ == "__main__":
  main()

