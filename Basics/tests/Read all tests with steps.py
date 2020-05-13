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

#Read manual_tests using the cookie from the #Sign_in function
resource='manual_tests'

#Storing the response into tests variable
manual_tests = requests.get(url+'/api/shared_spaces/' + shared_space + '/workspaces/'+ workspace +'/'+resource,
                    headers=ContentType,
                     cookies=cookie)

print('Getting Manual Tests Status: ' + str(manual_tests.status_code))

#Storing the JSON in response into manual_tests_data
manual_tests_data = manual_tests.json()

#Get the attribute 'total_count'
total_count = manual_tests_data['total_count']

#Get the attribute 'data' in to manual_tests_list
manual_tests_list = manual_tests_data['data']

print('Total Defects: ' + str(total_count))

#iterate through all manual_tests within manual_tests_list
for manual_test in manual_tests_list:
    #Printing defect fields
    print('Test Name: ' + manual_test['name'] + ', ID: ' + manual_test['id'] + ', Phase: ' + manual_test['phase']['id']
          + ', Total Steps: ' + str(manual_test['steps_num']))

    # Reading the testscripts for the test object
    resource = 'tests/' + manual_test['id'] + '/script'
    testscript = requests.get(
        url + '/api/shared_spaces/' + shared_space + '/workspaces/' + workspace + '/' + resource,
        headers=ContentType,
        cookies=cookie)

    print('Getting testscript: ' + str(testscript.status_code))
    testscript_data = testscript.json()
    testscript_steps = testscript_data['script']
    print('Testscript: ' + str(testscript_steps))

    #Split test steps by \n
    steps = testscript_steps.split('\n')
    for step in steps:
        #Print steps for the selected test
        print('Step: ' + step)

# Sign_out from ALM Octane
response_code = Auth.sign_out(url, cookie)
