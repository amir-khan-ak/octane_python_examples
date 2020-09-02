import json, requests, ast, re
import shutil

from flask import request, render_template
from flask import Flask

app = Flask(__name__)

ContentType = {'Content-Type': 'application/json', 'ALM_OCTANE_TECH_PREVIEW': 'true'}
configfile = open('config\\config.json')
configjson = json.load(configfile)
client_id = configjson['client_id']
client_secret = configjson['client_secret']


def Login(url, shared_space, workspace, client_id, client_secret):
    # Login to Octane
    resource = 'authentication/sign_in'
    payload = {"client_id": client_id, "client_secret": client_secret}
    resp = requests.post(url + '/' + resource,
                         data=json.dumps(payload),
                         headers=ContentType)

    cookie = resp.cookies
    # print('Login: ' + str(resp.status_code))
    return str(resp.status_code), cookie


def getItemInfo(url, shared_space, workspace, resource):
    # Logging Into ALM Octane
    returncode, cookie = Login(url, shared_space, workspace, client_id, client_secret)

    t_resource = resource
    getItemInforesp = requests.get(
        url + '/api/shared_spaces/' + shared_space + '/workspaces/' + workspace + '/' + t_resource,
        headers=ContentType,
        cookies=cookie)
    print('getItemInfo: ' + t_resource + " - " + str(getItemInforesp.status_code))

    # Logging out from ALM Octane
    Logout(configjson['url'], cookie)

    return str(getItemInforesp.status_code), getItemInforesp.json()



def Logout(url, cookie):
    # Logout from Octane
    resource = 'authentication/sign_out'
    resp = requests.post(url + '/' + resource,
                         headers=ContentType,
                         cookies=cookie)
    # print('Logout: ' + str(resp.status_code))
    return str(resp.status_code)


@app.route('/testdatausage', methods=['GET'])
def testdatausage():
    entity_ids = request.args.get('entity_ids')
    url = request.args.get('octane_url')
    shared_space = request.args.get('shared_space')
    workspace = request.args.get('workspace')
    resource = 'manual_tests/' + entity_ids

    # get style
    style = getStyle()

    divHeader = getDivHeader()
    # get test by it
    returncode, testJson = getItemInfo(url, shared_space, workspace, resource)
    html =  """<div class="content">
                    <h2>Test Type not supported for this feature. Please select a manual test only.</h2>
                    </div>"""
    if returncode == '200':
        divTestHeader = getTestDivHeader(testJson, url, shared_space, workspace)

        divTestData = """<div class="content">
                    <h2>No Test Data Found for this Test</h2>
                    </div>"""
        if testJson['test_data_table'] is not None:
            resource = 'test_data_tables/' + testJson['test_data_table']['id']

            # get test by it
            returncode, testdataJson = getItemInfo(url, shared_space, workspace, resource)
            divTestData = getTestDataSets(testdataJson, url, shared_space, workspace)


        html = style + divHeader + divTestHeader + divTestData

    return html


def getTestDataSets(ptestdataJson, url, shared_space, workspace):

    params = '<th>Data Set</th><th>Iteration</th>'
    arrParam = []
    for parameter in ptestdataJson['data']['parameters']:
        params = params + '<th>' + parameter + '</th>'
        arrParam.append(parameter)

    params = params + '<th>Used in Tests</th><th>Executed in Runs</th>'

    tContent=''
    for dataset in ptestdataJson['data']['data_sets']:
        iterNo = 1
        resource = 'runs?query="data_set EQ {id EQ ' + str(dataset['id']) + '}"'
        returncode, datasetInRunsJson = getItemInfo(url, shared_space, workspace, resource)
        html_runs = ''
        html_tests = ''
        for datasetRun in datasetInRunsJson['data']:
            entityRunLink = url + "/ui/entity-navigation?p=" + shared_space + "/" + workspace + "&entityType=run&id=" + \
                        datasetRun['id']
            entityTestLink = url + "/ui/entity-navigation?p=" + shared_space + "/" + workspace + "&entityType=test&id=" + \
                     datasetRun['test']['id']

            html_runs = html_runs + '<a href="' + entityRunLink + '"> ' + str(datasetRun['id']) + ' </a><br>'
            if str(datasetRun['test']['id']) not in html_tests:
                html_tests = html_tests + '<a href="' + entityTestLink + '"> ' + str(datasetRun['test']['id']) + ' </a><br>'

        for iteration in dataset['iterations']:
            tContent = tContent + '<tr><td>' + dataset['name'] + '</td><td>' + str(iterNo) + '</td>'
            for sParam in arrParam:
                tContent = tContent + '<td>' + iteration[sParam] + '</td>'

            if iterNo == 1:
                if html_tests == '':
                    tContent = tContent + '<td>Not used in any Test</td>'
                else:
                    tContent = tContent + '<td>' + html_tests + '</td>'
                if html_runs == '':
                    tContent = tContent + '<td>Not used in any Run</td>'
                else:
                    tContent = tContent + '<td>' + html_runs + '</td>'
            else:
                tContent = tContent + '<td>See Iteration 1</td>'
                tContent = tContent + '<td>See Iteration 1</td>'
            tContent = tContent + '</tr>'
            iterNo = iterNo + 1

    test_data_table = """
        <div class="content">
          <h2>Datatable Information</h1>
          <p>Datatable Name: """ + ptestdataJson['name'] + """</p>
          <p>Created on: """ + str(ptestdataJson['creation_time']) + """</p>
          <p>Last modified on: """ + str(ptestdataJson['last_modified']) + """</p>
       </div>
        <table id="testdatatable" class="greenTable">
          <tr>
            """ + params + """
          </tr>
          
        """ + tContent + """
        </table>"""


    return test_data_table


def getTestDivHeader(ptestJson, url, shared_space, workspace):
    entityLink = url + "/ui/entity-navigation?p=" + shared_space + "/" + workspace + "&entityType=test&id=" + ptestJson['id']
    testHeader = """<div class="content">
          <h1>Test Case Information</h1>
          <p>Test Name: """ + ptestJson['name'] + """</p>
          <p><a href=""" + entityLink + """ style="display:block;">Test Id: """ + ptestJson['id'] + """</a></p>
          <p>Total steps: """ + str(ptestJson['steps_num']) + """</p>
          <p>Current phase: """ + ptestJson['phase']['id'] + """</p>
       </div>"""
    return testHeader

def getStyle():
    style = """<style>
                /* Style the body */
                body {
                  font-family: Arial;
                  margin: 0;
                }
                
                /* Header/Logo Title */
                .header {
                  padding: 10px;
                  text-align: center;
                  background: #0079ef;
                  color: white;
                  font-size: 25px;
                }
                
                /* Page Content */
                .content {padding:10px;}
                .label {
                  color: white;
                  padding: 8px;
                  font-family: Arial;
                }
                .green {background-color: #4CAF50;} /* Green */
                .blue {background-color: #2196F3;} /* Blue */
                .orange {background-color: #ff9800;} /* Orange */
                .red {background-color: #f44336;} /* Red */ 
                .grey {background-color: #e7e7e7; color: black;} /* Gray */ 
                            #customers {
                  font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;
                  border-collapse: collapse;
                  width: 100%;
                }

                table.greenTable {
                  font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;
                  border-collapse: collapse;
                  width: 100%;
                }
                
                table.greenTable td, #customers th {
                  border: 1px solid #ddd;
                  padding: 8px;
                }
                
                table.greenTable tr:nth-child(even){background-color: #f2f2f2;}
                
                table.greenTable tr:hover {background-color: #ddd;}
                
                table.greenTable th {
                  padding-top: 12px;
                  padding-bottom: 12px;
                  text-align: left;
                  background-color: #0079ef;
                  color: white;
                }
                </style>"""
    return style

def getDivHeader():
    divHeader = """<div class="header">
                  <h1>ALM Octane</h1>
                  <p>Test Data Usage Report</p>
                </div>"""
    return divHeader

if __name__ == '__main__':
    app.run(host='192.252.36.3',
            port='7777') #env info
