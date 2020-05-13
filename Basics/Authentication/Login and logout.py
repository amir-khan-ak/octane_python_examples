# Required imports
import json
import requests

# ------ Login to Octane
# Define variables
url = "https://almoctane-eur.saas.microfocus.com"
client_id = "Python_Cli_wd3f4s228g0om25d"
client_secret = "(sd32634123324345W"
ContentType = {'Content-Type': 'application/json', 'ALM_OCTANE_TECH_PREVIEW': 'true'}

#Define resource and payload for sign in
resource = 'authentication/sign_in'
payload = {"client_id": client_id, "client_secret": client_secret}

#Send request and receive response (REST API)
resp = requests.post(url + '/' + resource,
                     data=json.dumps(payload),
                     headers=ContentType)

#SAVE Cookie and use in all subsequent requests
cookie = resp.cookies
print('Login: ' + str(resp.status_code))


# ------ Logout from Octane
#Define resource for sign out
resource = 'authentication/sign_out'

#Send request to sign out - important to sign out from the session, provide the cookie received at sign in
resp = requests.post(url + '/' + resource,
                     data=json.dumps(payload),
                     headers=ContentType,
                     cookies=cookie)

print('Logout: ' + str(resp.status_code))

