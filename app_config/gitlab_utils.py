import requests
import json
import pprint
import os
import sys
import errno
import logging
import gitlab
import const
import getpass
import time

# Gitlab API Documenation: http://doc.gitlab.com/ce/api/
# Python-Gitlab Documetation: https://python-gitlab.readthedocs.io/en/stable/index.html

access_token = None

print(const.AUTHENTICATE_REQUEST)
# login = input(const.LOGIN_REQUEST)
# password = getpass.getpass(prompt=const.PASSWORD_REQUEST)
login = "hax_l"
password = "PHDleo2019!"
def get_username():
    return login

def oauth_authentication():
    """
    Requests oauth authentication for the current user and login provided to be able to perform git operations. 
    :return: Dictionary containing details of the authentication request (access_token, toke_type, refresh_token, scope and created_at)
    :rtype: dict
    """
    return requests.post(const.OATH_REQUEST+login+const.PASSWORD_URL+password).json()

try:
    access_token = oauth_authentication()["access_token"]
except Exception as ex:
    template = const.EXCEPTION_TEMPLATE
    message = template.format(type(ex).__name__, ex.args)
    print(message)
    exit(-1)

gl = gitlab.Gitlab(const.ENDPOINT, oauth_token=access_token, api_version=4)
gl.auth()

def get_groups():
    """
    Retrieves all the groups of the current user.
    :return: Dictionary containing details of the groups (name and id).
    :rtype: dict
    """
    groups = gl.groups.list()
    groups_dict = dict()
    for group in groups:
        logging.info('%s - %d' % (group.attributes['name'], group.attributes['id']))
        groups_dict[group.attributes['name']] = ({'name': group.attributes['name'], 'id': group.attributes['id']})
    return groups_dict

def get_projects():
    """
    Retrieves all the projects of the current user.
    :return: List containing all the details of the projects (name, path and url) in a dictionary-type format.
    :rtype: list
    """
    projects_list = gl.projects.list()
    projects = []
    for project in projects_list:
        logging.info('%s [%s] - %s' % (project.attributes['name'], project.attributes['path_with_namespace'], project.attributes['ssh_url_to_repo']))
        projects.append({'name': project.attributes['name'], 'path': project.attributes['path_with_namespace'], 'url': project.attributes['ssh_url_to_repo']})
    return projects

def create_group(group_name, description):
    """
    Creates a group based on the name given as parameter and its description.
    :param group_name: Name of the group that will be created.
    :type group_name: str
    :param description: Description of the group that will be created.
    :type description: str
    :return: Returns 0 if successful or -1 if a problem occured.
    :rtype: int
    """
    try:
        newGroup = gl.groups.create({'name': group_name, 'path': group_name})
        newGroup.description = description
        newGroup.save()
        return 0
    except Exception as ex:
        template = const.EXCEPTION_TEMPLATE
        message = template.format(type(ex).__name__, ex.args)
        print(message)
        return -1

def get_project_web_url(project_name):
    projects_list = gl.projects.list(search=project_name)
    for project in projects_list:
        if project_name == project.attributes['name']:
            return project.attributes['web_url']
    raise Exception(const.PROJECT_NAME_NOT_FOUND)

def get_project_group(project_name):
    projects_list = gl.projects.list(search=project_name)
    for project in projects_list:
        if project_name == project.attributes['name']:
            return project.attributes['path_with_namespace'].split('/')[0]
    raise Exception(const.PROJECT_NAME_NOT_FOUND)

def get_forked_project(git_repository, git_repository_id, 
                                                        option_delete_fork):
    forked_project = None
    projects = get_owned_projects()
    for project in projects:
        if project['username'] == login and project['name'] == git_repository:
            if 'forked_from_project' in project:
                # check whether project is forked from the right project
                if project['forked_from_project']['name'] == git_repository:
                    print(const.FORKED_EXISTS.format(git_repository))
                    forked_project = project
            else:
                # Either we delete or we have to fail
                print(const.FORKED_EXISTS.format(git_repository))
                if not option_delete_fork:
                    return forked_project
            if option_delete_fork:
                # Delete fork
                print(const.GIT_DELETE_FORK_MSG)
                delete_project(project['id'])
                forked_project = None
            break
    return forked_project
        


def get_project_url(group_id, project_name):
    projects_list = gl.projects.list(search=project_name)
    for project in projects_list:
        if project.attributes['name'] == project_name:
            return project.attributes['http_url_to_repo']
    raise Exception(const.PROJECT_URL_NOT_FOUND)

def get_project_id(group_name, project_name):
    projects_list = gl.projects.list(search=project_name)
    for project in projects_list:
        if project.attributes['name'] == project_name and group_name in project.attributes['path_with_namespace']:
            return project.attributes['id']
    raise Exception(const.PROJECT_ID_NOT_FOUND)

def get_repo_group_names(config):
    repo_name = None
    group_name = None
    valid = False
    # config format: "const.ENDPOINT/group_name/project_name"
    if const.ENDPOINT in config:
        web_url = config
        web_url_split = web_url.split('/')
        if len(web_url_split) == 5:
            repo_name = web_url_split[-1]
            group_name = web_url_split[-2]
            valid = True
    elif '/' in config: # config format: "group_name/project_name"
        path_with_namespace = config.split('/')
        if len(path_with_namespace) == 2:
            group_name = path_with_namespace[0]
            repo_name = path_with_namespace[1]
            valid = True
    else: # config format: "project_name"
        repo_name = config
        group_name = get_project_group(repo_name)
        valid = True
    return repo_name, group_name, valid
    

def delete_group(group_name):
    """
    Deletes a group based on the name given as parameter.
    :param group_name: Name of the group that will be deleted.
    :type group_name: str
    :return: Returns 0 if successful or -1 if a problem occured.
    :rtype: int
    """
    try:
        group = gl.groups.get(group_name)
        group.delete()
        return 0
    except Exception as ex:
        template = const.EXCEPTION_TEMPLATE
        message = template.format(type(ex).__name__, ex.args)
        print(message)
        return -1


def create_repo(repo_name, namespace):
    """
    Creates a repository (project) with the name (given as parameter) under the specified namespace (also given as parameter).
    :param repo_name: Name of the repository that will be created.
    :type repo_name: str
    :param namespace: Namespace which the new repository will belong.
    :type namespace: str
    :return: Dictionary containing the details of the newly created repository, including name, path and url.
    :rtype: dict
    """
    try:
        namespace_id = gl.groups.get(namespace).attributes['id']
        project = gl.projects.create({'name': repo_name, 'namespace_id': namespace_id})
        logging.info('%s [%s] - %s' % (project.attributes['name'], project.attributes['path_with_namespace'], project.attributes['ssh_url_to_repo']))
        return {'name': project.attributes['name'], 'path': project.attributes['path_with_namespace'], 'url': project.attributes['ssh_url_to_repo']}
    except Exception as ex:
        template = const.EXCEPTION_TEMPLATE
        message = template.format(type(ex).__name__, ex.args)
        print(message)
        return -1

def get_group_id(group_name):
    """
    Retrieves the group id based on the group name given as parameter.
    :param group_name: Name of the group of interest.
    :type group_name: str
    :return: ID of the group given as parameter or -1 in case of a problem.
    :rtype: int
    """
    group_id = -1
    # it could be a personal group -> group name == username
    if group_name == login:
        group_id = 0
    else:
        try:
            group_id = gl.groups.get(group_name).attributes['id']
        except Exception as ex:
            template = const.EXCEPTION_TEMPLATE
            message = template.format(type(ex).__name__, ex.args)
            print(message)
        logging.info('Group name: %s (id %s)' % (group_name, group_id))
    return group_id

def get_group_projects(group_name):
    """
    Retrieves all the projects of a group, which is given as parameter.
    :param group_name: Name of the group of interest.
    :type group_id: str
    :return: List of the projects (for the specified group id) containing name, id, path and url (in a dictionary-type).
    :rtype: list
    """
    if group_name == login:
        group_id = 0
        group_projects = gl.projects.list(owned=True)
    else:
        # Retrieve the group's projects
        try:
            group = gl.groups.get(group_id, lazy = True)
            group_projects = group.projects.list()
        except Exception as ex:
            template = const.EXCEPTION_TEMPLATE
            message = template.format(type(ex).__name__, ex.args)
            print(message)
            exit(-1)
    
    # Retrieve the info from each project
    projects = []
    for project in group_projects:
        logging.info('%s %s [%s] - %s' % (project.attributes['name'], 
                                            project.attributes['id'], 
                                            project.attributes['path_with_namespace'], 
                                            project.attributes['http_url_to_repo']))
        projects.append({'name': project.attributes['name'], 
                        'id': project.attributes['id'], 
                        'path': project.attributes['path_with_namespace'], 
                        'url': project.attributes['http_url_to_repo']})
    return projects

def fork_project(project_id):
    """
    Creates a fork of the project given as parameter.
    :param project_id: ID of the project that wants to be forked.
    :type project_id: int
    :return: Returns 0 if successful or -1 if a problem occured.
    :rtype: int
    """
    try:
        project = gl.projects.get(project_id)
        fork = project.forks.create({})
        time.sleep(2)
        return fork.attributes['http_url_to_repo']
    except Exception as ex:
        template = const.EXCEPTION_TEMPLATE
        message = template.format(type(ex).__name__, ex.args)
        print(message)
        print(const.FORK_PROBLEM)
        exit(-1)

def create_merge_request(source_project_id, source_branch,
                        target_project_id, target_branch,
                        title, description, labels, clean_branch):
    """
    Creates a merge request based on the parameters given. 
    :param project_id: ID of the project for the merge request.
    :type project_id: int
    :param target_branch: Name of the target branch.
    :type project_id: str
    :param source_branch: Name of the source branch.
    :type source_branch: str
    :param title: Name of the merge request.
    :type title: str
    :param description: Description of the merge request.
    :type description: str
    :param labels: Possible labels for the merge request (this can be empty).
    :type labels: str
    :return: Returns 0 if successful or -1 if a problem occured.
    :rtype: int
    """
    try:
        project = gl.projects.get(source_project_id)
    except Exception as ex:
        template = const.EXCEPTION_TEMPLATE
        message = template.format(type(ex).__name__, ex.args)
        print(message)
        return -1

    mr = project.mergerequests.create({'source_branch': source_branch,
                                        'target_branch': target_branch,
                                        'title': title,
                                        'target_project_id': target_project_id,
                                        'remove_source_branch': clean_branch})
    mr.description = description
    mr.labels = labels
    mr.save()
    return mr

def get_owned_projects():
    """
    Retrieves the projects owned by the current user.
    :return: List of projects containing name, path and url (in a dictionary-type).
    :rtype: list
    """
    try:
        own_projects = gl.projects.list(owned=True)
    except Exception as ex:
        template = const.EXCEPTION_TEMPLATE
        message = template.format(type(ex).__name__, ex.args)
        print(message)
        exit(-1)
    
    projects = []
    for project in own_projects:
        logging.info('%s [%s] - %s' % (project.attributes['name'], project.attributes['path_with_namespace'], project.attributes['ssh_url_to_repo']))
        projects.append({'name': project.attributes['name'], 'path': project.attributes['path_with_namespace'], 'url': project.attributes['ssh_url_to_repo'], 'username': project.attributes['namespace']['name']})
        # if it's a fork add the source project
        if 'forked_from_project' in project.attributes:
            projects[-1]['forked_from_project'] = project.attributes['forked_from_project']
    return projects

def delete_project(project_id):
    """
    Deletes the project given as parameter
    :return: 
    """
    try:
        gl.projects.delete(project_id)
    except Exception as ex:
        template = const.EXCEPTION_TEMPLATE
        message = template.format(type(ex).__name__, ex.args)
        print(message)

def get_username():
    """
    Gets the current username 
    :return: Returns username if successful or "problem" if a problem occured.
    :rtype: str
    """
    try:
        username = gl.user.attributes['username']
    except Exception as ex:
        template = const.EXCEPTION_TEMPLATE
        message = template.format(type(ex).__name__, ex.args)
        print(message)

    if login == username:
        return username
    else:
        return -1

def update_project_visibility(project_id, visibility):
    """
    Update the visibility of the project passed via the excludes parameter
    :param project_id: ID of the project that will have it's visibility updated
    :type project_id: int
    :param visibility: New visibility for the project
    :type visibility: int
    :return: Returns 0 if successful or -1 if a problem occured.
    :rtype: int
    """
    try:
        project = gl.projects.get(project_id)
    except Exception as ex:
        template = const.EXCEPTION_TEMPLATE
        message = template.format(type(ex).__name__, ex.args)
        print(message)
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
    # for all groups
    for (key, group) in result.items():
        print('Process group: %s' % group['name'])
        # Exclude groups ...
        if group['name'] in excludes:
            continue

        group_id = group['id']
        projects = get_group_projects(group_id)
        for project in projects:
            result = update_project_visibility(project['id'], visibility=visibility)
            if result == 0:
                print('Visibility of project %s updated.' % project['name'])
                repository_count += 1
            else:
                print("Problem updating project the visibility of project %s." % project['name'])
    logging.info('Number of repositories changed: %d' % repository_count)
    print('Number of repositories changed: %d' % repository_count)


if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)

    if not access_token:
        print(const.NO_GITLAB_TOKEN)

    update_visibility_all_projects(excludes=['remote_data_transfers'])
