import tempfile
import plotly
import plotly.figure_factory as ff
import plotly.graph_objects as go
import requests, json
from flask import Flask, render_template, request
import Basics.Authentication.Authenticationfunctions as Auth

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.route('/defect_priority_severity', methods=['GET'])
def defect_priority_severity():
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
    # DEFECT Query
    resource = 'defects?query="id IN ' + entity_ids + '"'
    defects = requests.get(
        url + '/api/shared_spaces/' + shared_space + '/workspaces/' + workspace + '/' + resource,
        headers=ContentType,
        cookies=cookie)
    defects_data = defects.json()
    defects_total_count = defects_data['total_count']
    defects_list = defects_data['data']

    s1_p0 = 0
    s1_p1 = 0
    s1_p2 = 0
    s1_p3 = 0
    s1_p4 = 0
    s1_p5 = 0
    s2_p0 = 0
    s2_p1 = 0
    s2_p2 = 0
    s2_p3 = 0
    s2_p4 = 0
    s2_p5 = 0
    s3_p0 = 0
    s3_p1 = 0
    s3_p2 = 0
    s3_p3 = 0
    s3_p4 = 0
    s3_p5 = 0
    s4_p0 = 0
    s4_p1 = 0
    s4_p2 = 0
    s4_p3 = 0
    s4_p4 = 0
    s4_p5 = 0
    s5_p0 = 0
    s5_p1 = 0
    s5_p2 = 0
    s5_p3 = 0
    s5_p4 = 0
    s5_p5 = 0
    s0_p0 = 0
    s0_p1 = 0
    s0_p2 = 0
    s0_p3 = 0
    s0_p4 = 0
    s0_p5 = 0

    for defect in defects_list:
        if defect['severity'] is None:
            if defect['priority'] is None:
                s0_p0 = s0_p0 + 1
            elif defect['priority']['id'] == 'list_node.priority.urgent':
                s0_p5 = s0_p5 + 1
            elif defect['priority']['id'] == 'list_node.priority.very_high':
                s0_p4 = s0_p4 + 1
            elif defect['priority']['id'] == 'list_node.priority.high':
                s0_p3 = s0_p3 + 1
            elif defect['priority']['id'] == 'list_node.priority.medium':
                s0_p2 = s0_p2 + 1
            elif defect['priority']['id'] == 'list_node.priority.low':
                s0_p1 = s0_p1 + 1

        elif defect['severity']['id'] == 'list_node.severity.urgent':
            if defect['priority'] is None:
                s5_p0 = s5_p0 + 1
            elif defect['priority']['id'] == 'list_node.priority.urgent':
                s5_p5 = s5_p5 + 1
            elif defect['priority']['id'] == 'list_node.priority.very_high':
                s5_p4 = s5_p4 + 1
            elif defect['priority']['id'] == 'list_node.priority.high':
                s5_p3 = s5_p3 + 1
            elif defect['priority']['id'] == 'list_node.priority.medium':
                s5_p2 = s5_p2 + 1
            elif defect['priority']['id'] == 'list_node.priority.low':
                s5_p1 = s5_p1 + 1

        elif defect['severity']['id'] == 'list_node.severity.very_high':
            if defect['priority'] is None:
                s4_p0 = s4_p0 + 1
            elif defect['priority']['id'] == 'list_node.priority.urgent':
                s4_p5 = s4_p5 + 1
            elif defect['priority']['id'] == 'list_node.priority.very_high':
                s4_p4 = s4_p4 + 1
            elif defect['priority']['id'] == 'list_node.priority.high':
                s4_p3 = s4_p3 + 1
            elif defect['priority']['id'] == 'list_node.priority.medium':
                s4_p2 = s4_p2 + 1
            elif defect['priority']['id'] == 'list_node.priority.low':
                s4_p1 = s4_p1 + 1

        elif defect['severity']['id'] == 'list_node.severity.high':
            if defect['priority'] is None:
                s3_p0 = s3_p0 + 1
            elif defect['priority']['id'] == 'list_node.priority.urgent':
                s3_p5 = s3_p5 + 1
            elif defect['priority']['id'] == 'list_node.priority.very_high':
                s3_p4 = s3_p4 + 1
            elif defect['priority']['id'] == 'list_node.priority.high':
                s3_p3 = s3_p3 + 1
            elif defect['priority']['id'] == 'list_node.priority.medium':
                s3_p2 = s3_p2 + 1
            elif defect['priority']['id'] == 'list_node.priority.low':
                s3_p1 = s3_p1 + 1

        elif defect['severity']['id'] == 'list_node.severity.medium':
            if defect['priority'] is None:
                s2_p0 = s2_p0 + 1
            elif defect['priority']['id'] == 'list_node.priority.urgent':
                s2_p5 = s2_p5 + 1
            elif defect['priority']['id'] == 'list_node.priority.very_high':
                s2_p4 = s2_p4 + 1
            elif defect['priority']['id'] == 'list_node.priority.high':
                s2_p3 = s2_p3 + 1
            elif defect['priority']['id'] == 'list_node.priority.medium':
                s2_p2 = s2_p2 + 1
            elif defect['priority']['id'] == 'list_node.priority.low':
                s2_p1 = s2_p1 + 1

        elif defect['severity']['id'] == 'list_node.severity.low':
            if defect['priority'] is None:
                s1_p0 = s1_p0 + 1
            elif defect['priority']['id'] == 'list_node.priority.urgent':
                s1_p5 = s1_p5 + 1
            elif defect['priority']['id'] == 'list_node.priority.very_high':
                s1_p4 = s1_p4 + 1
            elif defect['priority']['id'] == 'list_node.priority.high':
                s1_p3 = s1_p3 + 1
            elif defect['priority']['id'] == 'list_node.priority.medium':
                s1_p2 = s1_p2 + 1
            elif defect['priority']['id'] == 'list_node.priority.low':
                s1_p1 = s1_p1 + 1

    x = ['P0 - Unknown', 'P1 - Low', 'P2 - Medium', 'P3 - High', 'P4 - Very High', 'P5 - Urgent']
    y = ['S5 - Critical', 'S4 - Very High', 'S3 - High', 'S2 - Medium', 'S1 - Low', 'S0 - Unknown']

    #Colors intensity 0=no heat, 10 = high heat
    z = [[5, 6, 7, 8, 9, 10],
         [4, 5, 6, 7, 8, 9],
         [3, 4, 5, 6, 7, 8],
         [2, 3, 4, 5, 6, 7],
         [1, 2, 3, 4, 5, 6],
         [0, 1, 2, 3, 4, 5]]

    z_text = [[str(s5_p0), str(s5_p1), str(s5_p2), str(s5_p3), str(s5_p4), str(s5_p5)],
              [str(s4_p0), str(s4_p1), str(s4_p2), str(s4_p3), str(s4_p4), str(s4_p5)],
              [str(s3_p0), str(s3_p1), str(s3_p2), str(s3_p3), str(s3_p4), str(s3_p5)],
              [str(s2_p0), str(s2_p1), str(s2_p2), str(s2_p3), str(s2_p4), str(s2_p5)],
              [str(s1_p0), str(s1_p1), str(s1_p2), str(s1_p3), str(s1_p4), str(s1_p5)],
              [str(s0_p0), str(s0_p1), str(s0_p2), str(s0_p3), str(s0_p4), str(s0_p5)]]

    fig = ff.create_annotated_heatmap(z, x=x, y=y, annotation_text=z_text, font_colors=['black'], colorscale="Tealrose")
    # fig.show()
    fig.update_layout(
        title='ALM Octane Defect Heatmap')

    # Sign_out from ALM Octane
    response_code = Auth.sign_out(url, cookie)

    plotly.offline.plot(fig, filename='templates/defect_priority_severity.html', auto_open=False)

    return render_template('defect_priority_severity.html')



if __name__ == '__main__':
    app.run(host='192.888.239.131',port='8315')
