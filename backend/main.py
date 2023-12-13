""""
Main application that sets up the Strava client to communicate with the
Strava API
"""

import os
from stravalib import Client

# Load API credentials from environment variables
STRAVA_CLIENT_ID = os.environ.get("STRAVA_CLIENT_ID")
STRAVA_CLIENT_SECRET = os.environ.get("STRAVA_CLIENT_SECRET")
STRAVA_ACCESS_TOKEN = os.environ.get("STRAVA_ACCESS_TOKEN")
STRAVA_REFRESH_TOKEN = os.environ.get("STRAVA_REFRESH_TOKEN")

REDIRECT_URL = 'http://localhost:5000/authorization'

# Initialize Strava client
client = Client()

# Set access token (optional if you want to use client ID and client secret directly)
if STRAVA_ACCESS_TOKEN:
    client.access_token = STRAVA_ACCESS_TOKEN
    client.refresh_token = STRAVA_REFRESH_TOKEN

# If access token is not provided, authenticate using client ID and client secret
elif STRAVA_CLIENT_ID and STRAVA_CLIENT_SECRET:
    authorize_url = (
        client.authorization_url(client_id=STRAVA_CLIENT_ID,
                                 redirect_uri=REDIRECT_URL,
                                 scope='read,activity:read'
                                )
    )

    print(f'Please go to {authorize_url} and authorize access.')

    # Get the authorization response from the user
    code = input('Enter the code from the authorization page: ')

    # Exchange the authorization code for an access token
    access_token_response = (
        client.exchange_code_for_token(
            client_id=STRAVA_CLIENT_ID,
            client_secret=STRAVA_CLIENT_SECRET,
            code=code
            )
        )
    client.access_token = access_token_response['access_token']
    client.refresh_token = access_token_response['refresh_token']


# Example: Fetch athlete's activities
athlete = client.get_athlete()
print(f'Athlete: {athlete.firstname} {athlete.lastname}, ID: {athlete.id}')
