# add_ec2_connector
Info : Python File adds the AWS EC2 connector into Qualys Asset View Connectors w.r.t details provided in "./AWS_EC2_CONNECTOR_INFO.csv" & "./config.txt".
Console output as well as debug_file.txt will have both success & failure logs.

#AWS_EC2_CONNECTOR_INFO.csv:
Info : csv files contains below attributes required for AWS connector
Script looks for AWS_CONNECTOR_INFO.csv in the directory the script runs from
> ARN,NAME,EXTID,REGION,MODULE

*EXTID must be an INT from 9-90 in length* Example: 98765456787654567821

*REGION must be single spaced list of regions or "ALL"*
Currently only ALL and single specified region work. Additonal support for multiple regions is being worked.
*Examples*
> ALL
> us-east-1


*MODULES must be an list of modules to activate for connector*
*Examples:*
> VM
> "VM PC"
> "VM PC SCA"

#Script configuration
*config.yml*
Provide script configuration information for API U/P, vulnerability severity ratings, and Qualys API URL
  username: "QualysUsername"
  password: "QualysPassword"

  apiURL: "Qualys API URL base (https:// - > .com/, no trailing '/') for your pod"
  Examples:
  >https://qualysapi.qualys.com
  >https://qualysapi.qg2.apps.qualys.com


#Script Requirements
This script is written in Python 2.7.x (X > 10)
This script requires the following PIP modules to run
Modules: sys, requests, datetime, os, time, yaml, json, csv, base64

Example Python module install
MAC/Linux "pip install requests"
Windows "python -m pip install requests"

Example Python yaml module install
MAC/Linux "pip install pyyaml"
Windows "python -m pip install pyyaml"


#Debug
Debug file for script run, located in ./debug folder with time/date stamp per line. To disable debug, comment out all lines containing "debug"
