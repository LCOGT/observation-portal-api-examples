#!/bin/env python
'''
query_proposals.py

Return details about proposals you belong to, including time allocations.
'''
import requests

API_TOKEN = 'PlaceApiTokenHere'  # API token obtained from https://observe.lco.global/accounts/profile/

response = requests.get(
    'https://observe.lco.global/api/proposals/',
    headers={'Authorization': 'Token {}'.format(API_TOKEN)}
)

# Make sure this API call was successful
try:
    response.raise_for_status()
except requests.exceptions.HTTPError as exc:
    print('Request failed: {}'.format(response.content))
    raise exc

proposals_dict = response.json()  # API returns a json dictionary containing proposal information

print('Member of {} proposals'.format(proposals_dict['count']))

# Loop over each proposal and print some things about it.
for proposal in proposals_dict['results']:
    print('\nProposal: {}'.format(proposal['id']))
    for time_allocation in proposal['timeallocation_set']:
        print('{0:.3f} out of {1} standard hours used on instrument type {2} for semester {3}'.format(
            time_allocation['std_time_used'],
            time_allocation['std_allocation'],
            time_allocation['instrument_type'],
            time_allocation['semester'],
        ))
