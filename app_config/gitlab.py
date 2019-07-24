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

###############
### UPDATED ###
###############
def oauth_authentication():
    return requests.post("https://git.psi.ch/oauth/token?grant_type=password&username="+login+"&password="+password).json()

###############
### UPDATED ###
###############
def get_groups():
    groups = gl.groups.list()
    groups_dict = dict()
    for group in groups:
        logging.info('%s - %d' % (group.attributes['name'], group.attributes['id']))
        groups_dict[group.attributes['name']] = ({'name': group.attributes['name'], 'id': group.attributes['id']})
    return groups_dict

###############
### UPDATED ###
###############
def get_projects():
    projects_list = gl.projects.list()
    projects = []
    for project in projects_list:
        logging.info('%s [%s] - %s' % (project.attributes['name'], project.attributes['path_with_namespace'], project.attributes['ssh_url_to_repo']))
        projects.append({'name': project.attributes['name'], 'path': project.attributes['path_with_namespace'], 'url': project.attributes['ssh_url_to_repo']})
    return projects

###############
### UPDATED ###
###############
def create_group(group_name, description):
    try:
        # creates the group and saves it
        newGroup = gl.groups.create({'name': group_name, 'path': group_name})
        newGroup.description = description
        newGroup.save()
        return 0
    except:
        print("Problem while creating group.")
        return -1
    
###############
### UPDATED ###
###############
def delete_group(group_name):
    try:
        group = gl.groups.get(group_name)
        group.delete()
        return 0
    except:
        print("Group to be deleted not found.")
        return -1

def create_repository(repository_name, namespace_id):
    # Create repository/project
    headers = {'PRIVATE-TOKEN': private_token}
    data = {"name": repository_name, "namespace_id":  namespace_id}
    r = requests.post('https://git.psi.ch/api/v4/projects', headers=headers, data=data)
    response = json.loads(r.content.decode("utf-8"))
    if print_response:
        print('Status Code: %d' % r.status_code)
        pprint.pprint(response)

    logging.info('%s [%s] - %s' % (response['name'], response['path_with_namespace'], response['ssh_url_to_repo']))
    return {'name': response['name'], 'path': response['path_with_namespace'], 'url': response['ssh_url_to_repo']}

###############
### UPDATED ###
###############
def get_group_id(group_name):
    group_id = -1
    try:
        group_id = gl.groups.get(group_name).attributes['id']
    except:
        print('Group name provided not found.')
    logging.info('Group name: %s (id %s)' % (group_name, group_id))
    return group_id

###############
### UPDATED ###
###############
def get_group_projects(group_id):
    # Retrieve the group
    try:
        group = gl.groups.get(group_id)
    except:
        print("Group id not found.")
        return -1

    # Retrieve the group's projects
    group_projects = group.projects.list()
    # Retrieve the info from each project
    projects = []
    for project in group_projects:
        logging.info('%s %s [%s] - %s' % (project.attributes['name'], project.attributes['id'], project.attributes['path_with_namespace'], project.attributes['ssh_url_to_repo']))
        projects.append({'name': project.attributes['name'], 'id': project.attributes['id'], 'path': project.attributes['path_with_namespace'], 'url': project.attributes['ssh_url_to_repo']})
    return projects

###############
### UPDATED ###
###############
def fork_project(project_id):
    try:
        project = gl.projects.get(project_id)
        fork = project.forks.create({})
        return 0
    except:
        print("Problem forking project id: %s" % project_id)
        return -1

###############
### UPDATED ###
###############
def create_merge_request(project_id, target_branch, source_branch, title, description, labels):
    try:
        project = gl.projects.get(project_id)
        mr = project.mergerequests.create({'source_branch': source_branch,
                                        'target_branch': target_branch,
                                        'title': title})
        mr.description = description
        mr.labels = labels
        mr.save()
        return 0
    except:
        print("Problem creating merge request.")
        return -1

###############
### UPDATED ###
###############
def get_owned_projects():
    try:
        own_projects = gl.projects.list(owned=True)
    except:
        print("Problem accessing own projects.")
        return -1
    projects = []
    for project in own_projects:
        logging.info('%s [%s] - %s' % (project.attributes['name'], project.attributes['path_with_namespace'], project.attributes['ssh_url_to_repo']))
        projects.append({'name': project.attributes['name'], 'path': project.attributes['path_with_namespace'], 'url': project.attributes['ssh_url_to_repo']})
    return projects

###############
### UPDATED ###
###############
def delete_project(project_id):
    try:
        gl.projects.delete(project_id)
        return 0
    except:
        print("Problem deleting project id: %s." % project_id))
        return -1

###############
### UPDATED ###
###############
def get_username():
    try:
        username = gl.user.attributes['username']
        return username
    except:
        print("Problem getting username.")
        return -1

####################################
### NOT SURE IF THIS MAKES SENSE ###
####################################
def update_project_visibility(project_id, visibility):
    try:
        project = gl.projects.get(project_id)
    except:
        print('Problem changing visibility of project id %s. Maybe access must be granted explicitly to each user.' % project_id )
        return -1
    project.attributes['visibility'] = visibility
    project.save()
    return 0


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
