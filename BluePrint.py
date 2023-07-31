# -----Libraries imported-----

import launchpy
import json
import openpyxl
import pandas as pd
import aanalytics2 as api2
import time
import csv
from aanalytics2 import ingestion
from pandas import DataFrame
import re
import collections
from collections import OrderedDict
# -----Libraries imported----- End


# -----Adobe Launch configuration-----


login1.configure(
    org_id=my_org_id,
    tech_id=my_tech_id, 
    secret=my_secret,
    private_key=my_key_as_string,
    client_id=my_client_id,
    environment="prod",
    sandbox=my_sandbox
)
# -----Adobe Launch configuration----- End


# -----Adobe Launch API LOGIN-----
admin = launchpy.Admin()
myCid = admin.getCompanyId()
myProperties=admin.getProperties(admin.COMPANY_ID)
# -----Adobe Launch API LOGIN----- End

# -----Creating a list with all properties from Adobe Launch-----

myProps=[prop["attributes"]["name"] for prop in admin.properties]

# -----Creating a list with all properties from Adobe Launch----- End


# LIST WITH ALL PROPERTIES SAVED IN datanalystPROP
datanalystProp=[prop for prop in admin.properties if prop["attributes"]["name"]=="Blueprint-Consent"]
datanalyst=launchpy.Property(datanalystProp[0])
dataGetRules=datanalyst.getRules()
dataElements = datanalyst.getDataElements()
list_dataElements_names = [data["attributes"]["name"] for data in dataElements]
#LIST WITH ALL DATA ELEMENTS FROM A PROPERTY


datanalyst.getRuleComponents()
rules=datanalyst.getRules()


list_rule_names = [rule["attributes"]["name"] for rule in rules]
with open("rule_names.txt","w") as f:
    for rule_name in list_rule_names:
        f.write(f"{rule_name}\n")

rcs = datanalyst.getRuleComponents()
rcs_rule_name=[]
rcs_action=[]

rcs_rule_name=[]

dict_rcs_action={}
len(rcs)
for rc in rcs:
    if "::actions::set-variables" in rc["attributes"]["delegate_descriptor_id"]:
        rcs_action.append(rc)
        rcs_rule_name.append(rc["rule_name"])
#Create 2 lists for rcs_action and rcs_rule_name
# -----Separate customCode and trackerProperties-----
dict_custom_setup={}
index = 0
for i in range(len(rcs_action)):
    if "customSetup" in rcs_action[i]["attributes"]["settings"] and "trackerProperties" in rcs_action[i]["attributes"]["settings"]:
        string_mare = rcs_action[i]["attributes"]["settings"]
        # print(string_mare)
        pattern = re.compile(r'trackerProperties')
        matches = pattern.finditer(string_mare)
        for match in matches:
            index_inceput=match.span()[0]
        for j in range(len(string_mare)):
            string_aux=string_mare[:index_inceput-2]+"}"
        dict_rcs_action[index]="{"+string_mare[index_inceput-1:]
        dict_custom_setup[index]=string_aux
        index+=1
    else:
        dict_rcs_action[index] = launchpy.extractSettings(rcs_action[i])
        index += 1
# -----Separate customCode and trackerProperties----- End



dict_rcs_rule_name={}
# dict_rcs_action[14]
index = 0
for i in rcs_rule_name:
    dict_rcs_rule_name[index] = i
    # print(index, " ", i)
    index += 1

big_dict={} #Create big dictionary with "rule name" and "eVars"


for i,j in dict_rcs_rule_name.items():
    for g,k in dict_rcs_action.items():
        print(g,k)
        if i==g:
            big_dict[i]={"Rule Name":j,"eVars":k}
# print(big_dict)


dict_rcs_rule_name


rcs_action = [rc for rc in rcs if "::actions::set-variables" in rc["attributes"]["delegate_descriptor_id"]]
rcs_condition = [rc for rc in rcs if "::conditions::" in rc["attributes"]["delegate_descriptor_id"]]
rcs_events = [rc for rc in rcs if "::events::" in rc["attributes"]["delegate_descriptor_id"]]

index=0
action0 = launchpy.extractSettings(rcs_action[0])
action0



counter=-1
counter2=0
dict_aux={}
idx3=0
for idx,value in big_dict.items():
    counter+=1
    # print(value["eVars"])
    #we transform trackerProperties from str to dict
    aux_var=json.loads(value["eVars"])
    print(aux_var.items())
    #we search for every value and extract
    #values : "eVars" , "props" , "events" , "server" , "pageURL", "pageName", "campaign" , "referrer"
    for idx2,value2 in aux_var.items():
        print(counter)
        if 'eVars' in aux_var[idx2].keys():
            for idx3 in range(len(aux_var[idx2]["eVars"])):
                if counter not in dict_aux.keys():
                    dict_aux[counter]={aux_var[idx2]["eVars"][idx3]["name"]:aux_var[idx2]["eVars"][idx3]["value"]}
                else:
                    dict_aux[counter][aux_var[idx2]["eVars"][idx3]["name"]]=aux_var[idx2]["eVars"][idx3]["value"]

        if 'props' in aux_var[idx2].keys():
            for idx3 in range(len(aux_var[idx2]["props"])):
                if counter not in dict_aux.keys():
                    dict_aux[counter]={aux_var[idx2]["props"][idx3]["name"]:aux_var[idx2]["props"][idx3]["value"]}
                else:
                    dict_aux[counter][aux_var[idx2]["props"][idx3]["name"]]=aux_var[idx2]["props"][idx3]["value"]

        if 'events' in aux_var[idx2].keys():
            for idx3 in range(len(aux_var[idx2]["events"])):
                if counter not in dict_aux.keys():
                    dict_aux[counter]={"events":"anything"}
                else:
                    dict_aux[counter]["events"] = aux_var[idx2]["events"][idx3]["name"]
        if "pageURL" in aux_var[idx2].keys():
            for idx3 in range(len(aux_var[idx2]["pageURL"])):
                if counter not in dict_aux.keys():
                    dict_aux[counter] = {"pageURL": "anything"}
                else:
                    dict_aux[counter]["pageURL"] = aux_var[idx2]["pageURL"]

        if "campaign" in aux_var[idx2].keys():
            for idx3 in aux_var[idx2]["campaign"].keys():
                if counter not in dict_aux.keys():
                    dict_aux[counter] = {"campaign": "anything"}
                else:
                    dict_aux[counter]["campaign"] = aux_var[idx2]["campaign"]["value"]

        if "pageName" in aux_var[idx2].keys():
            for idx3 in range(len(aux_var[idx2]["pageName"])):
                if counter not in dict_aux.keys():
                    dict_aux[counter] = {"pageName": "anything"}
                else:
                    dict_aux[counter]["pageName"] = aux_var[idx2]["pageName"]

        if "referrer" in aux_var[idx2].keys():
            for idx3 in range(len(aux_var[idx2]["referrer"])):
                if counter not in dict_aux.keys():
                    dict_aux[counter] = {"referrer": "anything"}
                else:
                    dict_aux[counter]["referrer"] = aux_var[idx2]["referrer"]
        if "server" in aux_var[idx2].keys():
            for idx3 in range(len(aux_var[idx2]["server"])):
                if counter not in dict_aux.keys():
                    dict_aux[counter] = {"server": "anything"}
                else:
                    dict_aux[counter]["server"] = aux_var[idx2]["server"]
        if "channel" in aux_var[idx2].keys():
            for idx3 in range(len(aux_var[idx2]["channel"])):
                if counter not in dict_aux.keys():
                    dict_aux[counter] = {"channel": "anything"}
                else:
                    dict_aux[counter]["channel"] = aux_var[idx2]["channel"]
dict_final_blueprint={}
for cheie1,valoare1 in big_dict.items():
    for cheie1,valoare2 in dict_aux.items():
        for cheie2 in valoare2.keys():
            dict_final_blueprint[cheie1] = {"Rule Name": big_dict[cheie1]["Rule Name"], "Details": dict_aux[cheie1]}