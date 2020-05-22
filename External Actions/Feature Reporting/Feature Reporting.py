import tempfile
import plotly
import plotly.figure_factory as ff
import plotly.graph_objects as go
import requests, json
from flask import Flask, render_template, request
import Basics.Authentication.Authenticationfunctions as Auth

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.route('/risky_features', methods=['GET'])
def risky_features():
    url = request.args.get('octane_url')
    shared_space = request.args.get('shared_space')
    workspace = request.args.get('workspace')
    entity_ids = request.args.get('entity_ids')
    client_id = "Python_1wqe213qwe35tt34o97oz4o"
    client_secret = "(1236123sad324324ZQ"
    ContentType = {'Content-Type': 'application/json', 'ALM_OCTANE_TECH_PREVIEW': 'true'}

    # Sign_in to ALM Octane and save cookie
    response_code, cookie = Auth.sign_in(url, client_id, client_secret)
    ##############################################
    resource = 'features?query="id IN ' + entity_ids + '"'
    features = requests.get(
        url + '/api/shared_spaces/' + shared_space + '/workspaces/' + workspace + '/' + resource,
        headers=ContentType,
        cookies=cookie)
    features_data = features.json()
    features_total_count = features_data['total_count']
    features_list = features_data['data']
    features_cat = []
    priority_r = []
    severity_r = []
    for feature in features_list:
        # print('pipeline Name: ' + pipeline['name'] + ', pipeline ID: ' + pipeline['id'])
        resource = 'defects?query="parent EQ {id IN ' + feature['id'] + '};' \
                                                                        'phase EQ {id IN ^phase.defect.new^,' \
                                                                        '^phase.defect.opened^}"'
        defects = requests.get(
            url + '/api/shared_spaces/' + shared_space + '/workspaces/' + workspace + '/' + resource,
            headers=ContentType,
            cookies=cookie)
        defects_data = defects.json()
        defects_total_count = defects_data['total_count']
        defects_list = defects_data['data']
        t_priority = 0
        t_severity = 0
        t_counter = 0
        for defect in defects_list:
            t_counter = t_counter + 1
            if defect['priority'] is None:
                t_priority = t_priority + 0
            elif defect['priority']['id'] == 'list_node.priority.urgent':
                t_priority = t_priority + 5
            elif defect['priority']['id'] == 'list_node.priority.very_high':
                t_priority = t_priority + 4
            elif defect['priority']['id'] == 'list_node.priority.high':
                t_priority = t_priority + 3
            elif defect['priority']['id'] == 'list_node.priority.medium':
                t_priority = t_priority + 2
            elif defect['priority']['id'] == 'list_node.priority.low':
                t_priority = t_priority + 1

            if defect['severity'] is None:
                t_severity = t_severity + 0
            elif defect['severity']['id'] == 'list_node.severity.urgent':
                t_severity = t_severity + 5

            elif defect['severity']['id'] == 'list_node.severity.very_high':
                t_severity = t_severity + 4

            elif defect['severity']['id'] == 'list_node.severity.high':
                t_severity = t_severity + 3

            elif defect['severity']['id'] == 'list_node.severity.medium':
                t_severity = t_severity + 2

            elif defect['severity']['id'] == 'list_node.severity.low':
                t_severity = t_severity + 1

        features_cat.append(feature['id'] + ' - ' + feature['name'])
        if t_counter == 0:
            priority_r.append(0)
            severity_r.append(0)
        else:
            priority_r.append(t_priority / t_counter)
            severity_r.append(t_severity / t_counter)

    categories = features_cat

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=priority_r,
        theta=categories,
        fill='toself',
        name='Priority'
    ))
    fig.add_trace(go.Scatterpolar(
        r=severity_r,
        theta=categories,
        fill='toself',
        name='Severity'
    ))

    fig.update_layout(
        title='Feature Risk Circle [Based on "new and opened" Defects average priority and severity]',
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5]
            )),
        showlegend=True
    )

    ##############################################
    # Sign_out from ALM Octane
    response_code = Auth.sign_out(url, cookie)

    plotly.offline.plot(fig, filename='templates/risky_features.html', auto_open=False)

    return render_template('risky_features.html')



if __name__ == '__main__':
    app.run(host='192.888.239.131',port='8315')
