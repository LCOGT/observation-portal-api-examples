#!/bin/env python
"""
submit_direct_submission_observation.py

Submit an DIRECT submission observation.
DIRECT submissions are observations that must take place at a fixed time and location,
and are separate from the scheduler's scheduled observations.
NOTE: your proposal must allow direct submissions for this to be accepted.
"""
import requests

API_TOKEN = 'PlaceApiTokenHere'  # API token obtained from https://observe.lco.global/accounts/profile/
PROPOSAL_ID = 'PlaceProposalHere'  # Proposal IDs may be found here: https://observe.lco.global/proposals/

# The target of the observation
target = {
    'name': 'm83',
    'type': 'ICRS',
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
# different filters and exposure times. The fields acquisition_config and guiding_config
# are required fields in a configuration that are ultimately filled in with defaults
# if the submitted values are empty.
configurations = [
    {
        'type': 'EXPOSE',
        'instrument_type': '1M0-SCICAM-SINISTRO',
        'instrument_name': 'fa14',
        'guide_camera_name': 'ef02',
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

# The full Observation
observation = {
    'name': 'Example Direct Submission',  # The title
    'site': 'cpt',
    'enclosure': 'doma',
    'telescope': '1m0a',
    'start': '2023-08-20T21:16:22Z',
    'end': '2023-08-20T21:21:22Z',
    'proposal': PROPOSAL_ID,
    'priority': 10,
    'operator': 'SINGLE',
    'request': {
        'configurations': configurations,
        'optimization_type': 'TIME',
        'observation_note': 'This is an example direct submission'
    }
}

# Submit the fully formed Observation
response = requests.post(
    'https://observe.lco.global/api/schedule/',
    headers={'Authorization': 'Token {}'.format(API_TOKEN)},
    json=observation  # Make sure you use json!
)

# Make sure the API call was successful
try:
    response.raise_for_status()
except requests.exceptions.HTTPError as exc:
    print('API call failed: {}'.format(response.content))
    raise exc

observation_dict = response.json()  # The API will return the newly submitted observation as json

# Print out the url on the portal where we can view the submitted observation
print('View the observing request: https://observe.lco.global/observations/{}/'.format(observation_dict['id']))
