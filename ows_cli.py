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


if __name__ == '__main__':
    print ''
    arg_list = []
    for arg in sys.argv[:1]
        if arg startswith('--'):
            arg_list.append(arg[2:])
    parsed_string = '&'.joint(arg_list)
    # Action=MyAction&param1=value1&param2=value2&tags.keyn=valuen&tags.keym=valuem

    status_code, response = call(parsed_string)

    print "Code: {}".format(status_code)
    print "Request Id: {}".format(response.find('requestId').text)
    print "Data:"

    for child in response.getchildren():
         for item in child:
             print [(ite.tag, ite.text) for ite in item.getchildren()]
