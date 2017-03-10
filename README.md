# Description
This is a low level API handler designed to addresse Outscale APIs, based of information found on the public API documentation:
- http://docs.outscale.com/

# Setup
As for the classic AWS CLI, you need to export the endpoints for the region you target. Access Key and Secret Key are also needed.

In your shell, export to your environment:
- export FCU_ENDPOINT=fcu.eu-west-2.outscale.com
- export AWS_ACCESS_KEY_ID=XXXXXXXXXXXXXXXXXXXXX
- export AWS_SECRET_ACCESS_KEY=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

# Examples
For a DescribeInstances:
- python ows_cli.py fcu --Action=DescribeInstances

For a DescribeSecurityGroups with filter:
- python ows_cli.py fcu --Action=DescribeSecurityGroups --Filter.1.Name vpc-id --Filter.1.Value vpc-x54x4f0x

For a RunInstance:
- python ows_cli.py eim --Action=ListUsers

# ToDo
*Package to be called directly as:*
- ows fcu --Action=ActionToExecute
