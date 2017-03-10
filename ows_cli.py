import os, sys, argparse
from api_caller import call_api
from xml.etree import cElementTree

"""
    You need to export to your environment:
    export FCU_ENDPOINT=fcu.eu-west-2.outscale.com
    export LBU_ENDPOINT=lbu.eu-west-2.outscale.com
    export ICU_ENDPOINT=icu.eu-west-2.outscale.com
    export EIM_ENDPOINT=eim.eu-west-2.outscale.com
    export AWS_ACCESS_KEY_ID=XXXXXXXXXXXXXXXXXXXXX
    export AWS_SECRET_ACCESS_KEY=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
"""

def call(service, call_arg):
    parser = cElementTree.XMLParser(
                target=cElementTree.TreeBuilder(),
                encoding='UTF-8')
    endpoint = os.environ.get('{}_ENDPOINT'.format(service.upper()))
    status_code, call_response = call_api('GET', endpoint, call_arg)
    parser.feed(call_response)
    response = parser.close()
    return status_code, response


if __name__ == '__main__':
    print ''
    service = sys.argv[1]
    arg_list = []
    for arg in sys.argv[2:]:
        if arg.startswith('--'):
            arg_list.append(arg[2:])
    parsed_string = '&'.join(arg_list)
    # Action=MyAction&param1=value1&param2=value2&tags.keyn=valuen&tags.keym=valuem
    status_code, response = call(service, parsed_string)

    print "Code: {}".format(status_code)
    print "Request Id: {}".format(response.find('requestId').text)
    print "Data:"

    for child in response.getchildren():
         for item in child:
             print [(ite.tag, ite.text) for ite in item.getchildren()]
