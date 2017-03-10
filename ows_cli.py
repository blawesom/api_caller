import os, sys, argparse
from api_caller import call_api
from xml.etree import cElementTree

"""
    You need to export to your environment:
    export FCU_ENDPOINT=fcu.eu-west-2.outscale.com
    export AWS_ACCESS_KEY_ID=XXXXXXXXXXXXXXXXXXXXX
    export AWS_SECRET_ACCESS_KEY=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
"""

def call(call_arg):
    parser = cElementTree.XMLParser(
                target=cElementTree.TreeBuilder(),
                encoding='UTF-8')
    fcu_endpoint = os.environ.get('FCU_ENDPOINT')

    status_code, call_response = call_api('GET', fcu_endpoint, call_arg)
    parser.feed(call_response)
    response = parser.close()
    return status_code, response


def args_to_string(dict_args):
    request = ''
    for arg in dict_args:
        joined = '='.join([arg, dict_args[arg]])
        request = '{}&{}'.format(request, joined)
    # Action=MyAction&param1=value1&param2=value2&tags.keyn=valuen&tags.keym=valuem
    return request[1:]


if __name__ == '__main__':
    print ''
    parser = argparse.ArgumentParser()
    args, ukargs = parser.parse_known_args()

    parsed = {}
    for i, arg in enumerate(ukargs):
        if arg.startswith('--'):
            parsed[arg[2:]] = ukargs[i+1]
        else:
            pass
            
    status_code, response = call(args_to_string(parsed))

    print "Code: {}".format(status_code)
    print "Request Id: {}".format(response.find('requestId').text)
    print "Data:"

    for child in response.getchildren():
         for item in child:
             print [(ite.tag, ite.text) for ite in item.getchildren()]
