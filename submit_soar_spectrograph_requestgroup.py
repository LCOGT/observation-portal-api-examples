#!/bin/env python
"""
submit_soar_spectrograph_requestgroup.py

Submit a spectrograph RequestGroup to be scheduled for observing on the SOAR telescope.
"""
import requests

API_TOKEN = 'PlaceApiTokenHere'  # API token obtained from https://observe.lco.global/accounts/profile/
PROPOSAL_ID = 'PlaceProposalHere'  # Proposal IDs may be found here: https://observe.lco.global/proposals/

# The target of the observation
target = {
    'name': 'm83',
    'type': 'ICRS',
    'ra': 204.254,
    'dec': -29.865,
    'epoch': 2000
}

# Constraints used for scheduling the observation
constraints = {
    'max_airmass': 1.6,
    'min_lunar_distance': 30
}

# The configurations for this request. In this example we are taking on SPECTRUM and one ARC.
# The fields acquisition_config and guiding_config are required fields in a configuration that are ultimately
# filled in with defaults if the submitted values are empty (as for the ARC).
configurations = [
    {
        'type': 'SPECTRUM',
        'instrument_type': 'SOAR_GHTS_REDCAM',
        'target': target,
        'constraints': constraints,
        'acquisition_config': {
            'mode': 'MANUAL'
        },
        'guiding_config': {
            'mode': 'ON',
            'optional': False
        },
        'instrument_configs': [
            {
                'exposure_time': 300,
                'exposure_count': 1,
                'rotator_mode': 'SKY',
                'mode': 'GHTS_R_400m1_2x2',
                'optical_elements': {
                    'slit': 'slit_1.0as',
                    'grating': 'SYZY_400'
                },
                'extra_params': {
                    'rotator_angle': 0
                }
            }
        ]
    },
    {
        'type': 'ARC',
        'instrument_type': 'SOAR_GHTS_REDCAM',
        'target': target,
        'constraints': constraints,
        'acquisition_config': {},
        'guiding_config': {},
        'instrument_configs': [
            {
                'exposure_time': 1,
                'exposure_count': 1,
                'rotator_mode': 'SKY',
                'mode': 'GHTS_R_400m1_2x2',
                'optical_elements': {
                    'slit': 'slit_1.0as',
                    'grating': 'SYZY_400'
                },
                'extra_params': {
                    'rotator_angle': 0
                }
            }
        ]
    }
]

# The time windows during which this request should be considered for observing. In this example
# we only provide one. These times are in UTC.
windows = [{
    'start': '2019-07-01 00:00:00',
    'end': '2019-08-15 00:00:00'
}]

# The telescope class that should be used for this observation
location = {
    'telescope_class': '4m0'
}

# The full RequestGroup, with additional meta-data
requestgroup = {
    'name': 'Example Request 5',  # The title
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
