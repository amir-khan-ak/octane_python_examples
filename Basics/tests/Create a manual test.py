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


#Declare the manual_tests resource
resource='manual_tests'

#Create a test in Octane
test_data = {"data":[{"name":"Manual test created from python",
                        "phase":{"id":"phase.test_manual.new",
                        "type":"phase"}}]}

tests = requests.post(url+'/api/shared_spaces/' + shared_space + '/workspaces/'+ workspace +'/'+resource,
                        data=json.dumps(test_data),
                        headers=ContentType,
                        cookies=cookie)

print('Creating Defect Status: ' + str(tests.status_code))
if tests.status_code == 201:
    print('Test with ID: ' + tests.json()['data'][0]['id'] + ' created successfully.')

# Adding steps to manual test
steps = '- SIMPLE STEP 1: Use Authenticationfunctions to Sign_in to ALM Octane. \n'\
        '- ? VERIFICAITON STEP 2: Verify sign_in returncode is 200. \n'\
        '- SIMPLE STEP 3: Use the cookie returned from the sign_in function in all future requests. \n'\
        '- SIMPLE STEP 4: Use the sign_out function in Authenticationfunction to sign_out using your cookie'

# Define the payload for the steps
payload = {"script": steps, "comment": "Excel Import Update", "revision_type": "Minor"}

# Define the resource for the test script to add steps - it contains the id of the created test in the code above
resource = 'tests/' + str(tests.json()['data'][0]['id']) + '/script'

#Request a PUT to update the test with steps
testscript = requests.put(
    url + '/api/shared_spaces/' + shared_space + '/workspaces/' + workspace + '/' + resource,
    data=json.dumps(payload),
    headers=ContentType,
    cookies=cookie)

print('Updating Test Status: ' + str(testscript.status_code))
if testscript.status_code == 200:
    print('Teststeps were added successfully.')

# Sign_out from ALM Octane
response_code = Auth.sign_out(url, cookie)
