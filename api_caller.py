# /usr/local/bin/python
# encoding = utf-8

import sys, os, re
import sigv4
import requests
import inspect


def call_api(method, endpoint, action, payload='', path='/'):
    """
    Generate a signed call to the API to return status and content

    :param method: GET or POST method verb
    :type method: str
    :param endpoint: endpoint of the api for the service (fcu.eu-west-2.outscale.com)
    :type endpoint: str
    :param action: REST formated action (see docs.outscale.com)
    :type action: str
    :param payload: payload for POST requests
    :type payload: str
    :param path: path of the API
    :type path: str
    :return: status_code and content
    :rtype: tuple
    """

    access_key = os.environ.get('AWS_ACCESS_KEY_ID')
    secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')

    if access_key is None or secret_key is None:
        print 'No access key is available.'
        sys.exit()

    services = {'fcu': 'ec2',
                'lbu': 'elb',
                'osu': 's3',
                'eim': 'iam',
                'icu': 'icu'}

    request_parameters = '{}&Version=2016-10-24'.format(action)

    params = { 'method': method,
                'service': services[endpoint.split('.')[0]],
                'host': endpoint,
                'request_parameters': request_parameters,
                'payload': payload,
                'path': path,
                'access_key': access_key,
                'secret_key': secret_key }

    signed_request, headers = sigv4.sign_request(params)

    endpoint = 'https://{}'.format(params['host'])
    if method == 'GET':
        request_url = endpoint + '?' + signed_request
        r = requests.get(request_url, headers=headers)
    # elif method == 'POST':
    #     r = requests.post(endpoint, data=signed_request, headers=headers)
    else:
        return 0, 'Method not supported'
    # Clean XML for proper parsing
    pattern = "( xmlns\=\"[:.a-zA-Z0-9\/-]*\")"
    req = re.sub(pattern, '', r.text)

    return r.status_code, req
