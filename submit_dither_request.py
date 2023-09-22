#!/bin/env python
"""
submit_dither_request.py

Submit a Request with dither pattern by utilizing the Expand Dither Pattern API endpoint.

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

# Additional constraints to be added to this configuration
constraints = {
    'max_airmass': 1.6,
    'min_lunar_distance': 30
}

# The configurations for this request. In this example we are taking 1x30s exposure in
# the V-band. The fields acquisition_config and guiding_config are required fields in a 
# configuration that are ultimately filled in with defaults if the submitted values are empty.
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

# The below lines expand your configuration into multiple InstrumentConfigs, each 
# with a dithered position according to the expansion parameters.
# See https://developers.lco.global/#expand-dither-pattern for more info.

# Select configuration to dither (we will choose the first for this example):
dithered_configuration = configurations[0]

dithered_configuration = requests.post(
    'https://observe.lco.global/api/configurations/dither/',
    headers={'Authorization': 'Token {}'.format(API_TOKEN)},
    json={
        'pattern': 'line', # accepts line, grid, or spiral
        'num_points': 3, # the number of points in the dither pattern (not required for grid)
        'point_spacing': 5, # distance in arcseconds between each point (or columns in grid)
        'configuration': dithered_configuration
        }
).json()

# Reinsert the configuration back into the list of configurations.
configurations[0] = dithered_configuration

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

# The full RequestGroup, with additional meta-data
requestgroup = {
    'name': 'Dither Example',  # The title
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
