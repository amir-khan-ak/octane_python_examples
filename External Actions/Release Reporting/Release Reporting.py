import tempfile
import plotly
import plotly.figure_factory as ff
import plotly.graph_objects as go
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

    # Build a figure using plotly
    fig = ff.create_gantt(df, title='ALM Octane Releases on Timeline')
    print(tempfile.gettempdir())

    # Make figure available offline to parse to ALM Octane
    plotly.offline.plot(fig, filename='templates/releases_on_gantt.html', auto_open=False)

    # Sign_out from ALM Octane
    response_code = Auth.sign_out(url, cookie)

    return render_template('releases_on_gantt.html')


@app.route('/release_summary', methods=['GET'])
def release_summary():
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
    # read Releases
    resource = 'releases?query="id IN ' + entity_ids + '"&order_by=id'
    releases = requests.get(url + '/api/shared_spaces/' + shared_space + '/workspaces/' + workspace + '/' + resource,
                            headers=ContentType,
                            cookies=cookie)

    print('Getting releases: ' + str(releases.status_code))
    releases_data = releases.json()
    releases_total_count = releases_data['total_count']
    releases_list = releases_data['data']
    print('Total releases: ' + str(releases_total_count))

    labels = ["Releases"]
    parents = [""]
    values = [10]
    marker_colors = ["lightgrey"]
    # iterate through all Releases
    for release in releases_list:
        ### FEATURES
        resource = 'features?query="release EQ {id IN ' + release['id'] + '}"'
        features = requests.get(
            url + '/api/shared_spaces/' + shared_space + '/workspaces/' + workspace + '/' + resource,
            headers=ContentType,
            cookies=cookie)
        features_data = features.json()
        features_total_count = features_data['total_count']
        labels.append(release['name'])
        parents.append("Releases")
        marker_colors.append("#581845")
        values.append(features_total_count)
        labels.append("Features")
        parents.append(release['name'])
        values.append(features_total_count)
        marker_colors.append("#FF5733")

        # New State
        resource = 'features?query="release EQ {id IN ' + release['id'] + '};phase EQ {id EQ^phase.feature.new^}"'
        labels, parents, values, marker_colors = get_data_build_df(resource, url, shared_space, workspace, ContentType,
                                                                   cookie, labels, "New", parents, "Features", values,
                                                                   marker_colors, "#FF5733", "#FFA454")

        # InProgress State
        resource = 'features?query="release EQ {id IN ' + release[
            'id'] + '};phase EQ {id EQ^phase.feature.inprogress^}"'
        labels, parents, values, marker_colors = get_data_build_df(resource, url, shared_space, workspace, ContentType,
                                                                   cookie, labels, "In Progress", parents, "Features",
                                                                   values, marker_colors, "#FF5733", "#FFA454")

        # In Testing State
        resource = 'features?query="release EQ {id IN ' + release['id'] + '};phase EQ {id EQ^phase.feature.intesting^}"'
        labels, parents, values, marker_colors = get_data_build_df(resource, url, shared_space, workspace, ContentType,
                                                                   cookie, labels, "In Testing", parents, "Features",
                                                                   values, marker_colors, "#FF5733", "#FFA454")

        # Done State
        resource = 'features?query="release EQ {id IN ' + release['id'] + '};phase EQ {id EQ^phase.feature.done^}"'
        labels, parents, values, marker_colors = get_data_build_df(resource, url, shared_space, workspace, ContentType,
                                                                   cookie, labels, "Done", parents, "Features", values,
                                                                   marker_colors, "#FF5733", "#FFA454")

        ### STORIES
        resource = 'stories?query="release EQ {id IN ' + release['id'] + '}"'
        stories = requests.get(
            url + '/api/shared_spaces/' + shared_space + '/workspaces/' + workspace + '/' + resource,
            headers=ContentType,
            cookies=cookie)
        stories_data = stories.json()
        stories_total_count = stories_data['total_count']
        stories_list = stories_data['data']
        labels.append("User Stories")
        parents.append(release['name'])
        values.append(stories_total_count)
        marker_colors.append("#FFC300")

        # NEW STATE
        resource = 'stories?query="release EQ {id IN ' + release['id'] + '};phase EQ {id EQ^phase.story.new^}"'
        labels, parents, values, marker_colors = get_data_build_df(resource, url, shared_space, workspace, ContentType,
                                                                   cookie, labels, "_New_", parents, "User Stories",
                                                                   values, marker_colors, "#FFC300", "#FFE844")

        # IN PROGRESS STATE
        resource = 'stories?query="release EQ {id IN ' + release['id'] + '};phase EQ {id EQ^phase.story.inprogress^}"'
        labels, parents, values, marker_colors = get_data_build_df(resource, url, shared_space, workspace, ContentType,
                                                                   cookie, labels, "_In_Progress_", parents,
                                                                   "User Stories", values, marker_colors, "#FFC300",
                                                                   "#FFE844")

        # In Testing STATE
        resource = 'stories?query="release EQ {id IN ' + release['id'] + '};phase EQ {id EQ^phase.story.intesting^}"'
        labels, parents, values, marker_colors = get_data_build_df(resource, url, shared_space, workspace, ContentType,
                                                                   cookie, labels, "_In_Testing_", parents,
                                                                   "User Stories", values, marker_colors, "#FFC300",
                                                                   "#FFE844")

        # DONE STATE
        resource = 'stories?query="release EQ {id IN ' + release['id'] + '};phase EQ {id EQ^phase.story.done^}"'
        labels, parents, values, marker_colors = get_data_build_df(resource, url, shared_space, workspace, ContentType,
                                                                   cookie, labels, "_Done_", parents, "User Stories",
                                                                   values, marker_colors, "#FFC300", "#FFE844")

        # FOUND DEFECTS
        resource = 'defects?query="detected_in_release EQ {id IN ' + release['id'] + '}"'
        defects = requests.get(
            url + '/api/shared_spaces/' + shared_space + '/workspaces/' + workspace + '/' + resource,
            headers=ContentType,
            cookies=cookie)
        defects_data = defects.json()
        defects_total_count = defects_data['total_count']
        defects_list = defects_data['data']
        labels.append("Defects Found In Release")
        parents.append(release['name'])
        values.append(defects_total_count)
        marker_colors.append("#900C3F")

        # NEW STATE
        resource = 'defects?query="detected_in_release EQ {id IN ' + release[
            'id'] + '};phase EQ {id IN ^phase.defect.new^}"'
        labels, parents, values, marker_colors = get_data_build_df(resource, url, shared_space, workspace, ContentType,
                                                                   cookie, labels, "_NEW_", parents,
                                                                   "Defects Found In Release", values, marker_colors,
                                                                   "#900C3F", "#FF6B6B")

        # IN PROGRESS STATE
        resource = 'defects?query="detected_in_release EQ {id IN ' + release[
            'id'] + '};phase EQ {id IN ^phase.defect.opened^}"'
        labels, parents, values, marker_colors = get_data_build_df(resource, url, shared_space, workspace, ContentType,
                                                                   cookie, labels, "_OPENED_", parents,
                                                                   "Defects Found In Release", values, marker_colors,
                                                                   "#900C3F", "#FF6B6B")

        # In Testing STATE
        resource = 'defects?query="detected_in_release EQ {id IN ' + release[
            'id'] + '};phase EQ {id IN ^phase.defect.fixed^,^phase.defect.proposeclose^}"'
        labels, parents, values, marker_colors = get_data_build_df(resource, url, shared_space, workspace, ContentType,
                                                                   cookie, labels, "_IN_TESTING_", parents,
                                                                   "Defects Found In Release", values, marker_colors,
                                                                   "#900C3F", "#FF6B6B")

        # DONE STATE
        resource = 'defects?query="detected_in_release EQ {id IN ' + release[
            'id'] + '};phase EQ {id IN ^phase.defect.closed^,' \
                    '^phase.defect.rejected^,^phase.defect.duplicate^,' \
                    '^phase.defect.deferred^}"'
        labels, parents, values, marker_colors = get_data_build_df(resource, url, shared_space, workspace, ContentType,
                                                                   cookie, labels, "_DONE_", parents,
                                                                   "Defects Found In Release", values, marker_colors,
                                                                   "#900C3F", "#FF6B6B")

        # DEFECTS
        resource = 'defects?query="release EQ {id IN ' + release['id'] + '}"'
        defects = requests.get(
            url + '/api/shared_spaces/' + shared_space + '/workspaces/' + workspace + '/' + resource,
            headers=ContentType,
            cookies=cookie)
        defects_data = defects.json()
        defects_total_count = defects_data['total_count']
        defects_list = defects_data['data']
        labels.append("Defects Fixes Planned in Release")
        parents.append(release['name'])
        values.append(defects_total_count)
        marker_colors.append("#900C3F")

        # NEW STATE
        resource = 'defects?query="release EQ {id IN ' + release['id'] + '};phase EQ {id IN ^phase.defect.new^}"'
        labels, parents, values, marker_colors = get_data_build_df(resource, url, shared_space, workspace, ContentType,
                                                                   cookie, labels, "_NEW", parents,
                                                                   "Defects Fixes Planned in Release", values, marker_colors,
                                                                   "#900C3F", "#FF6B6B")

        # IN PROGRESS STATE
        resource = 'defects?query="release EQ {id IN ' + release['id'] + '};phase EQ {id IN ^phase.defect.opened^}"'
        labels, parents, values, marker_colors = get_data_build_df(resource, url, shared_space, workspace, ContentType,
                                                                   cookie, labels, "_OPENED", parents,
                                                                   "Defects Fixes Planned in Release", values, marker_colors,
                                                                   "#900C3F", "#FF6B6B")

        # In Testing STATE
        resource = 'defects?query="release EQ {id IN ' + release[
            'id'] + '};phase EQ {id IN ^phase.defect.fixed^,^phase.defect.proposeclose^}"'
        labels, parents, values, marker_colors = get_data_build_df(resource, url, shared_space, workspace, ContentType,
                                                                   cookie, labels, "_IN_TESTING", parents,
                                                                   "Defects Fixes Planned in Release", values, marker_colors,
                                                                   "#900C3F", "#FF6B6B")

        # DONE STATE
        resource = 'defects?query="release EQ {id IN ' + release['id'] + '};phase EQ {id IN ^phase.defect.closed^,' \
                                                                         '^phase.defect.rejected^,^phase.defect.duplicate^,' \
                                                                         '^phase.defect.deferred^}"'
        labels, parents, values, marker_colors = get_data_build_df(resource, url, shared_space, workspace, ContentType,
                                                                   cookie, labels, "_DONE", parents,
                                                                   "Defects Fixes Planned in Release", values, marker_colors,
                                                                   "#900C3F", "#FF6B6B")

        # RUNS
        resource = 'runs?query="release EQ {id IN ' + release['id'] + '}"'
        labels, parents, values, marker_colors = get_data_runs_build_df(resource, url, shared_space, workspace, ContentType, cookie, labels, "Total Test Runs",
                               parents,release['name'],values, marker_colors, "#80FF61")

        # PLANNED RUNS
        resource = 'runs?query="release EQ {id IN ' + release[
            'id'] + '};native_status EQ {id=^list_node.run_native_status.planned^}"'
        labels, parents, values, marker_colors = get_data_runs_build_df(resource, url, shared_space, workspace, ContentType, cookie, labels, "Planned Runs",
                               parents,"Total Test Runs",values, marker_colors, "#00F3FF")

        # PASSED RUNS
        resource = 'runs?query="release EQ {id IN ' + release[
            'id'] + '};native_status EQ {id=^list_node.run_native_status.passed^}"'
        labels, parents, values, marker_colors = get_data_runs_build_df(resource, url, shared_space, workspace, ContentType, cookie, labels, "Passed Runs",
                               parents,"Total Test Runs",values, marker_colors, "#04FF00")

        # FAILED RUNS
        resource = 'runs?query="release EQ {id IN ' + release[
            'id'] + '};native_status EQ {id=^list_node.run_native_status.failed^}""'
        labels, parents, values, marker_colors = get_data_runs_build_df(resource, url, shared_space, workspace, ContentType, cookie, labels, "Failed Runs",
                               parents,"Total Test Runs",values, marker_colors, "#FF0000")

        # NOT COMPLETED RUNS
        resource = 'runs?query="release EQ {id IN ' + release[
            'id'] + '};native_status EQ {id=^list_node.run_native_status.not_completed^}"'
        labels, parents, values, marker_colors = get_data_runs_build_df(resource, url, shared_space, workspace,
                                                                        ContentType, cookie, labels,
                                                                        "Not Completed Runs", parents,
                                                                        "Total Test Runs",values, marker_colors,
                                                                        "#FFB200")

        # BLOCKED RUNS
        resource = 'runs?query="release EQ {id IN ' + release[
            'id'] + '};native_status EQ {id=^list_node.run_native_status.blocked^}"'
        labels, parents, values, marker_colors = get_data_runs_build_df(resource, url, shared_space, workspace,
                                                                        ContentType, cookie, labels,
                                                                        "Blocked Runs",
                                                                        parents, "Total Test Runs", values,
                                                                        marker_colors, "#ACACAC")


        # SKIPPED RUNS
        resource = 'runs?query="release EQ {id IN ' + release[
            'id'] + '};native_status EQ {id=^list_node.run_native_status.skipped^}"'
        labels, parents, values, marker_colors = get_data_runs_build_df(resource, url, shared_space, workspace,
                                                                        ContentType, cookie, labels,
                                                                        "Skipped Runs",
                                                                        parents, "Total Test Runs", values,
                                                                        marker_colors, "#FFEC00")

    fig = go.Figure(go.Treemap(
        labels=labels,
        parents=parents,
        values=values,
        textinfo="label+value",
        marker_colors=marker_colors,
    ))
    ##############################################
    # Sign_out from ALM Octane
    response_code = Auth.sign_out(url, cookie)

    plotly.offline.plot(fig, filename='templates/release_summary.html', auto_open=False)

    return render_template('release_summary.html')


@app.route('/releases_summary_table', methods=['GET'])
def releases_summary_table():
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
    # read releases
    resource = 'releases?query="id IN ' + entity_ids + '"&order_by=id'
    releases = requests.get(url + '/api/shared_spaces/' + shared_space + '/workspaces/' + workspace + '/' + resource,
                            headers=ContentType,
                            cookies=cookie)

    print('Getting releases: ' + str(releases.status_code))
    releases_data = releases.json()
    releases_total_count = releases_data['total_count']
    releases_list = releases_data['data']
    print('Total releases: ' + str(releases_total_count))
    header_values = ['<b>Metric</b>']
    body_dimension = 0
    body_values = [['<b>Number of Features</b>', '- New', '- In Progress', '- In Testing', '- Done',
                    '<b>Number of User Stories</b>', '- New', '- In Progress', '- In Testing', '- Done',
                    '<b>Number of Defect Fixes</b>', '- New', '- In Progress', '- In Testing', '- Done',
                    '<b>Number of Defects Found</b>', '- New', '- In Progress', '- In Testing', '- Done',
                    '<b>Number of Test Executions</b>', '- Planned', '- Passed', '- Failed', '- Not Completed',
                    '- Blocked', '- Skipped',
                    '<b>Number of Execution Types</b>', '- Automated', '- Manual', '- Test Suites']]
    # iterate through all Releases
    for release in releases_list:
        body_dimension = body_dimension + 1
        ### FEATURES
        resource = 'features?query="release EQ {id IN ' + release['id'] + '}"'
        header_values.append(release['name'])
        body_values.append([])
        body_values, body_dimension = get_data_build_matrix(resource, url, shared_space, workspace, ContentType, cookie,
                                                            body_values, body_dimension,'<b>')

        # New State
        resource = 'features?query="release EQ {id IN ' + release['id'] + '};phase EQ {id EQ^phase.feature.new^}"'
        body_values, body_dimension = get_data_build_matrix(resource, url, shared_space, workspace, ContentType, cookie,
                                                            body_values, body_dimension,'')

        # In Progress State
        resource = 'features?query="release EQ {id IN ' + release[
            'id'] + '};phase EQ {id EQ^phase.feature.inprogress^}"'
        body_values, body_dimension = get_data_build_matrix(resource, url, shared_space, workspace, ContentType, cookie,
                                                            body_values, body_dimension,'')

        # In Testing State
        resource = 'features?query="release EQ {id IN ' + release['id'] + '};phase EQ {id EQ^phase.feature.intesting^}"'
        body_values, body_dimension = get_data_build_matrix(resource, url, shared_space, workspace, ContentType, cookie,
                                                            body_values, body_dimension,'')
        # Done State
        resource = 'features?query="release EQ {id IN ' + release['id'] + '};phase EQ {id EQ^phase.feature.done^}"'
        body_values, body_dimension = get_data_build_matrix(resource, url, shared_space, workspace, ContentType, cookie,
                                                            body_values, body_dimension,'')

        ### STORIES
        resource = 'stories?query="release EQ {id IN ' + release['id'] + '}"'
        body_values, body_dimension = get_data_build_matrix(resource, url, shared_space, workspace, ContentType, cookie,
                                                            body_values, body_dimension,'<b>')

        # NEW STATE
        resource = 'stories?query="release EQ {id IN ' + release['id'] + '};phase EQ {id EQ^phase.story.new^}"'
        body_values, body_dimension = get_data_build_matrix(resource, url, shared_space, workspace, ContentType, cookie,
                                                            body_values, body_dimension,'')

        # In Progress STATE
        resource = 'stories?query="release EQ {id IN ' + release['id'] + '};phase EQ {id EQ^phase.story.inprogress^}"'
        body_values, body_dimension = get_data_build_matrix(resource, url, shared_space, workspace, ContentType, cookie,
                                                            body_values, body_dimension,'')

        # In Testing STATE
        resource = 'stories?query="release EQ {id IN ' + release['id'] + '};phase EQ {id EQ^phase.story.intesting^}"'
        body_values, body_dimension = get_data_build_matrix(resource, url, shared_space, workspace, ContentType, cookie,
                                                            body_values, body_dimension,'')

        # DONE STATE
        resource = 'stories?query="release EQ {id IN ' + release['id'] + '};phase EQ {id EQ^phase.story.done^}"'
        body_values, body_dimension = get_data_build_matrix(resource, url, shared_space, workspace, ContentType, cookie,
                                                            body_values, body_dimension,'')

        # DEFECTS PLANNED FIXES
        resource = 'defects?query="release EQ {id IN ' + release['id'] + '}"'
        body_values, body_dimension = get_data_build_matrix(resource, url, shared_space, workspace, ContentType, cookie,
                                                            body_values, body_dimension,'<b>')

        # NEW STATE
        resource = 'defects?query="release EQ {id IN ' + release['id'] + '};phase EQ {id IN ^phase.defect.new^}"'
        body_values, body_dimension = get_data_build_matrix(resource, url, shared_space, workspace, ContentType, cookie,
                                                            body_values, body_dimension, '')

        # IN PROGRESS STATE
        resource = 'defects?query="release EQ {id IN ' + release['id'] + '};phase EQ {id IN ^phase.defect.opened^}"'
        body_values, body_dimension = get_data_build_matrix(resource, url, shared_space, workspace, ContentType, cookie,
                                                            body_values, body_dimension,'')

        # In Testing STATE
        resource = 'defects?query="release EQ {id IN ' + release[
            'id'] + '};phase EQ {id IN ^phase.defect.fixed^,^phase.defect.proposeclose^}"'
        body_values, body_dimension = get_data_build_matrix(resource, url, shared_space, workspace, ContentType, cookie,
                                                            body_values, body_dimension,'')

        # DONE STATE
        resource = 'defects?query="release EQ {id IN ' + release['id'] + '};phase EQ {id IN ^phase.defect.closed^,' \
                                                                         '^phase.defect.rejected^,^phase.defect.duplicate^,' \
                                                                         '^phase.defect.deferred^}"'
        body_values, body_dimension = get_data_build_matrix(resource, url, shared_space, workspace, ContentType, cookie,
                                                            body_values, body_dimension,'')

        # FOUND DEFECTS
        resource = 'defects?query="detected_in_release EQ {id IN ' + release['id'] + '}"'
        body_values, body_dimension = get_data_build_matrix(resource, url, shared_space, workspace, ContentType, cookie,
                                                            body_values, body_dimension,'<b>')

        # NEW STATE
        resource = 'defects?query="detected_in_release EQ {id IN ' + release[
            'id'] + '};phase EQ {id IN ^phase.defect.new^}"'
        body_values, body_dimension = get_data_build_matrix(resource, url, shared_space, workspace, ContentType, cookie,
                                                            body_values, body_dimension, '')

        # IN PROGRESS STATE
        resource = 'defects?query="detected_in_release EQ {id IN ' + release[
            'id'] + '};phase EQ {id IN ^phase.defect.opened^}"'
        body_values, body_dimension = get_data_build_matrix(resource, url, shared_space, workspace, ContentType, cookie,
                                                            body_values, body_dimension,'')

        # In Testing STATE
        resource = 'defects?query="detected_in_release EQ {id IN ' + release[
            'id'] + '};phase EQ {id IN ^phase.defect.fixed^,^phase.defect.proposeclose^}"'
        body_values, body_dimension = get_data_build_matrix(resource, url, shared_space, workspace, ContentType, cookie,
                                                            body_values, body_dimension,'')

        # DONE STATE
        resource = 'defects?query="detected_in_release EQ {id IN ' + release[
            'id'] + '};phase EQ {id IN ^phase.defect.closed^,' \
                    '^phase.defect.rejected^,^phase.defect.duplicate^,' \
                    '^phase.defect.deferred^}"'
        body_values, body_dimension = get_data_build_matrix(resource, url, shared_space, workspace, ContentType, cookie,
                                                            body_values, body_dimension,'')

        # RUNS
        resource = 'runs?query="release EQ {id IN ' + release['id'] + '}"'
        body_values, body_dimension = get_data_build_matrix(resource, url, shared_space, workspace, ContentType, cookie,
                                                            body_values, body_dimension, '<b>')

        # PLANNED RUNS
        resource = 'runs?query="release EQ {id IN ' + release[
            'id'] + '};native_status EQ {id=^list_node.run_native_status.planned^}"'
        body_values, body_dimension = get_data_build_matrix(resource, url, shared_space, workspace, ContentType, cookie,
                                                            body_values, body_dimension,'')

        # PASSED RUNS
        resource = 'runs?query="release EQ {id IN ' + release[
            'id'] + '};native_status EQ {id=^list_node.run_native_status.passed^}"'
        body_values, body_dimension = get_data_build_matrix(resource, url, shared_space, workspace, ContentType, cookie,
                                                            body_values, body_dimension, '')

        # FAILED RUNS
        resource = 'runs?query="release EQ {id IN ' + release[
            'id'] + '};native_status EQ {id=^list_node.run_native_status.failed^}""'
        body_values, body_dimension = get_data_build_matrix(resource, url, shared_space, workspace, ContentType, cookie,
                                                            body_values, body_dimension,'')

        # NOT COMPLETED RUNS
        resource = 'runs?query="release EQ {id IN ' + release[
            'id'] + '};native_status EQ {id=^list_node.run_native_status.not_completed^}"'
        body_values, body_dimension = get_data_build_matrix(resource, url, shared_space, workspace, ContentType, cookie,
                                                            body_values, body_dimension,'')

        # BLOCKED RUNS
        resource = 'runs?query="release EQ {id IN ' + release[
            'id'] + '};native_status EQ {id=^list_node.run_native_status.blocked^}"'
        body_values, body_dimension = get_data_build_matrix(resource, url, shared_space, workspace, ContentType, cookie,
                                                            body_values, body_dimension,'')

        # SKIPPED RUNS
        resource = 'runs?query="release EQ {id IN ' + release[
            'id'] + '};native_status EQ {id=^list_node.run_native_status.skipped^}"'
        body_values, body_dimension = get_data_build_matrix(resource, url, shared_space, workspace, ContentType, cookie,
                                                            body_values, body_dimension,'')

        # TOTAL EXECUTION TYPES
        #
        resource = 'runs?query="release EQ {id IN ' + release['id'] + '}"'
        body_values, body_dimension = get_data_build_matrix(resource, url, shared_space, workspace, ContentType, cookie,
                                                            body_values, body_dimension,'<b>')

        # AUTOMATED RUNS
        resource = 'runs?query="release EQ {id IN ' + release[
            'id'] + '};subtype EQ ^run_automated^"'
        body_values, body_dimension = get_data_build_matrix(resource, url, shared_space, workspace, ContentType, cookie,
                                                            body_values, body_dimension,'')

        # MANUAL RUNS
        resource = 'runs?query="release EQ {id IN ' + release[
            'id'] + '};subtype EQ ^run_manual^"'
        body_values, body_dimension = get_data_build_matrix(resource, url, shared_space, workspace, ContentType, cookie,
                                                            body_values, body_dimension,'')

        # SUITE RUNS
        resource = 'runs?query="release EQ {id IN ' + release[
            'id'] + '};subtype EQ ^run_suite^"'
        body_values, body_dimension = get_data_build_matrix(resource, url, shared_space, workspace, ContentType, cookie,
                                                            body_values, body_dimension,'')

    headerColor = 'grey'
    rowColor = 'white'

    fig = go.Figure(data=[go.Table(
        header=dict(
            values=header_values,
            line_color='darkslategray',
            fill_color=headerColor,
            align=['left', 'center'],
            font=dict(color='white', size=12)
        ),
        cells=dict(
            values=body_values,
            line_color='darkslategray',
            # 2-D list of colors for alternating rows
            fill_color=rowColor,
            align=['left', 'center'],
            font=dict(color='darkslategray', size=11)
        ))
    ])
    fig.update_layout(
        title='Multi Release Summary Table',
    )
    ##############################################
    # Sign_out from ALM Octane
    response_code = Auth.sign_out(url, cookie)

    plotly.offline.plot(fig, filename='templates/releases_summary_tables.html', auto_open=False)

    return render_template('releases_summary_tables.html')


def get_data_build_df(resource, url, shared_space, workspace, ContentType, cookie, labels, label_text, parents,
                      parent_text, values, marker_colors, marker_colors_parent, marker_color_child):
    response = requests.get(
        url + '/api/shared_spaces/' + shared_space + '/workspaces/' + workspace + '/' + resource,
        headers=ContentType,
        cookies=cookie)
    response_data = response.json()
    response_total_count = response_data['total_count']
    response_list = response_data['data']
    labels.append(label_text)
    parents.append(parent_text)
    values.append(response_total_count)
    marker_colors.append(marker_colors_parent)
    for item in response_list:
        if parent_text == "User Stories":
            labels.append('US-' + item['id'] + '-' + item['name'])
        elif parent_text == "Features":
            labels.append(item['name'])
        elif parent_text == "Defects Found In Release":
            labels.append('D-' + item['id'] + '-' + item['name'])
        elif parent_text == "Defects Fixes Planned in Release":
            labels.append('D-' + item['id'] + '-' + item['name'])

        parents.append(label_text)
        marker_colors.append(marker_color_child)
        if item['story_points'] is None:
            values.append(1)
        else:
            values.append(item['story_points'])
    return labels, parents, values, marker_colors


def get_data_runs_build_df(resource, url, shared_space, workspace, ContentType, cookie, labels, label_text, parents,
                      parent_text, values, marker_colors, marker_colors_parent):
    response = requests.get(
        url + '/api/shared_spaces/' + shared_space + '/workspaces/' + workspace + '/' + resource,
        headers=ContentType,
        cookies=cookie)
    response_data = response.json()
    response_total_count = response_data['total_count']
    labels.append(label_text)
    parents.append(parent_text)
    values.append(response_total_count)
    marker_colors.append(marker_colors_parent)
    return labels, parents, values, marker_colors


def get_data_build_matrix(resource, url, shared_space, workspace, ContentType, cookie, body_values, body_dimension,
                          body_text):
    response = requests.get(
        url + '/api/shared_spaces/' + shared_space + '/workspaces/' + workspace + '/' + resource,
        headers=ContentType,
        cookies=cookie)
    response_data = response.json()
    response_total_count = response_data['total_count']

    if body_text == '<b>':
        body_values[body_dimension].append('<b>' + str(response_total_count) + '</b>')
    else:
        body_values[body_dimension].append(response_total_count)
    return body_values, body_dimension


if __name__ == '__main__':
    app.run(host='192.888.239.131',port='8315')
