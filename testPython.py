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
from BluePrint import dict_final_blueprint
# -----Libraries imported----- End


# -----Adobe Launch configuration-----

api2.configure(
    org_id=my_org_id,
    tech_id=my_tech_id, 
    secret=my_secret,
    private_key=my_key_as_string,
    client_id=my_client_id,
    environment="prod",
    sandbox=my_sandbox
)

login1.configure(
    org_id=my_org_id,
    tech_id=my_tech_id, 
    secret=my_secret,
    private_key=my_key_as_string,
    client_id=my_client_id,
    environment="prod",
    sandbox=my_sandbox
)
# -----Adobe Analytics configuration----- End


# -----Adobe Analytics API LOGIN-----
login = api2.Login()
cids = login.getCompanyId()
cid = "onemar1"
mycompany = api2.Analytics(cid)
ags=api2.Analytics(cid)
# -----Adobe Analytics API LOGIN----- End


# -----Retrieving All evars and events from Adobe Analytics-----
list_metrics=[]

Metrics=ags.getMetrics(rsid="omazeudigitallabprod") #rsid of the report suite
Metrics_dict=Metrics.to_dict()

for i in Metrics_dict["id"].values():
    if "evar" in i:
        list_metrics.append(i.replace("metrics/","").replace("instances","").replace("v","V"))
    if "event" in i:
        list_metrics.append(i.replace("metrics/",""))
# -----Retrieving All evars and events from Adobe Analytics----- End



# -----Adobe Launch API LOGIN-----
admin = launchpy.Admin()
myCid = admin.getCompanyId()
myProperties=admin.getProperties(admin.COMPANY_ID)
# -----Adobe Launch API LOGIN----- End

# -----Creating a list with all properties from Adobe Launch-----

myProps=[prop["attributes"]["name"] for prop in admin.properties]

# -----Creating a list with all properties from Adobe Launch----- End


# LIST WITH ALL PROPERTIES SAVED IN datanalystPROP
datanalystProp=[prop for prop in admin.properties if prop["attributes"]["name"]=="Allianz UK"]
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


#----- Creating dict_final-----
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
dict_final={}
for cheie1,valoare1 in big_dict.items():
for cheie1,valoare2 in dict_aux.items():
    for cheie2 in valoare2.keys():
        dict_final[cheie1] = {"Rule Name": big_dict[cheie1]["Rule Name"], "Details": dict_aux[cheie1]}
#----- Creating dict_final-----End







# -----Appending custom code to the main dictionary------
pattern_main = re.compile(r's.eVar\d+ = [^;]+')
for i,j in dict_custom_setup.items():
    matches_main = re.findall(pattern_main, j)
    if matches_main:
       for match_main in matches_main:
           equal_index = match_main.find("=")
           # if "Details" in dict_final[i]:
                dict_final[i]['Details'][match_main[:equal_index].replace("s.","").strip()] = match_main[equal_index:].replace("_satellite.getVar","").replace("(", "").replace(")", "").replace("=", "").replace('"', '').strip()
# -----Appending custom code to the main dictionary------ End



# -----Read the SDR file-----
    excel_data = pd.read_excel("SDR_OK.xlsx")
    dict = excel_data.to_dict()
# -----Read the SDR file----- End

# -----Add "Comments" Key to dict_final-----
dict_comments={}
for i in range(len(dict_final)+1):
    if i in dict_final.keys():
        for v,a in dict["Evar #"].items():
            for g,j in dict_final[i]["Details"].items():
                if str(g)==str(a).strip():
                    if str(j).replace("%","")!=str(dict["Data Layer"][v]):
                        if "comments" not in dict_final[i].keys():
                            # dict_final[i]["comments"] = {"not equal values between"+str(j):str(dict["Data Layer"][v])+"(SDR VALUE)"}
                            dict_final[i]["comments"] = {"not equal values between" + str(j) : str(dict["Data Layer"][v]) + "(SDR VALUE)"}
                        else:
                            # dict_final[i]["comments"]["not equal values between"+str(j)]=str(dict["Data Layer"][v])+"(SDR VALUE)"
                            dict_final[i]["comments"]["not equal values between" + str(j)] =  str(dict["Data Layer"][v]) + "(SDR VALUE)"
                    elif "event" in str(j) and str(j)==str(dict["Data Layer"][v]):
                        if "comments" not in dict_final[i].keys():
                            dict[i]["comments"]={"not equal values between"+str(j):str(dict["Data Layer"][v])+"(SDR VALUE)"}
                        else:
                            dict[i]["comments"]["not equal values between" + str(j)] = str(dict["Data Layer"][v]) + "(SDR VALUE)"
                    else:
                        if "comments" not in dict_final[i].keys():
                            dict_final[i]["comments"]={str(g):"All fine"}
                        else:
                            dict_final[i]["comments"][str(g)]="All fine"
# -----Add "Comments" Key to dict_final----- End

set_common_analytics_launch_evars=set()
list_events_analytics=[]
for eVar_or_event in list_metrics:
    # print(eVar_or_event)
    for value_dict_final in dict_final.values():
        for evars in value_dict_final["Details"].keys():
            if evars == eVar_or_event:
                set_common_analytics_launch_evars.add(evars)
            if evars=="events":
                if value_dict_final["Details"]["events"]==eVar_or_event:
                    list_events_analytics.append(value_dict_final["Details"]["events"])

# -----List all common events AA and AL-----
list_events_analytics
# -----All events from Analytics-----
list_events_analytics_all=[]
list_events_analytics_all_additional=[]
for i in list_metrics:
    if "event" in i and i.isalpha()==False:
        list_events_analytics_all_additional.append(int(i.replace("event","")))
list_events_analytics_all_additional.sort()
for i in list_events_analytics_all_additional:
    list_events_analytics_all.append("event"+str(i))
# -----All events from Analytics----- End



# -----List all common eVars AA and AL-----
list_evars_analytics=[]
list_evars_analytics_additional=[]
for i in set_common_analytics_launch_evars:
    list_evars_analytics_additional.append(int(i.replace("eVar","")))
list_evars_analytics_additional.sort()
for i in list_evars_analytics_additional:
    list_evars_analytics.append("eVar"+str(i))
# -----List all common eVars AA and AL----- End



# -----All eVars from Analytics-----
list_evars_analytics_all=[]
list_evars_analytics_all_additional=[]
for i in list_metrics:
    if "eVar" in i:
        list_evars_analytics_all_additional.append(int(i.replace("eVar","")))
list_evars_analytics_all_additional.sort()
for i in list_evars_analytics_all_additional:
    list_evars_analytics_all.append("eVar"+str(i))
# -----All eVars from Analytics----- End

# -----List with all eVars and events used in Launch and enabled in Analytics-----
list_common_events_and_evars=[]
for i in list_evars_analytics:
    list_common_events_and_evars.append(i)
for j in list_events_analytics:
    list_common_events_and_evars.append(j)
# -----List with all eVars and events used in Launch and enabled in Analytics----- End


# -----Add "SDR" Key to dict_final-----
for i in range(len(dict_final)+1):
    if i in dict_final.keys():
        for kapa2,valo2 in dict["Evar #"].items():
            print(valo2)
            for kapa,valo in dict_final[i]["Details"].items():
                print(kapa)
                if str(kapa)==str(valo2).strip():
                    if "SDR" not in dict_final[i].keys():
                        dict_final[i]["SDR"] = {str(kapa):str(dict["Data Layer"][kapa2])}
                    else:
                        dict_final[i]["SDR"][str(kapa)] = str(dict["Data Layer"][kapa2])
                elif str(kapa)=="events" and dict_final[i]["Details"][kapa]==str(valo2).strip():
                    if "SDR" not in dict_final[i].keys():
                        dict_final[i]["SDR"]= {str(dict_final[i]["Details"][kapa]):str(valo2.strip())}
                    else:
                        dict_final[i]["SDR"][str(dict_final[i]["Details"][kapa])]= str(valo2.strip())
# -----Add "SDR" Key to dict_final----- End


# -----eVars and events enabled in Analytics-----
for i in range(len(dict_final)+1):
    if i in dict_final.keys():
        for kapa3 in list_common_events_and_evars:
            for kapa, valo in dict_final[i]["Details"].items():
                if str(kapa)==str(kapa3) and str(kapa)!="events":
                    print(kapa,kapa3)
                    if "Analytics" not in dict_final[i].keys():
                        dict_final[i]["Analytics"] = {str(kapa): "Enabled in Analytics"}
                    else:
                        dict_final[i]["Analytics"][str(kapa)] = "Enabled in Analytics"
                elif str(dict_final[i]["Details"][kapa])==str(kapa3) and str(kapa)=="events":
                    if "Analytics" not in dict_final[i].keys():
                        dict_final[i]["Analytics"] = {str(dict_final[i]["Details"][kapa]): "Enabled in Analytics"}
                    else:
                        dict_final[i]["Analytics"][str(dict_final[i]["Details"][kapa])] = "Enabled in Analytics"
                elif  str(kapa)!=str(kapa3) and str(kapa)!="events":
                    if "Analytics" not in dict_final[i].keys():
                        dict_final[i]["Analytics"] = {str(kapa): "Not Enabled in Analytics"}
                    elif str(kapa) in dict_final[i]["Analytics"].keys():
                        pass
                    else:
                        dict_final[i]["Analytics"][str(kapa)] = "Not Enabled in Analytics"
                elif str(dict_final[i]["Details"][kapa])!= str(kapa3) and str(kapa) == "events":
                    if "Analytics" not in dict_final[i].keys():
                        dict_final[i]["Analytics"] = {str(dict_final[i]["Details"][kapa]): "Not Enabled in Analytics"}
                    elif str(dict_final[i]["Details"][kapa]) in dict_final[i]["Analytics"].keys():
                        pass
                    else:
                        dict_final[i]["Analytics"][str(dict_final[i]["Details"][kapa])] = "Not Enabled in Analytics"
# -----eVars and events enabled in Analytics-----End


# -----Comparation to blueprint for rules------
for i in range(len(dict_final)+1):
    # dict_final[i]["Details"].items():
    for j in range(len(dict_final_blueprint)):
        if i in dict_final.keys():
            if dict_final[i]["Rule Name"]==dict_final_blueprint[j]["Rule Name"] or  str(dict_final_blueprint[j]["Rule Name"]) in str(dict_final[i]["Rule Name"]).replace(" ",""):
                # print("avem aceleasi reguli ", dict_final_blueprint[j]["Rule Name"])
                if "Blue Print Rule" not in dict_final[i].keys():
                    # dict_final[i]["comments"] = {"not equal values between"+str(j):str(dict["Data Layer"][v])+"(SDR VALUE)"}
                    dict_final[i]["Blue Print Rule"] = {dict_final[i]["Rule Name"]:"Rule present in BluePrint"}
                    # print(dict_final[i]["Blue Print"]["In accordance to Blue Print" + str(value_final)])
                else:
                #     # dict_final[i]["comments"]["not equal values between"+str(j)]=str(dict["Data Layer"][v])+"(SDR VALUE)"
                    dict_final[i]["Blue Print Rule"][dict_final[i]["Rule Name"]]="Rule present in BluePrint"
            else:
                if "Blue Print Rule" not in dict_final[i].keys():
                    # dict_final[i]["comments"] = {"not equal values between"+str(j):str(dict["Data Layer"][v])+"(SDR VALUE)"}
                    dict_final[i]["Blue Print Rule"] = {dict_final[i]["Rule Name"]: "Rule Not present in BluePrint"}
                  # print(dict_final[i]["Blue Print"]["In accordance to Blue Print" + str(value_final)])
        else:
            continue
# -----Comparation to blueprint for rules------End

# -----Comparation to blueprint for eVars------














# -----Creating the final excel file-----
list_rules=[]
list_details=[]
list_comments=[]
list_sdr=[]
list_analytics=[]
list_blueprint_rules=[]


for i in dict_final.keys():
    list_rules.append(dict_final[i]["Rule Name"])
    # list_comments.append(dict_final[i].get("comments") or " ")
    # count=0
    for kei,valu in dict_final[i]["Details"].items():
        list_details.append(str(kei).replace("'","")+" - "+str(valu).replace("%",""))
    for kei2,valu2 in dict_final[i].get("comments",{}).items():
        list_comments.append(str(kei2).replace("'","")+" - "+str(valu2).replace("%",""))
    for kei3, valu3 in dict_final[i].get("SDR",{}).items():
        list_sdr.append(str(kei3).replace("'","")+" - "+str(valu3).replace("%",""))
    for kei4, valu4 in dict_final[i].get("Analytics",{}).items():
        list_analytics.append(str(kei4).replace("'","")+" - "+str(valu4).replace("%",""))
    for kei5, valu5 in dict_final[i].get("Blue Print Rule",{}).items():
        list_blueprint_rules.append(str(kei5).replace("'","")+" - "+str(valu5).replace("%",""))
    max_size=max(len(list_details),len(list_rules),len(list_comments),len(list_sdr),len(list_analytics),len(list_blueprint_rules))

    list_rules+=([" "]*(max_size-len(list_rules)))
    list_details+=([" "]*(max_size-len(list_details)))
    list_comments+=([" "]*(max_size-len(list_comments)))
    list_sdr+=([" "]*(max_size-len(list_sdr)))
    list_analytics+=([" "])*(max_size-len(list_analytics))
    list_blueprint_rules+=([" "])*(max_size-len(list_blueprint_rules))

df = DataFrame({"Rule Name":list_rules,"Details":list_details,"SDR":list_sdr,"Analytics":list_analytics,"Comments":list_comments,"Blue Print":list_blueprint_rules})


df.to_excel('BluePrint-allianz-nebun2.xlsx', sheet_name='sheet1', index=False)

# -----Creating the final excel file----- End


