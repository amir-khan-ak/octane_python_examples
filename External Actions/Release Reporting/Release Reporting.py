import tempfile

import plotly
import plotly.figure_factory as ff
import requests, json
from flask import Flask, render_template, request
import Basics.Authentication.Authenticationfunctions as Auth

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.route('/release_overview', methods=['GET'])
def release_overview():
    url = request.args.get('octane_url')
    shared_space = request.args.get('shared_space')
    workspace = request.args.get('workspace')
    entity_ids = request.args.get('entity_ids')
    client_id = "Python_1wqe213qwe35tt34o97oz4o"
    client_secret = "(1236123sad324324ZQ"
    ContentType = {'Content-Type': 'application/json', 'ALM_OCTANE_TECH_PREVIEW': 'true'}

    # Sign_in to ALM Octane and save cookie
    response_code, cookie = Auth.sign_in(url, client_id, client_secret)

    # Read Releases
    resource = 'releases?query="id IN ' + entity_ids + '"'
    releases = requests.get(url + '/api/shared_spaces/' + shared_space + '/workspaces/' + workspace + '/' + resource,
                            headers=ContentType,
                            cookies=cookie)

    print('Getting releases Status: ' + str(releases.status_code))
    releases_data = releases.json()
    releases_total_count = releases_data['total_count']
    releases_list = releases_data['data']
    print('Total releases: ' + str(releases_total_count))

    df = []
    # iterate through all Releases
    for release in releases_list:
        print('Release Name: ' + release['name'] + ', ID: ' + release['id'] + ', Startdate: ' + release['start_date'] +
              ', Enddate: ' + release['end_date'])
        df.append(dict(Task=release['name'], Start=release['start_date'], Finish=release['end_date']))

    #Build a figure using plotly
    fig = ff.create_gantt(df, title='ALM Octane Releases on Timeline')
    print(tempfile.gettempdir())

    # Make figure available offline to parse to ALM Octane
    plotly.offline.plot(fig, filename='templates/releases_on_gantt.html', auto_open=False)

    # Sign_out from ALM Octane
    response_code = Auth.sign_out(url, cookie)

    return render_template('releases_on_gantt.html')


if __name__ == '__main__':
    app.run(host='192.888.239.131',
            port='8315')
