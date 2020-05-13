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
defectid = '85001'
resource='defects' + '/' + defectid

#Delete a defect by ID in Octane
defects = requests.delete(url+'/api/shared_spaces/' + shared_space + '/workspaces/'+ workspace +'/'+resource,
                        headers=ContentType,
                        cookies=cookie)

print('Deleting Defect Status: ' + str(defects.status_code))
if defects.status_code == 200:
    print('Defect deleted successfully.')

# Sign_out from ALM Octane
response_code = Auth.sign_out(url, cookie)
