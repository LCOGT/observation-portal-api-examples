# Observation Portal API Examples

This repository contains python scripts demonstrating how to use the [Observation Portal API](https://observe.lco.global/api/).
They can be used as a starting point for writing custom scripts to submit/query observation requests programatically.

**All scripts assume the [requests](http://docs.python-requests.org/en/master/) library is installed.**

### Full Documentation

The example scripts included here are basic. To view the full API documentation, please see the
[Developers Docs](https://developers.lco.global). Check the [Observations section](https://developers.lco.global/#observations) 
for a description of terminology used in this repository.

### Authentication

Most (if not all) of the examples require an authentication token. This token is like a password in that
it is used to authenticate you with the API and make sure you have permission to perform specific actions.
This token must be placed in the HTTP `Authorization` header and is valid forever (or until you revoke it).

You can obtain your authentication token from your [profile page](https://observe.lco.global/accounts/profile/).

If for some reason you are unable to access your profile page (on a server without a graphical interface, for example)
you can obtain your token via API. The [obtain_auth_token.py](obtain_auth_token.py) example does just that.

### Examples

* [query_requestgroups.py](query_requestgroups.py) Query the status of your observation requests.
* [submit_imaging_requestgroup.py](submit_imaging_requestgroup.py) Submit an imaging observation request.
* [submit_repeat_imaging_requestgroup.py](submit_repeat_imaging_requestgroup.py) Submit an imaging observation request with a repeated set of exposures.
* [submit_nonsidereal_target.py](submit_nonsidereal_target.py) Submit an imaging observation request for a non-sidereal target.
* [submit_spectrograph_requestgroup.py](submit_spectrograph_requestgroup.py) Submit a spectrograph observation request.
* [submit_cadence_request.py](submit_cadence_request.py) Submit observation requests on a cadence.
* [query_ipp.py](query_ipp.py) Query details about Intra Proposal Priority.
* [query_proposals.py](query_proposals.py) Query proposal details, including time allocations.
* [obtain_auth_token.py](obtain_auth_token.py) Obtain your API authentication token.
* [submit_soar_imaging_requestgroup.py](submit_soar_imaging_requestgroup.py) Submit an imaging requestgroup for the SOAR telescope.
* [submit_soar_spectrograph_requestgroup.py](submit_soar_spectrograph_requestgroup.py) Submit a spectrograph requestgroup for the SOAR telescope.
