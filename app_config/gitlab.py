import requests
import json
import pprint
import os
import logging


# Gitlab API Documenation: http://doc.gitlab.com/ce/api/

private_token = None
# Download Gitlab private token for authentication if not already done so
if not os.path.isfile(os.path.expanduser('~')+'/.gitlab_token'):

    print("\nYou are missing the gitlab access token - due to changes in the gitlab API this cannot be done automatically for you any more\n\nPlease follow the procedure described as resolution of: https://jira.psi.ch/browse/CTRLIT-6320 before you continue ...\n")
    exit(-1)

    # import getpass
    #
    # print('To download your Gitlab private token please authenticate')
    # print('Username: '+getpass.getuser())
    #
    # data = {"login": getpass.getuser(), 'password': getpass.getpass()}
    # r = requests.post('https://git.psi.ch/api/v4/profile/account', data=data)
    # response = json.loads(r.content.decode("utf-8"))
    # print(response)
    # private_token = response['private_token']
    # with open(os.path.expanduser('~')+'/.gitlab_token', 'w') as tfile:
    #     tfile.write(response['private_token'])
    # os.chmod(os.path.expanduser('~')+'/.gitlab_token', 0o600)

# Somehow get private token for gitlab
if not private_token:
    with open(os.path.expanduser('~')+'/.gitlab_token', 'r') as tfile:
        private_token = tfile.read().replace('\n', '')

if 'GITLAB_PRIVATE_TOKEN' in os.environ:
    private_token = os.environ['GITLAB_PRIVATE_TOKEN']


print_response = False


def get_groups():
    # Get groups
    headers = {'PRIVATE-TOKEN': private_token}
    data = {"per_page": 100}
    r = requests.get('https://git.psi.ch/api/v3/groups', headers=headers, data=data)
    response = json.loads(r.content.decode("utf-8"))
    if print_response:
        print('Status Code: %d' % r.status_code)
        pprint.pprint(response)

    groups = dict()
    for group in response:
        logging.info('%s - %d' % (group['name'], group['id']))
        groups[group['name']] = ({'name': group['name'], 'id': group['id']})

    return groups


def get_projects():
    # Get projects / repositories
    headers = {'PRIVATE-TOKEN': private_token}
    r = requests.get('https://git.psi.ch/api/v3/projects', headers=headers)
    response = json.loads(r.content.decode("utf-8"))
    if print_response:
        print('Status Code: %d' % r.status_code)
        pprint.pprint(response)

    projects = []
    for project in response:
        logging.info('%s [%s] - %s' % (project['name'], project['path_with_namespace'], project['ssh_url_to_repo']))
        projects.append({'name': project['name'], 'path': project['path_with_namespace'], 'url': project['ssh_url_to_repo']})

    return projects


def create_group(group_name):
    # Create group/namespace
    headers = {'PRIVATE-TOKEN': private_token}
    data = {"name": group_name, "path":  group_name}
    r = requests.post('https://git.psi.ch/api/v3/groups', headers=headers, data=data)
    response = json.loads(r.content.decode("utf-8"))
    if print_response:
        print('Status Code: %d' % r.status_code)
        pprint.pprint(response)

    logging.info('%s - %d' % (response['name'], response['id']))
    return {'name': response['name'], 'id': response['id']}


def create_repository(repository_name, namespace_id):
    # Create repository/project
    headers = {'PRIVATE-TOKEN': private_token}
    data = {"name": repository_name, "namespace_id":  namespace_id}
    r = requests.post('https://git.psi.ch/api/v3/projects', headers=headers, data=data)
    response = json.loads(r.content.decode("utf-8"))
    if print_response:
        print('Status Code: %d' % r.status_code)
        pprint.pprint(response)

    logging.info('%s [%s] - %s' % (response['name'], response['path_with_namespace'], response['ssh_url_to_repo']))
    return {'name': response['name'], 'path': response['path_with_namespace'], 'url': response['ssh_url_to_repo']}


def get_group_id(group_name):
    headers = {'PRIVATE-TOKEN': private_token}
    data = {"search": group_name}
    r = requests.get('https://git.psi.ch/api/v3/groups', headers=headers, data=data)
    response = json.loads(r.content.decode("utf-8"))
    if print_response:
        print('Status Code: %d' % r.status_code)
        pprint.pprint(response)

    return response[0]['id']


def get_group_projects(group_id):
    headers = {'PRIVATE-TOKEN': private_token}
    r = requests.get('https://git.psi.ch/api/v3/groups/%d' % group_id, headers=headers)
    response = json.loads(r.content.decode("utf-8"))
    if print_response:
        print('Status Code: %d' % r.status_code)
        pprint.pprint(response)

    projects = []
    for project in response['projects']:
        logging.info('%s %s [%s] - %s' % (project['name'], project['id'], project['path_with_namespace'], project['ssh_url_to_repo']))
        projects.append({'name': project['name'], 'id': project['id'], 'path': project['path_with_namespace'], 'url': project['ssh_url_to_repo']})

    return projects


def fork_project(project_id):
    # POST /projects/fork/:id
    # Create group/namespace
    headers = {'PRIVATE-TOKEN': private_token}
    r = requests.post('https://git.psi.ch/api/v3/projects/fork/%d' % project_id, headers=headers)
    response = json.loads(r.content.decode("utf-8"))
    if print_response:
        print('Status Code: %d' % r.status_code)
        pprint.pprint(response)

    return response


def create_merge_request(project_id, project_id_fork, title='Test Merge Request', description='Some wonderful text'):
    # POST /projects/:id/merge_requests
    headers = {'PRIVATE-TOKEN': private_token}
    data = {'target_project_id': project_id, 'source_branch': 'master', 'target_branch': 'master', 'title': title, 'description': description}
    r = requests.post('https://git.psi.ch/api/v3/projects/%d/merge_requests' % project_id_fork, headers=headers, data=data)
    response = json.loads(r.content.decode("utf-8"))
    if print_response:
        print('Status Code: %d' % r.status_code)
        pprint.pprint(response)

    return response


def get_owned_projects():
    # GET /projects/owned
    headers = {'PRIVATE-TOKEN': private_token}
    # data = {"search": group_name}
    data = {}
    r = requests.get('https://git.psi.ch/api/v3/projects/owned', headers=headers, data=data)
    response = json.loads(r.content.decode("utf-8"))
    if print_response:
        print('Status Code: %d' % r.status_code)
        pprint.pprint(response)

    return response


def delete_project(project_id):
    # DELETE /projects/:id
    headers = {'PRIVATE-TOKEN': private_token}
    r = requests.delete('https://git.psi.ch/api/v3/projects/%d' % project_id, headers=headers)
    response = json.loads(r.content.decode("utf-8"))
    if print_response:
        print('Status Code: %d' % r.status_code)
        pprint.pprint(response)

    return


def get_username():
    headers = {'PRIVATE-TOKEN': private_token}
    r = requests.get('https://git.psi.ch/api/v3/user', headers=headers)
    response = json.loads(r.content.decode("utf-8"))
    if print_response:
        print('Status Code: %d' % r.status_code)
        pprint.pprint(response)

    return response['username']


def update_project_visibility(project_id, visibility=10):
    headers = {'PRIVATE-TOKEN': private_token}
    data = {"visibility_level": visibility}
    r = requests.put('https://git.psi.ch/api/v3/projects/%d' % project_id, headers=headers, data=data)
    response = json.loads(r.content.decode("utf-8"))
    if print_response:
        print('Status Code: %d' % r.status_code)
        pprint.pprint(response)

    return response


def update_visibility_all_projects(visibility=10, excludes=[]):
    """
    Update the visibility of the projects of all visible groups except the groups passed via the excludes parameter
    :param visibility: Visibility setting of the project 10=internal, 0=private, 20=public - default: 10
    :param excludes: List of groups to exclude from this bulk update
    :return:
    """
    result = get_groups()

    repository_count = 0
    for (key, group) in result.items():
        # logging.info('Process group: %s' % group['name'])
        print('Process group: %s' % group['name'])
        # Exclude groups ...
        if group['name'] in excludes:
            continue

        group_id = group['id']
        # group_id = get_group_id('launcher_config')
        projects = get_group_projects(group_id)
        for project in projects:
            # logging.info('Update project: %s' % project['name'])
            print('Update project: %s' % project['name'])
            result = update_project_visibility(project['id'], visibility=visibility)
            # pprint.pprint(result)
            repository_count += 1

    # logging.info('Number of repositories changed: %d' % repository_count)
    print('Number of repositories changed: %d' % repository_count)


if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)

    if not private_token:
        print('Before executing this script make sure that you have set GITLAB_PRIVATE_TOKEN')

    # result = get_groups()
    # result = get_projects()
    # result = create_group('test')
    # result = create_repository('test', 18)

    # pprint.pprint(result)

    update_visibility_all_projects(excludes=['remote_data_transfers'])
