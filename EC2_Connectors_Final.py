
#
# Author: Sean Nicholson
# Purpose: Automate the adding of EC2 connectors via the Qualys API
# version: 1.0.0
# date: 11.20.2018
#
#
#

import sys, requests, datetime, os, time, yaml, json, csv, base64

def config():
    with open('config.yml', 'r') as config_settings:
        config_info = yaml.load(config_settings, Loader=yaml.SafeLoader)
        username = str(config_info['defaults']['username']).rstrip()
        password = str(config_info['defaults']['password']).rstrip()
        URL = str(config_info['defaults']['apiURL']).rstrip()
        cloudview = str(config_info['defaults']['cloudview']).rstrip()
        if username == '' or password == '' or URL == '':
            print ("Config information in ./config.yml not configured correctly. Exiting...")
            sys.exit(1)
    return username, password, URL, cloudview

def Post_Call(username,password,URL,data_connector):

    usrPass = str(username)+':'+str(password)
    usrPassBytes = bytes(usrPass, "utf-8")
    b64Val = base64.b64encode(usrPassBytes).decode("utf-8")
    headers = {
        'Accept': '*/*',
        'content-type': 'text/xml',
        'X-Requested-With': 'curl',
        'Authorization': "Basic %s" % b64Val

    }

    r = requests.post(URL, data=data_connector, headers=headers)
    return r.raise_for_status()


def Add_AWS_EC2_Connector():
    username, password, URL, cloudview = config()
    URL = URL + "/qps/rest/2.0/create/am/awsassetdataconnector"

    print ('------------------------------AWS Connectors--------------------------------')
    if not os.path.exists("debug"):
        os.makedirs("debug")
    debug_file_name = "debug/debug_file"+ time.strftime("%Y%m%d-%H%M%S") + ".txt"
    debug_file = open(debug_file_name, "w")
    debug_file.write('------------------------------AWS Connectors--------------------------------' + '\n')
    with open('AWS_EC2_CONNECTOR_INFO.csv', 'rt') as f:
        reader = csv.DictReader(f)
        a = list(reader)
        f.close()
    counter=0
    for i in a:
        counter += 1

        ARN = i['ARN']
        EXT = i['EXTID']
        NAME = i['NAME']
        MODULE = i['MODULE']
        REGION = i['REGION']
        print (str(counter) + ' : AWS Connector')
        debug_file.write(str(counter) + ' : AWS Connector' + '\n')
        print ('---' + 'ARN : ' + str(ARN))
        print ('---' + 'EXT : ' + str(EXT))
        #print '---' + 'DESC : ' + str(DESC)
        print ('---' + 'NAME : ' + str(NAME))
        print ('---' + 'REGION : ' + str(REGION))
        print ('---' + 'MODULE : ' + str(MODULE))
        debug_file.write('---' + 'ARN : ' + str(ARN) + '\n')
        debug_file.write('---' + 'EXT : ' + str(EXT) + '\n')
        debug_file.write('---' + 'NAME : ' + str(NAME) + '\n')
        debug_file.write('---' + 'REGION : ' + str(REGION) + '\n')
        debug_file.write('---' + 'MODULE : ' + str(MODULE) + '\n')

        module_list = i['MODULE'].split()
        activate_module = ""
        region_list = ""
        activate_region = ""
        for m in module_list:
            activate_module += "<ActivationModule>{0}</ActivationModule>".format(str(m))

        if i['REGION'] != "ALL":
            region_list = i['REGION'].split()
            for r in region_list:
                activate_region += "<AwsEndpointSimple><regionCode>{0}</regionCode></AwsEndpointSimple>".format(str(r))
            xml = "<?xml version=\"1.0\" encoding=\"UTF-8\"?><ServiceRequest><data><AwsAssetDataConnector><name>{0}</name><arn>{1}</arn><externalId>{2}</externalId><endpoints><add>{3}</add></endpoints><disabled>false</disabled><activation><set>{4}</set></activation><useForCloudView>{5}</useForCloudView></AwsAssetDataConnector></data></ServiceRequest>".format(i['NAME'],i['ARN'],i['EXTID'],activate_region,activate_module,cloudview)
        else:
            xml = "<?xml version=\"1.0\" encoding=\"UTF-8\"?><ServiceRequest><data><AwsAssetDataConnector><name>{0}</name><arn>{1}</arn><externalId>{2}</externalId><disabled>false</disabled><allRegions>true</allRegions><activation><set>{3}</set></activation><useForCloudView>{4}</useForCloudView></AwsAssetDataConnector></data></ServiceRequest>".format(i['NAME'],i['ARN'],i['EXTID'],activate_module,cloudview)

        try:
            Post_Call(username, password, URL, xml)
            print (str(counter) + ' : Connector Added Successfully')
            print ('-------------------------------------------------------------')
            debug_file.write(str(counter) + ' : Connector Added Successfully' + '\n')

        except requests.exceptions.HTTPError as e:  # This is the correct syntax
            print (str(counter) + ' : Failed to Add AWS Connector')
            print (e)
            print ('-------------------------------------------------------------')
            debug_file.write(str(counter) + ' : Failed to Add AWS Connector' + '\n')
            debug_file.write(str(e) + '\n')

    debug_file.close()

Add_AWS_EC2_Connector()
