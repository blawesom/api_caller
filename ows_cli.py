import os, sys, argparse
from api_caller import call_api
from xml.etree import cElementTree
import xmltodict, json
from ConfigParser import ConfigParser


def call(service, call_arg):
    endpoint = os.environ.get('{}_ENDPOINT'.format(service.upper()))
    status_code, call_response = call_api('GET', endpoint, call_arg)
    response = xmltodict.parse(call_response)
    return status_code, response


def help(extend=False):
    conf=ConfigParser()
    conf.read('ows.cfg')
    print '\n\t---- OWS CLI v{} ----\n\tTo get help use the -h or --help argument'.format(conf.get('app', 'version'))
    if extend:
        print '\n\tExpected arguments are:\
                \n\t\tService: fcu, lbu, eim, osu...\
                \n\t\tAction: --Action=ExpectedAction \
                \n\t\tOptions: --OptionKey=OptionValue'
    print ''
    sys.exit(1)


if __name__ == '__main__':
    if sys.argv[1] in ['-h', '--help']:
        help(extend=True)
    else:
        try:
            service = sys.argv[1]
            arg_list = []
            for arg in sys.argv[2:]:
                if arg.startswith('--'):
                    arg_list.append(arg[2:])
            parsed_string = '&'.join(arg_list)
            # Action=MyAction&param1=value1&param2=value2&tags.keyn=valuen&tags.keym=valuem
            status_code, response = call(service, parsed_string)
        except Exception as e:
            print e
            help()

    print "\nCode: {}".format(status_code)
    print json.dumps(response)
