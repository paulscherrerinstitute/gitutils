#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from gitutils import const
import requests
import json
import pprint
import os
import sys
import errno
import logging
import gitlab
import getpass
import time
import pwd

# Gitlab API Documenation: http://doc.gitlab.com/ce/api/
# Python-Gitlab Documetation:
#       https://python-gitlab.readthedocs.io/en/stable/index.html

access_token = None
login = None
password = None
gl = None

def get_gl():
    return gl

def authenticate(endpoint):
    global gl
    global login
    global password
    global access_token
    private_token = None

    # Try to take the access token from the .gitlab_token file

    if os.path.isfile(os.path.expanduser('~') + '/.gitlab_token'):
        with open(os.path.expanduser('~') + '/.gitlab_token', 'r') as tfile:
            private_token = tfile.read().replace('\n', '')

    # if not existant, authenticate with the user and saves it
    if private_token is None:
        print(const.AUTHENTICATE_REQUEST)
        login = input(const.LOGIN_REQUEST)
        password = getpass.getpass(prompt=const.PASSWORD_REQUEST)
        try:
            access_token = oauth_authentication()['access_token']
        except Exception as ex:
            template = const.EXCEPTION_TEMPLATE
            message = template.format(type(ex).__name__, ex.args)
            print(message)
            sys.exit(-1)

        # saves token into personal file
        if access_token:
            with open(os.path.expanduser('~') + '/.gitlab_token', 'w'
                      ) as tfile:
                tfile.write(access_token)
            os.chmod(os.path.expanduser('~') + '/.gitlab_token', 0o600)

        # python-gitlab object
        gl = gitlab.Gitlab(const.ENDPOINT, oauth_token=access_token,
                           api_version=4)
    else:
        gl = gitlab.Gitlab(const.ENDPOINT, oauth_token=private_token,
                           api_version=4)
        login = pwd.getpwuid(os.getuid())[0]
    gl.auth()

def get_username():
    """
    Gets the username used for authentication.
    :return: Username
    :rtype: str
    """
    global login
    return login


def oauth_authentication():
    """
    Requests oauth authentication for the current user and login provided to be
    able to perform git operations.
    :return: Dictionary containing details of the authentication request
    (access_token, toke_type, refresh_token, scope and created_at)
    :rtype: dict
    """
    global login
    return requests.post(const.OATH_REQUEST + login +
                         const.PASSWORD_URL + password).json()


def get_groups():
    """
    Retrieves all the groups of the current user.
    :return: Dictionary containing details of the groups (name and id).
    :rtype: dict
    """

    groups = gl.groups.list()
    groups_dict = dict()
    for group in groups:
        logging.info('%s - %d' % (group.attributes['name'],
                     group.attributes['id']))
        groups_dict[group.attributes['name']] = \
            {'name': group.attributes['name'],
             'id': group.attributes['id']}
    return groups_dict


def get_projects():
    """
    Retrieves all the projects of the current user.
    :return: List containing all the details of the projects
    (name, path and url) in a dictionary-type format.
    :rtype: list
    """

    projects_list = gl.projects.list()
    projects = []
    for project in projects_list:
        logging.info('%s [%s] - %s' % (project.attributes['name'],
                     project.attributes['path_with_namespace'],
                     project.attributes['ssh_url_to_repo']))
        projects.append({'name': project.attributes['name'],
                         'path': project.attributes['path_with_namespace'],
                         'url': project.attributes['ssh_url_to_repo']})
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

    exitCode = 0
    try:
        newGroup = gl.groups.create({'name': group_name,
                                     'path': group_name,
                                     'description': description})
    except Exception as ex:
        template = const.EXCEPTION_TEMPLATE
        message = template.format(type(ex).__name__, ex.args)
        print(message)
        exitCode = -1
    logging.info('Newly created group: %s - %d' % (
                 newGroup.attributes['name'],
                 newGroup.attributes['id']))
    return exitCode


def get_project_web_url(project_name):
    """
    Function to get the web_url attribute of a project based on its name.
    :param project_name: Name of the project
    :type project_name: str
    :return: Returns the web url to the project.
    :rtype: str
    """

    projects_list = gl.projects.list(search=project_name)
    for project in projects_list:
        if project_name == project.attributes['name']:
            logging.info('Project web url: %s'
                         % project.attributes['web_url'])
            return project.attributes['web_url']
    raise Exception(const.PROJECT_NAME_NOT_FOUND)


def checkKey(dict, key):
    if key in dict:
        return True
    else:
        return False


def get_project_group(project_name, merge=False):
    """
    Function to get the group of a project based on its name.
    :param project_name: Name of the project
    :type project_name: str
    :return: Returns the name of the group.
    :rtype: str
    """

    count = 0
    projects_list = gl.projects.list(search=project_name)
    for project in projects_list:
        if project_name == project.attributes['name']:
            if merge:
                if checkKey(project.attributes, 'forked_from_project'):
                    groupFound = \
                        project.attributes['path_with_namespace'].split('/')[0]
                    count += 1
                    logging.info('Project\'s %s group:' % groupFound)
            elif not merge:
                project_path = project.attributes['path_with_namespace']
                groupFound = project_path.split('/')[0]
                count += 1
                logging.info('Project\'s %s group:' % groupFound)
    if count == 1:
        return groupFound
    elif count >= 2:
        raise Exception(const.MULTIPLE_PROJECTS)
    else:
        raise Exception(const.PROJECT_NAME_NOT_FOUND)


def get_forked_project(git_repository, git_repository_id):
    """
    Function to get the forked project based on the git repository name and id.
    :param git_repository: Name of the project
    :type git_repository: str
    :param git_repository_id: Id of the project
    :type git_repository_id: int
    :return: Returns the web url to the project.
    :rtype: str
    """
    global login
    forked_project = None
    projects = get_owned_projects()
    for project in projects:
        if project['username'] == login and project['name'] == git_repository:
            if 'forked_from_project' in project:
                # check whether project is forked from the right project
                if project['forked_from_project']['name'] == git_repository:
                    print(const.FORKED_EXISTS.format(git_repository))
                    logging.info(const.FORKED_EXISTS.format(git_repository))
                    forked_project = project
    return forked_project


def get_branch(project_id):
    """
    Function to check if there is a 'master' branch on the project.
    :param project_id: Id of the project
    :type project_id: int
    :return: Returns the name of the branch.
    :rtype: str
    """

    # Get a project by ID

    project = gl.projects.get(project_id, lazy=True)

    # Verifies if there is a master branch to merge into

    branch = project.branches.get('master')
    if branch.attributes['name']:
        logging.info('Master branch found within project id %s. '
                     % project_id)
        return 'master'
    else:
        raise Exception(const.GIT_UNABLE_TO_FIND_MASTER_BRANCH
                        % project['name'])


def get_project_url(group_id, project_name):
    """
    Function to get the project http url attribute of a project based on
    its group id and name.
    :param project_name: Name of the project
    :type project_name: str
    :param group_id: Id of the group
    :type group_id: int
    :return: Returns the http url to the project.
    :rtype: str
    """

    projects_list = gl.projects.list(search=project_name)
    for project in projects_list:
        if project.attributes['name'] == project_name:
            logging.info('Project http url to repo: %s'
                         % project.attributes['http_url_to_repo'])
            return project.attributes['http_url_to_repo']
    raise Exception(const.PROJECT_URL_NOT_FOUND)


def get_project_id(group_name, project_name):
    """
    Function to get the id attribute of a project based on its group and
    project name.
    :param group_name: Name of the group
    :type group_name: str
    :param project_name: Name of the project
    :type project_name: str
    :return: Returns the id of the project.
    :rtype: str
    """

    projects_list = gl.projects.list(search=project_name)
    for project in projects_list:
        if project.attributes['name'] == project_name:
            if group_name in project.attributes['path_with_namespace']:
                logging.info('Found the project id ( %s - %s ) : %s' % (
                             group_name, project_name,
                             project.attributes['id']))
                return project.attributes['id']
    raise Exception(const.PROJECT_ID_NOT_FOUND)


def get_repo_group_names(config):
    """
    Gets the project name and group name based on the argument given
    on the cli.
    :param config: String given as argument that can be of different
    formats: full path to the project, groupname/projectname or project name.
    :type config: str
    :return: Returns the project name, group name and a boolean indicating
    if the results are valid.
    :rtype: tuple
    """

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
    elif '/' in config:
        # config format: "group_name/project_name"
        path_with_namespace = config.split('/')
        if len(path_with_namespace) == 2:
            group_name = path_with_namespace[0]
            repo_name = path_with_namespace[1]
            valid = True
    else:
        # config format: "project_name"
        repo_name = config
        group_name = get_project_group(repo_name, False)

        # warning if multiple and ERROR out - > ambiguous
        valid = True

    project_id = get_project_id(group_name, repo_name)
    return (repo_name, group_name, project_id, valid)


def delete_group(group_name):
    """
    Deletes a group based on the name given as parameter.
    :param group_name: Name of the group that will be deleted.
    :type group_name: str
    :return: Returns 0 if successful or -1 if a problem occured.
    :rtype: int
    """

    group = gl.groups.get(group_name, lazy=True)
    returnCode = 0
    try:
        group.delete()
    except Exception as ex:
        template = const.EXCEPTION_TEMPLATE
        message = template.format(type(ex).__name__, ex.args)
        print(message)
        returnCode = -1
    logging.info('Deleted group: %s' % group_name)
    return returnCode


def create_repo(repo_name, namespace):
    """
    Creates a repository (project) with the name (given as parameter) under
    the specified namespace (also given as parameter).
    :param repo_name: Name of the repository that will be created.
    :type repo_name: str
    :param namespace: Namespace which the new repository will belong.
    :type namespace: str
    :return: Dictionary containing the details of the newly created repository,
    including name, path and url.
    :rtype: dict
    """

    namespace_group = gl.groups.get(namespace, lazy=True)
    try:
        project = gl.projects.create({
                'name': repo_name,
                'namespace_id': namespace_group.attributes['id']})
    except Exception as ex:
        template = const.EXCEPTION_TEMPLATE
        message = template.format(type(ex).__name__, ex.args)
        print(message)
        return -1
    logging.info('%s [%s] - %s' % (project.attributes['name'],
                 project.attributes['path_with_namespace'],
                 project.attributes['ssh_url_to_repo']))
    return {'name': project.attributes['name'],
            'path': project.attributes['path_with_namespace'],
            'url': project.attributes['ssh_url_to_repo']}


def get_group_id(group_name):
    """
    Retrieves the group id based on the group name given as parameter.
    :param group_name: Name of the group of interest.
    :type group_name: str
    :return: ID of the group given as parameter or -1 in case of a problem.
    :rtype: int
    """
    global login
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
    :return: List of the projects (for the specified group id) containing name,
     id, path and url (in a dictionary-type).
    :rtype: list
    """
    global login
    if group_name == login:
        group_id = 0
        group_projects = gl.projects.list(owned=True)
    else:

        # Retrieve the group's projects
        group_id = get_group_id(group_name)
        try:
            group = gl.groups.get(group_id, lazy=True)
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
        projects.append({
            'name': project.attributes['name'],
            'id': project.attributes['id'],
            'path': project.attributes['path_with_namespace'],
            'url': project.attributes['http_url_to_repo'],
            })
    return projects


def fork_project(project_id):
    """
    Creates a fork of the project given as parameter.
    :param project_id: ID of the project that wants to be forked.
    :type project_id: int
    """

    project = gl.projects.get(project_id, lazy=True)
    try:
        fork = project.forks.create({})
    except Exception as ex:
        template = const.EXCEPTION_TEMPLATE
        message = template.format(type(ex).__name__, ex.args)
        print(message)
        exit(-1)
    logging.info('Forked project id %d' % project_id)
    return fork


def create_merge_request(source_project_id,
                         source_branch,
                         target_project_id,
                         target_branch,
                         title,
                         description):
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
    :return: Returns 0 if successful or -1 if a problem occured.
    :rtype: int
    """

    project = gl.projects.get(source_project_id, lazy=True)
    try:
        mr = project.mergerequests.create({
            'source_branch': 'master',
            'target_branch': 'master',
            'title': title,
            'description': description,
            'target_project_id': target_project_id,
            })
    except Exception as ex:
        template = const.EXCEPTION_TEMPLATE
        message = template.format(type(ex).__name__, ex.args)
        print(message)
        exit(-1)
    logging.info('Creating merge request %s (Description: %s). Source project \
                id/branch: %s - %s. Targer project id/branch: %s - %s' % (
                title,
                description,
                source_project_id,
                'master',
                target_project_id,
                'master'))
    return mr


def get_owned_projects():
    """
    Retrieves the projects owned by the current user.
    :return: List of projects containing name, path and url
    (in a dictionary-type).
    :rtype: dict
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
        logging.info('%s [%s] - %s' % (project.attributes['name'],
                     project.attributes['path_with_namespace'],
                     project.attributes['ssh_url_to_repo']))
        projects.append({
            'name': project.attributes['name'],
            'path': project.attributes['path_with_namespace'],
            'url': project.attributes['ssh_url_to_repo'],
            'username': project.attributes['namespace']['name'],
            'id': project.attributes['id'],
            })

        # if it's a fork add the source project

        if 'forked_from_project' in project.attributes:
            projects[-1]['forked_from_project'] = \
                project.attributes['forked_from_project']
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
        exit(-1)
    return 0


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
    Update the visibility of the projects of all visible groups
    except the groups passed via the excludes parameter
    :param visibility: Visibility setting of the project
    10=internal, 0=private, 20=public - default: 10
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
            result = update_project_visibility(project['id'],
                                               visibility=visibility)
            if result == 0:
                print('Visibility of project %s updated.' %
                      project['name'])
                repository_count += 1
            else:
                print('Problem updating project the \
                      visibility of project %s.' % project['name'])
    logging.info('Number of repositories changed: %d'
                 % repository_count)
    print('Number of repositories changed: %d' % repository_count)


if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)

    if not access_token:
        print(const.NO_GITLAB_TOKEN)

    update_visibility_all_projects(excludes=['remote_data_transfers'])