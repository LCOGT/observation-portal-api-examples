#!/bin/env python
"""
submit_cadence_request.py

Submit a RequestGroup to the cadence endpoint, which generates for you in it's response a new
RequestGroup that has many Requests that observe on a cadence. This new RequestGroup can
then be submitted.
"""
import requests

API_TOKEN = 'PlaceApiTokenHere'  # API token obtained from https://observe.lco.global/accounts/profile/
PROPOSAL_ID = 'PlaceProposalHere'  # Proposal IDs may be found here: https://observe.lco.global/proposals/

# The cadence we want for this observation
cadence = {
    'start': '2019-05-01 00:00:00',
    'end': '2019-05-30 00:00:00',
    'period': 24,
    'jitter': 12.0
}

# The target of the observation
target = {
    'name': 'm83',
    'type': 'ICRS',
    'ra': 204.253,
    'dec': -29.865,
    'epoch': 2000
}

# Additional constraints to be added to this configuration
constraints = {
    'max_airmass': 1.6,
    'min_lunar_distance': 30
}

# The configurations for this request. In this example we are taking 2 exposures with
# different filters and exposure times. The fields acquisition_config and guiding_config 
# are required fields in a configuration that are ultimately filled in with defaults 
# if the submitted values are empty.
configurations = [
    {
        'type': 'EXPOSE',
        'instrument_type': '1M0-SCICAM-SINISTRO',
        'target': target,
        'constraints': constraints,
        'acquisition_config': {},
        'guiding_config': {},
        'instrument_configs': [
            {
                'exposure_time': 30,
                'exposure_count': 1,
                'optical_elements': {
                    'filter': 'v'
                }
            }
        ]
    },
    {
        'type': 'EXPOSE',
        'instrument_type': '1M0-SCICAM-SINISTRO',
        'target': target,
        'constraints': constraints,
        'acquisition_config': {},
        'guiding_config': {},
        'instrument_configs': [
            {
                'exposure_time': 30,
                'exposure_count': 1,
                'optical_elements': {
                    'filter': 'b'
                }
            }
        ]
    }
]

# We do not provide windows for a cadence request
windows = []

# The telescope class that should be used for this observation
location = {
    'telescope_class': '1m0'
}

# The full RequestGroup, with additional meta-data
requestgroup = {
    'name': 'Cadence Example',  # The title
    'proposal': PROPOSAL_ID,
    'ipp_value': 1.05,
    'operator': 'SINGLE',
    'observation_type': 'NORMAL',
    'requests': [{
        'cadence': cadence,
        'configurations': configurations,
        'windows': windows,
        'location': location,
    }]
}

# Submit the fully formed cadence RequestGroup
response = requests.post(
    'https://observe.lco.global/api/requestgroups/cadence/',
    headers={'Authorization': 'Token {}'.format(API_TOKEN)},
    json=requestgroup  # Make sure you use json!
)

# Make sure this API call was successful
try:
    response.raise_for_status()
except requests.exceptions.HTTPError as exc:
    print('Request failed: {}'.format(response.content))
    raise exc

# The API has returned a new RequestGroup with many requests with windows that
# satisfy the provided cadence parameters. We can review and submit if it looks good.
cadence_request = response.json()

print('Cadence generated {} requests'.format(len(cadence_request['requests'])))
i = 1
for request in cadence_request['requests']:
    print('Request {0} window start: {1} window end: {2}'.format(
        i, request['windows'][0]['start'], request['windows'][0]['end']
    ))
    i = i + 1

# Looks good? Submit to the regular /api/requestgroups/ endpoint
response = requests.post(
    'https://observe.lco.global/api/requestgroups/',
    headers={'Authorization': 'Token {}'.format(API_TOKEN)},
    json=cadence_request  # Make sure you use json!
)

# Make sure this API call was successful
try:
    response.raise_for_status()
except requests.exceptions.HTTPError as exc:
    print('Request failed: {}'.format(response.content))
    raise exc

requestgroup_dict = response.json()

# Print out the url on the portal where we can view the submitted request
print('View this observing request: https://observe.lco.global/requestgroups/{}/'.format(requestgroup_dict['id']))
