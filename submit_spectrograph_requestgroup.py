#!/bin/env python
"""
submit_spectrograph_requestgroup.py

Submit a RequestGroup for a spectrographic observation to be scheduled for
observing. Note this is almost identical to submit_imaging_requestgroup.py
except we are changing the instrument type and configurations.
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

# Constraints used for scheduling this observation
constraints = {
    'max_airmass': 2
}

# The configurations for this request. In this example we are taking 2 exposures with different filters.
configurations = [{
    'type': 'SPECTRUM',
    'instrument_type': '2M0-FLOYDS-SCICAM',
    'constraints': constraints,
    'target': target,
    'acquisition_config': {
        'mode': 'WCS'
    },
    'guiding_config': {
        'mode': 'ON',
        'optional': False
    },
    'instrument_configs': [
        {
            'exposure_time': 30,
            'exposure_count': 1,
            'rotator_mode': 'VFLOAT',
            'optical_elements': {
                'slit': 'slit_2.0as'
            }
        }
    ]
}]

# The windows during which this request should be considered for observing.
# In this example we only provide one.
windows = [{
    'start': '2019-05-02 00:00:00',
    'end': '2019-05-30 00:00:00'
}]

# The telescope class that should be used for this observation
location = {
    'telescope_class': '2m0'
}

# The full RequestGroup, with additional meta-data
requestgroup = {
    'name': 'Example Spectrograph Request',  # The title
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

# Make sure this api call was successful
try:
    response.raise_for_status()
except requests.exceptions.HTTPError as exc:
    print('Request failed: {}'.format(response.content))
    raise exc

requestgroup_dict = response.json()  # The API will return the newly submitted RequestGroup as json

# Print out the url on the portal where we can view the submitted request
print('View the observing request: https://observe.lco.global/requestgroups/{}/'.format(requestgroup_dict['id']))
