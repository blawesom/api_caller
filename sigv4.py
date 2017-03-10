# /usr/local/bin/python
# encoding = utf-8

import sys, os, base64, datetime, hashlib, hmac


def sign(key, msg):
    return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()


def getSignatureKey(key, dateStamp, regionName, serviceName):
    kDate = sign(('AWS4' + key).encode('utf-8'), dateStamp)
    kRegion = sign(kDate, regionName)
    kService = sign(kRegion, serviceName)
    kSigning = sign(kService, 'aws4_request')
    return kSigning


def sign_request(params):
    region = params['host'].split('.')[1]
    endpoint = 'https://{}'.format(params['host'])

    # Create a date for headers and the credential string
    t = datetime.datetime.utcnow()
    amzdate = t.strftime('%Y%m%dT%H%M%SZ')
    datestamp = t.strftime('%Y%m%d') # Date w/o time, used in credential scope
    canonical_uri = params['path']

    # Query string values must be URL-encoded (space=%20).
    canonical_querystring = params['request_parameters']
    canonical_headers = 'host:' + params['host'] + '\n' + 'x-amz-date:' + amzdate + '\n'
    signed_headers = 'host;x-amz-date'
    payload_hash = hashlib.sha256(params['payload']).hexdigest()
    canonical_request = params['method'] + '\n' + canonical_uri + '\n' + canonical_querystring + '\n' + canonical_headers + '\n' + signed_headers + '\n' + payload_hash

    algorithm = 'AWS4-HMAC-SHA256'
    credential_scope = datestamp + '/' + region + '/' + params['service'] + '/' + 'aws4_request'
    string_to_sign = algorithm + '\n' +  amzdate + '\n' +  credential_scope + '\n' +  hashlib.sha256(canonical_request).hexdigest()
    signing_key = getSignatureKey(params['secret_key'], datestamp, region, params['service'])

    # Sign the string_to_sign using the signing_key
    signature = hmac.new(signing_key, (string_to_sign).encode('utf-8'), hashlib.sha256).hexdigest()

    # Create authorization header and add to request headers
    authorization_header = algorithm + ' ' + 'Credential=' + params['access_key'] + '/' + credential_scope + ', ' +  'SignedHeaders=' + signed_headers + ', ' + 'Signature=' + signature
    headers = {'x-amz-date':amzdate, 'Authorization':authorization_header, 'user-agent': 'awesome api_caller'}

    return canonical_querystring, headers
