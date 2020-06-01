#!/bin/env python
"""
submit_muscat_imaging_requestgroup.py

Submit an imaging RequestGroup for the MUSCAT instrument to be scheduled for observing.
"""
import requests

API_TOKEN = 'PlaceApiTokenHere'  # API token obtained from https://observe.lco.global/accounts/profile/
PROPOSAL_ID = 'PlaceProposalHere'  # Proposal IDs may be found here: https://observe.lco.global/proposals/

# The target of the observation
target = {
    'name': 'm40',
    'type': 'ICRS',
    'ra': 185.55221,
    'dec': 58.08294,
    'epoch': 2000
}

# Constraints used for scheduling the observation
constraints = {
    'max_airmass': 1.6,
    'min_lunar_distance': 30
}

# The configurations for this request. The MUSCAT instrument has extra_params within it's instrument
# configurations for the g, r, i, z exposure times and the exposing mode. It has optical_elements groups
# in its instrument configurations for g, r, i, z diffuser states (ON or OFF)
# For more information on the MUSCAT instrument, look here: https://lco.global/observatory/instruments/muscat3/
configurations = [
    {
        'type': 'EXPOSE',
        'instrument_type': '2M0-SCICAM-MUSCAT',
        'target': target,
        'constraints': constraints,
        'acquisition_config': {},
        'guiding_config': {},
        'instrument_configs': [
            {
                'exposure_time': 35.0,
                'exposure_count': 1,
                'optical_elements': {
                    'diffuser_g_position': 'in',
                    'diffuser_r_position': 'out',
                    'diffuser_i_position': 'out',
                    'diffuser_z_position': 'in'
                },
                'extra_params': {
                    'exposure_mode': 'SYNCHRONOUS',  # SYNCHRONOUS or ASYNCHRONOUS
                    'exposure_time_g': 35.0,
                    'exposure_time_r': 33.0,
                    'exposure_time_i': 30.0,
                    'exposure_time_z': 29.5
                }
            }
        ]
    }
]

# The time windows during which this request should be considered for observing. In this example
# we only provide one. These times are in UTC.
windows = [{
    'start': '2020-05-02 00:00:00',
    'end': '2020-05-30 00:00:00'
}]

# The telescope class that should be used for this observation
location = {
    'telescope_class': '2m0'
}

# The full RequestGroup, with additional meta-data
requestgroup = {
    'name': 'Example Request Muscat',  # The title
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
