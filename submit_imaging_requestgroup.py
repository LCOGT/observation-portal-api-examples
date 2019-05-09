#!/bin/env python
"""
submit_imaging_requestgroup.py

Submit an imaging RequestGroup to be scheduled for observing.
"""
import requests

API_TOKEN = 'PlaceApiTokenHere'  # API token obtained from https://observe.lco.global/accounts/profile/
PROPOSAL_ID = 'PlaceProposalHere'  # Proposal IDs may be found here: https://observe.lco.global/proposals/

# The target of the observation
target = {
    'name': 'm83',
    'type': 'SIDEREAL',
    'ra': 204.253,
    'dec': -29.865,
    'epoch': 2000
}

# Constraints used for scheduling the observation
constraints = {
    'max_airmass': 1.6,
    'min_lunar_distance': 30
}

# The configurations for this request. In this example we are taking 2 exposures with
# different filters and exposure times.
configurations = [
    {
        'type': 'EXPOSE',
        'instrument_type': '1M0-SCICAM-SINISTRO',
        'target': target,
        'constraints': constraints,
        # The fields acquisition_config and guiding_config are required fields that are ultimately
        # filled in with defaults if the submitted values are empty.
        'acquisition_config': {},
        'guiding_config': {},
        'instrument_configs': [
            {
                'exposure_time': 30,
                'exposure_count': 1,
                'optical_elements': {
                    'filter': 'v'
                }
            },
            {
                'exposure_time': 60,
                'exposure_count': 1,
                'optical_elements': {
                    'filter': 'b'
                }
            }
        ]
    }
]

# The time windows during which this request should be considered for observing. In this example
# we only provide one. These times are in UTC.
windows = [{
    'start': '2019-05-02 00:00:00',
    'end': '2019-05-30 00:00:00'
}]

# The telescope class that should be used for this observation
location = {
    'telescope_class': '1m0'
}

# The full userrequest, with additional meta-data
requestgroup = {
    'name': 'Example Request 3',  # The title
    'proposal': PROPOSAL_ID,
    'ipp_value': 1.05,
    'operator': 'SINGLE',
    'observation_type': 'NORMAL',
    'requests': [{
        'configurations': configurations,
        'windows': windows,
        'location': location,
    }]
}

# Submit the fully formed RequestGroup
response = requests.post(
    'https://observe.lco.global/api/requestgroups/',
    headers={'Authorization': 'Token {}'.format(API_TOKEN)},
    json=requestgroup  # Make sure you use json!
)

# Make sure the API call was successful
try:
    response.raise_for_status()
except requests.exceptions.HTTPError as exc:
    print('API call failed: {}'.format(response.content))
    raise exc

requestgroup_dict = response.json()  # The API will return the newly submitted requestgroup as json

# Print out the url on the portal where we can view the submitted request
print('View the observing request: https://observe.lco.global/requestgroups/{}/'.format(requestgroup_dict['id']))
