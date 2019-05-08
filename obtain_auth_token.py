#!/bin/env python
"""
obtain_auth_token.py

Obtain an API token via username/password.

You may also obtain your API key from your profile page: https://observe.lco.global/accounts/profile/
"""
import requests

USERNAME = 'PlaceUsernameHere'
PASSWORD = 'PlacePasswordHere'

response = requests.post(
    'https://observe.lco.global/api/api-token-auth/',
    data={
        'username': USERNAME,
        'password': PASSWORD
    }
)

# Make sure this api call was successful
try:
    response.raise_for_status()
except requests.exceptions.HTTPError as exc:
    print('Request failed: {}'.format(response.content))
    raise exc

# Print out your API token:
print(response.json()['token'])
