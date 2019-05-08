#!/bin/env python
"""
query_requestgroups.py

Get RequestGroups belonging to a specific proposal.
"""
import requests

API_TOKEN = 'PlaceApiTokenHere'  # API token obtained from https://observe.lco.global/accounts/profile/
PROPOSAL_ID = 'PlaceProposalHere'  # Proposal IDs may be found here: https://observe.lco.global/proposals/

# Use the requests library to make an HTTP request to the API
response = requests.get(
    'https://observe.lco.global/api/requestgroups/?proposal={}'.format(PROPOSAL_ID),
    headers={'Authorization': 'Token {}'.format(API_TOKEN)}
)

# Make sure the API call was successful
try:
    response.raise_for_status()
except requests.exceptions.HTTPError as exc:
    print('Request failed: {}'.format(response.content))
    raise exc

# Loop over the returned RequestGroups and print some information about them
for requestgroup in response.json()['results'][:5]:  # Get the first 5 RequestGroups
    print('RequestGroup "{0}" status is {1}'.format(
        requestgroup['name'], requestgroup['state']
    ))
    print('View the RequestGroup here: https://observe.lco.global/requestgroups/{0}/\n'.format(
        requestgroup['id']
    ))
