import json
import os
import sys

from googleapiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

class OAuthAuthentication:
    def __init__(self):
        self.CLIENT_SECRETS_FILE = "secret/client_secret.json"
        self.YOUTUBE_READ_WRITE_SCOPE = "https://www.googleapis.com/auth/youtube"
        self.YOUTUBE_API_SERVICE_NAME = "youtube"
        self.YOUTUBE_API_VERSION = "v3"
        self.MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:

   %s

with information from the API Console
https://console.developers.google.com/

For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   self.CLIENT_SECRETS_FILE))
        
        self.credentials = self.get_credentials()
    
    def get_credentials(self):
        flow = flow_from_clientsecrets(
            self.CLIENT_SECRETS_FILE,
            message=self.MISSING_CLIENT_SECRETS_MESSAGE,
            scope=self.YOUTUBE_READ_WRITE_SCOPE
        )

        storage = self.get_storage()
        credentials = storage.get()

        if credentials is None or credentials.invalid:
            flags = argparser.parse_args()
            credentials = run_flow(flow, storage, flags)
        
        return credentials

    def get_storage(self):
        return Storage("secret/%s-oauth2.json" % sys.argv[0])
    
    def get_access_token(self):
        with open(f'secret/{sys.argv[0]}-oauth2.json') as f:
            data = json.load(f)
    
        return data["access_token"]