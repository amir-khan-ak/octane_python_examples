# Required imports
import json
import requests


def sign_in(url, client_id, client_secret):
    resource = 'authentication/sign_in'
    payload = {"client_id": client_id, "client_secret": client_secret}
    ContentType = {'Content-Type': 'application/json', 'ALM_OCTANE_TECH_PREVIEW': 'true'}

    # Send request and receive response (REST API)
    resp = requests.post(url + '/' + resource,
                         data=json.dumps(payload),
                         headers=ContentType)

    # SAVE Cookie and use in all subsequent requests
    cookie = resp.cookies
    print('Login to ALM Octane response code: ' + str(resp.status_code))
    return resp.status_code, cookie


def sign_out(url, cookie):
    resource = 'authentication/sign_out'
    ContentType = {'Content-Type': 'application/json', 'ALM_OCTANE_TECH_PREVIEW': 'true'}

    # Send request to sign out - important to sign out from the session, provide the cookie received at sign in
    resp = requests.post(url + '/' + resource,
                         headers=ContentType,
                         cookies=cookie)

    print('Logout to ALM Octane response code: ' + str(resp.status_code))
    return resp.status_code


# ------ EXAMPLE How to use the sign_in and sign_out function
# ------ REMOVE (code below) when using the authentication functions
url = "https://almoctane-eur.saas.microfocus.com"
client_id = "Python_1wqe213qwe35tt34o97oz4o"
client_secret = "(1236123sad324324ZQ"

response_code, cookie = sign_in(url, client_id, client_secret)
print("Call to sign_in to ALM Octane response code: " + str(response_code))

response_code = sign_out(url, cookie)
print("Call to sign_out to ALM Octane response code: " + str(response_code))

# ------ REMOVE (code above) when using the authentication functions
