# Using the basic authentication functions and define the whole package as Auth
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

#Storing the response into defects variable
defects = requests.get(url+'/api/shared_spaces/' + shared_space + '/workspaces/'+ workspace +'/'+resource,
                    headers=ContentType,
                     cookies=cookie)

print('Getting Defects Status: ' + str(defects.status_code))

#Storing the JSON in response into defect_data
defects_data = defects.json()

#Get the attribute 'total_count'
total_count = defects_data['total_count']

#Get the attribute 'data' in to defect_list
defect_list = defects_data['data']

print('Total Defects: ' + str(total_count))

#iterate through all defects within defect_list
for defect in defect_list:
    #Printing defect fields
    print('Defect Summary: ' + defect['name'] + ', ID: ' + defect['id'] + ', Phase: ' + defect['phase']['id'])


# Sign_out from ALM Octane
response_code = Auth.sign_out(url, cookie)
