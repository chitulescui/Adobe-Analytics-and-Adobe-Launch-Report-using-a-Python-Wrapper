# Adobe-Analytics-and-Adobe-Launch-Report-using-API
In order to track elements on a website using Adobe Launch we have to create a property containing Data elements and Rules and use them to retrieve the information which will be passed to Adobe Analytics.
Due to the fact that when we set-up a rule in Adobe Launch we can either store the information through adobe variables or through a custom code(usualy using javascript), we want to 
create a document with all those details to have a better overview about the implementation of the tracking code/rules in that Adobe Launch property.

Gaining access to the whole data we first have to create a project in Adobe Developer Console, to ensure the connection using JWT authentification method and then connect to Adobe Launch API via a Python Wrapper. 
The documentation about the Python Wrapper can be found here: https://github.com/pitchmuc/aepp/blob/main/docs/getting-started.md

* **First Step** : Create the configuration file to ensure the connectivity to **Launch and Analytics API**
* **Second Step** : Retrieve a JSON file containing whole data via **Python Wrapper**
* **Third Step**: Parse the data and look for the Rules`s **name/dataElements/props/events/customCod**e
* **Forth Step** : Extract all the information and compare it to a template (**SDR_OK.xlsl & BluePrint.py**)
* **Fifth Step**: : Create an xlsl document with the same structure as **Report Example.xlsx**
