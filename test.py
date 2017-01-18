import os
from api_caller import call_api
from xml.etree import cElementTree

"""
    You need to export to your environment:
    export FCU_ENDPOINT=fcu.eu-west-2.outscale.com
    export AWS_ACCESS_KEY_ID=XXXXXXXXXXXXXXXXXXXXX
    export AWS_SECRET_ACCESS_KEY=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
"""
fcu_endpoint = os.environ.get('FCU_ENDPOINT')

# GET test
status_code, call_response = call_api('GET', fcu_endpoint, 'Action=DescribeInstances')

parser = cElementTree.XMLParser(
            target=cElementTree.TreeBuilder(),
            encoding='UTF-8')
parser.feed(call_response)
root = parser.close()

print "Code: {}".format(status_code)
print "Request Id: {}".format(root.find('requestId').text)

# for child in root.getchildren():
#      for item in child:
#          print [(ite.tag, ite.text) for ite in item.getchildren()]
