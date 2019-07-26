import requests
import json
import pprint
import os
import sys
import errno
import logging
import gitlab
import const

# Gitlab API Documenation: http://doc.gitlab.com/ce/api/
# Python-Gitlab Documetation: https://python-gitlab.readthedocs.io/en/stable/index.html

private_token = None

print(const.AUTHENTICATE_REQUEST)
login = input(const.LOGIN_REQUEST)
password = getpass.getpass(prompt=const.PASSWORD_REQUEST)

gl = gitlab.Gitlab(const.endpoint, oauth_token=access_token, api_version=4)
gl.auth()

def oauth_authentication():
    """
    Requests oauth authentication for the current user and login provided to be able to perform git operations. 
    :return: Dictionary containing details of the authentication request (access_token, toke_type, refresh_token, scope and created_at)
    :rtype: dict
    """
    return requests.post(const.OATH_REQUEST+login+const.PASSWORD_URL+password).json()

try:
    private_token = oauth_authentication()["access_token"]
except Exception as ex:
    template = const.EXCEPTION_TEMPLATE
    message = template.format(type(ex).__name__, ex.args)
    print(message)
    sys.exit(errno.EACCES)

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
    try:
        group_id = gl.groups.get(group_name).attributes['id']
    except Exception as ex:
        template = const.EXCEPTION_TEMPLATE
        message = template.format(type(ex).__name__, ex.args)
        print(message)
    logging.info('Group name: %s (id %s)' % (group_name, group_id))
    return group_id

def get_group_projects(group_id):
    """
    Retrieves all the projects of a group, which is given as parameter.
    :param group_id: ID of the group of interest.
    :type group_id: int
    :return: List of the projects (for the specified group id) containing name, id, path and url (in a dictionary-type).
    :rtype: list
    """
    # Retrieve the group
    try:
        group = gl.groups.get(group_id)
    except Exception as ex:
        template = const.EXCEPTION_TEMPLATE
        message = template.format(type(ex).__name__, ex.args)
        print(message)
        return -1

    # Retrieve the group's projects
    group_projects = group.projects.list()
    # Retrieve the info from each project
    projects = []
    for project in group_projects:
        logging.info('%s %s [%s] - %s' % (project.attributes['name'], project.attributes['id'], project.attributes['path_with_namespace'], project.attributes['ssh_url_to_repo']))
        projects.append({'name': project.attributes['name'], 'id': project.attributes['id'], 'path': project.attributes['path_with_namespace'], 'url': project.attributes['ssh_url_to_repo']})
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
        return 0
    except Exception as ex:
        template = const.EXCEPTION_TEMPLATE
        message = template.format(type(ex).__name__, ex.args)
        print(message)
        return -1

def create_merge_request(project_id, target_branch, source_branch, title, description, labels):
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
        project = gl.projects.get(project_id)
        mr = project.mergerequests.create({'source_branch': source_branch,
                                        'target_branch': target_branch,
                                        'title': title})
        mr.description = description
        mr.labels = labels
        mr.save()
        return 0
    except Exception as ex:
        template = const.EXCEPTION_TEMPLATE
        message = template.format(type(ex).__name__, ex.args)
        print(message)
        return -1

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
        return -1
    projects = []
    for project in own_projects:
        logging.info('%s [%s] - %s' % (project.attributes['name'], project.attributes['path_with_namespace'], project.attributes['ssh_url_to_repo']))
        projects.append({'name': project.attributes['name'], 'path': project.attributes['path_with_namespace'], 'url': project.attributes['ssh_url_to_repo']})
    return projects

def delete_project(project_id):
    """
    Deletes the project given as parameter
    :return: Returns 0 if successful or -1 if a problem occured.
    :rtype: int
    """
    try:
        gl.projects.delete(project_id)
        return 0
    except Exception as ex:
        template = const.EXCEPTION_TEMPLATE
        message = template.format(type(ex).__name__, ex.args)
        print(message)
        return -1

def get_username():
    """
    Gets the current username 
    :return: Returns username if successful or "problem" if a problem occured.
    :rtype: str
    """
    try:
        username = gl.user.attributes['username']
        return username
    except Exception as ex:
        template = const.EXCEPTION_TEMPLATE
        message = template.format(type(ex).__name__, ex.args)
        print(message)
        return const.RETURN_PROBLEM

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

    if not private_token:
        print(const.NO_GITLAB_TOKEN)

    update_visibility_all_projects(excludes=['remote_data_transfers'])
