from flask import request
from flask import Flask
import requests
# Required imports
import json
import requests

FROM_PHASE = 'pjmr2nn6n981vtqw6q8lo2ng0'
TO_PHASE = '6d095vxxgej6gt601qqky2epr'

app = Flask(__name__)


@app.route('/defect_risk', methods=['POST'])
def defect_risk():
    if request.args.get('test') is None:
        server_url = request.json['server_url']
        event_type = request.json['event_type']
        sharedspace_id = str(request.json['sharedspace_id'])
        workspace_id = str(request.json['workspace_id'])
        username_id = str(request.json['username']['id'])
        username_mail = request.json['username']['email']
        json_data = request.json['data']
        print("******************************************")
        print(str(json_data))
        for dataset in json_data:
            print("******************************************")
            print("DATASET: " + str(dataset))
            print("******************************************")
            print("ENTITY: " + str(dataset['entity']))
            type = dataset['entity']['type']
            id = str(dataset['entity']['id'])
            # risk = dataset['entity']['risk_udf']
            name = dataset['entity']['name']
            priority = dataset['entity']['priority']
            severity = dataset['entity']['severity']
            # phases = dataset['entity']['phase']
            print("******************************************")
            # print("PHASES: " + str(phases))
            changes = dataset['changes']
            print("******************************************")
            print("CHANGES: " + str(dataset['changes']))
        print("******************************************")
        print("Server: " + server_url)
        print("event_type: " + event_type)
        print("sharedspace_id: " + sharedspace_id)
        print("workspace_id: " + workspace_id)
        print("username_id: " + username_id)
        print("username_mail: " + username_mail)
        print("type: " + type)
        print("defect id: " + id)
        print("name: " + name)
        print("priority: " + priority['id'])
        print("severity: " + severity['id'])
        # print("Risk: " + risk)
        print("******************************************")
        CHANGES = dataset['changes']
        # print(str(hasattr(CHANGES, 'phase')))
        if 'severity' in CHANGES:
            print("CHANGE severity")
            new = CHANGES['severity']['newValue']
            update_risk(id, priority, new, sharedspace_id, workspace_id)
        else:
            print('severity not changed')
        if 'priority' in CHANGES:
            print("CHANGE priority")
            new = CHANGES['priority']['newValue']
            update_risk(id, new, severity, sharedspace_id, workspace_id)
        else:
            print('priority not changed')
    else:
        print("Connection successful: " + str(request.args.get('test')))
    return 'Connection successful'


def update_risk(defect_id, priority, severity, space, workspace):
    # Required import
    if severity is None:
        if priority is None:
            defect_risk = "Unknown"
        elif priority['id'] == 'list_node.priority.urgent':
            defect_risk = "High"
        elif priority['id'] == 'list_node.priority.very_high':
            defect_risk = "High"
        elif priority['id'] == 'list_node.priority.high':
            defect_risk = "High"
        elif priority['id'] == 'list_node.priority.medium':
            defect_risk = "Medium"
        elif priority['id'] == 'list_node.priority.low':
            defect_risk = "Low"

    elif severity['id'] == 'list_node.severity.urgent':
        if priority is None:
            defect_risk = "Very High (Priority Unknown)"
        elif priority['id'] == 'list_node.priority.urgent':
            defect_risk = "Critical"
        elif priority['id'] == 'list_node.priority.very_high':
            defect_risk = "Critical"
        elif priority['id'] == 'list_node.priority.high':
            defect_risk = "Very High"
        elif priority['id'] == 'list_node.priority.medium':
            defect_risk = "High"
        elif priority['id'] == 'list_node.priority.low':
            defect_risk = "Medium"

    elif severity['id'] == 'list_node.severity.very_high':
        if priority is None:
            defect_risk = "Very High (Priority Unknown)"
        elif priority['id'] == 'list_node.priority.urgent':
            defect_risk = "Very High"
        elif priority['id'] == 'list_node.priority.very_high':
            defect_risk = "Very High"
        elif priority['id'] == 'list_node.priority.high':
            defect_risk = "High"
        elif priority['id'] == 'list_node.priority.medium':
            defect_risk = "High"
        elif priority['id'] == 'list_node.priority.low':
            defect_risk = "Medium"

    elif severity['id'] == 'list_node.severity.high':
        if priority is None:
            defect_risk = "High (Priority Unknown)"
        elif priority['id'] == 'list_node.priority.urgent':
            defect_risk = "Very High"
        elif priority['id'] == 'list_node.priority.very_high':
            defect_risk = "Very High"
        elif priority['id'] == 'list_node.priority.high':
            defect_risk = "High"
        elif priority['id'] == 'list_node.priority.medium':
            defect_risk = "High"
        elif priority['id'] == 'list_node.priority.low':
            defect_risk = "Medium"

    elif severity['id'] == 'list_node.severity.medium':
        if priority is None:
            defect_risk = "Medium (Priority Unknown)"
        elif priority['id'] == 'list_node.priority.urgent':
            defect_risk = "High"
        elif priority['id'] == 'list_node.priority.very_high':
            defect_risk = "High"
        elif priority['id'] == 'list_node.priority.high':
            defect_risk = "Medium"
        elif priority['id'] == 'list_node.priority.medium':
            defect_risk = "Medium"
        elif priority['id'] == 'list_node.priority.low':
            defect_risk = "Medium"

    elif severity['id'] == 'list_node.severity.low':
        if priority is None:
            defect_risk = "Low (Priority Unknown)"
        elif priority['id'] == 'list_node.priority.urgent':
            defect_risk = "Medium"
        elif priority['id'] == 'list_node.priority.very_high':
            defect_risk = "Medium"
        elif priority['id'] == 'list_node.priority.high':
            defect_risk = "Low"
        elif priority['id'] == 'list_node.priority.medium':
            defect_risk = "Low"
        elif priority['id'] == 'list_node.priority.low':
            defect_risk = "Low"

    # ------ Login to Octane
    # Define variables
    url = "http://192.168.5.138:8087"
    client_id = "webhooks_pnqjkl0nylp3qi65my2w9kxv3"
    client_secret = "+12911923422424990247202X"
    ContentType = {'Content-Type': 'application/json', 'ALM_OCTANE_TECH_PREVIEW': 'true'}

    # Define resource and payload for sign in
    resource = 'authentication/sign_in'
    payload = {"client_id": client_id, "client_secret": client_secret}

    # Send request and receive response (REST API)
    resp = requests.post(url + '/' + resource,
                         data=json.dumps(payload),
                         headers=ContentType)

    # SAVE Cookie and use in all subsequent requests
    cookie = resp.cookies
    print('Login: ' + str(resp.status_code))

    shared_space = space
    workspace = workspace
    # set retest counter
    # Read Defects using the cookie from the #Sign_in function
    resource = 'defects/' + defect_id

    # Create a defect in Octane
    defect_data = {"risk_udf": defect_risk}
    defects = requests.put(url + '/api/shared_spaces/' + shared_space + '/workspaces/' + workspace + '/' + resource,
                           data=json.dumps(defect_data),
                           headers=ContentType,
                           cookies=cookie)

    print('Creating Defect Status: ' + str(defects.status_code))
    if defects.status_code == 201:
        print('Defect with ID: ' + defects.json()['data'][0]['id'] + ' created successfully.')

    # ------ Logout from Octane
    # Define resource for sign out
    resource = 'authentication/sign_out'

    # Send request to sign out - important to sign out from the session, provide the cookie received at sign in
    resp = requests.post(url + '/' + resource,
                         data=json.dumps(payload),
                         headers=ContentType,
                         cookies=cookie)

    print('Logout: ' + str(resp.status_code))


@app.route('/defect_webhook', methods=['POST'])
def defect_webhook():
    if request.args.get('test') is None:
        server_url = request.json['server_url']
        event_type = request.json['event_type']
        sharedspace_id = str(request.json['sharedspace_id'])
        workspace_id = str(request.json['workspace_id'])
        username_id = str(request.json['username']['id'])
        username_mail = request.json['username']['email']
        json_data = request.json['data']
        print("******************************************")
        print(str(json_data))
        for dataset in json_data:
            print("******************************************")
            print("DATASET: " + str(dataset))
            print("******************************************")
            print("ENTITY: " + str(dataset['entity']))
            type = dataset['entity']['type']
            id = str(dataset['entity']['id'])
            retestcounter = dataset['entity']['risk_udf']
            name = dataset['entity']['name']
            # phases = dataset['entity']['phase']
            print("******************************************")
            # print("PHASES: " + str(phases))
            changes = dataset['changes']
            print("******************************************")
            print("CHANGES: " + str(dataset['changes']))
        print("******************************************")
        print("Server: " + server_url)
        print("event_type: " + event_type)
        print("sharedspace_id: " + sharedspace_id)
        print("workspace_id: " + workspace_id)
        print("username_id: " + username_id)
        print("username_mail: " + username_mail)
        print("type: " + type)
        print("defect id: " + id)
        print("name: " + name)
        print("Retest counter: " + retestcounter)
        print("******************************************")
        CHANGES = dataset['changes']
        # print(str(hasattr(CHANGES, 'phase')))
        if 'phase' in CHANGES:
            old = CHANGES['phase']['oldValue']['id']
            new = CHANGES['phase']['newValue']['id']
            if old == FROM_PHASE and new == TO_PHASE:
                update_retest_counter(id, retestcounter)
                print("CHANGE DEFECT and COUNT RETEST")
        else:
            print('phase not changed')
    else:
        print("Connection successful: " + str(request.args.get('test')))
    return 'Connection successful'


def update_retest_counter(defect_id, retestcounter):
    # Required import

    # ------ Login to Octane
    # Define variables
    url = "http://almoctane:8080"
    client_id = "API_asdasdasdq213123"
    client_secret = ")asdas123213123sd123"
    ContentType = {'Content-Type': 'application/json', 'ALM_OCTANE_TECH_PREVIEW': 'true'}

    # Define resource and payload for sign in
    resource = 'authentication/sign_in'
    payload = {"client_id": client_id, "client_secret": client_secret}

    # Send request and receive response (REST API)
    resp = requests.post(url + '/' + resource,
                         data=json.dumps(payload),
                         headers=ContentType)

    # SAVE Cookie and use in all subsequent requests
    cookie = resp.cookies
    print('Login: ' + str(resp.status_code))

    shared_space = '1001'
    workspace = '7001'
    # set retest counter
    # Read Defects using the cookie from the #Sign_in function
    resource = 'defects/' + defect_id

    # Create a defect in Octane
    u_retestcounter = int(retestcounter) + 1
    print(str(u_retestcounter))
    defect_data = {"risk_udf": str(u_retestcounter)}
    defects = requests.put(url + '/api/shared_spaces/' + shared_space + '/workspaces/' + workspace + '/' + resource,
                           data=json.dumps(defect_data),
                           headers=ContentType,
                           cookies=cookie)

    print('Creating Defect Status: ' + str(defects.status_code))
    if defects.status_code == 201:
        print('Defect with ID: ' + defects.json()['data'][0]['id'] + ' created successfully.')

    # ------ Logout from Octane
    # Define resource for sign out
    resource = 'authentication/sign_out'

    # Send request to sign out - important to sign out from the session, provide the cookie received at sign in
    resp = requests.post(url + '/' + resource,
                         data=json.dumps(payload),
                         headers=ContentType,
                         cookies=cookie)

    print('Logout: ' + str(resp.status_code))


if __name__ == '__main__':
    app.run(host='192.555.333.222',
            port='5555')
