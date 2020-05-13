# Using the basic authentication functions and define the whole package as Auth
import json
import requests
import Basics.Authentication.Authenticationfunctions as Auth

# ------ EXAMPLE How to use the sign_in and sign_out function
url = "https://almoctane-eur.saas.microfocus.com"
client_id = "Python_1wqe213qwe35tt34o97oz4o"
client_secret = "(1236123sad324324ZQ"
ContentType = {'Content-Type': 'application/json', 'ALM_OCTANE_TECH_PREVIEW': 'true'}

# Sign_in to ALM Octane and save cookie
response_code, cookie = Auth.sign_in(url, client_id,client_secret)

#Define ALM Octane shared_space and workspace
shared_space = '54432'
workspace = '4123'

#Read Defects using the cookie from the #Sign_in function
resource='defects'

#Create a defect in Octane
defect_data = {"data":[
                {"name":"MULTI_CREATION_01 - Defect created from python",
                 "description":"MULTI_CREATION_01 - This is a test defect created from python using REST API",
                "phase":{"id":"phase.defect.new", "type":"phase"}},
                {"name": "MULTI_CREATION_02 - Defect created from python",
                 "description": "MULTI_CREATION_02 - This is a test defect created from python using REST API",
                 "phase": {"id": "phase.defect.new", "type": "phase"}},
                {"name": "MULTI_CREATION_03 - Defect created from python",
                 "description": "MULTI_CREATION_03 - This is a test defect created from python using REST API",
                 "phase": {"id": "phase.defect.new", "type": "phase"}},

]}

defects = requests.post(url+'/api/shared_spaces/' + shared_space + '/workspaces/'+ workspace +'/'+resource,
                        data=json.dumps(defect_data),
                        headers=ContentType,
                        cookies=cookie)

print('Creating Defect Status: ' + str(defects.status_code))
if defects.status_code == 201:
    print('Defect 1 with ID: ' + defects.json()['data'][0]['id'] + ' created successfully.')
    print('Defect 2 with ID: ' + defects.json()['data'][1]['id'] + ' created successfully.')
    print('Defect 3 with ID: ' + defects.json()['data'][2]['id'] + ' created successfully.')

# Sign_out from ALM Octane
response_code = Auth.sign_out(url, cookie)
