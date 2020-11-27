#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from gitutils import const
from gitutils import gitutils_exception


import requests
import os
import logging
import gitlab
import getpass
import time
import shutil
import pwd
import subprocess
import urllib
import click
import sys
# Gitlab API Documenation: http://doc.gitlab.com/ce/api/
# Python-Gitlab Documetation:
#       https://python-gitlab.readthedocs.io/en/stable/index.html

access_token = None
login = None
password = None
gl = None
user_defined_endpoint = None


def get_gl():
    return gl


def authenticate():
    global gl
    global login
    global password
    global access_token
    # Try to take the access token from the .gitlab_token file
    access_token = parse_access_token()
    # if not existant, authenticate with the user and saves it
    if access_token is None or access_token == "":
        print(const.AUTHENTICATE_REQUEST)
        access_token = get_user_password()

        # saves token into personal file
        save_token(access_token)

        # python-gitlab object
        connect_gl(access_token)
    else:
        # uses the stored token
        try:
            gl = gitlab.Gitlab(get_endpoint(), oauth_token=access_token,
                               api_version=4)
            gl.auth()
            # if successfull, gets the login from the account
            login = pwd.getpwuid(os.getuid())[0]
        except Exception:
            print(const.AUTHENTICATE_REQUEST_INVALID_TOKEN)
            access_token = get_user_password()
            # Tries to authenticate again
            connect_gl(access_token)

            # saves token into personal file
            save_token(access_token)

def get_project(project_id):
    return gl.projects.get(project_id)

def get_project_tree(project_id, branch):
    return get_project(project_id).repository_tree(recursive=True,
            all=True, branch=branch)

def parse_access_token():
    if os.path.isfile(os.path.expanduser('~') + const.GIT_TOKEN_FILE):
        with open(os.path.expanduser('~') + const.GIT_TOKEN_FILE, 'r') as tfile:
            return tfile.read().replace('\n', '')

def check_role(role):
    if role == 'guest':
        return gitlab.GUEST_ACCESS
    elif role == 'reporter':
        return gitlab.REPORTER_ACCESS
    elif role == 'dev':
        return gitlab.DEVELOPER_ACCESS
    elif role == 'maintainer':
        return gitlab.MAINTAINER_ACCESS
    elif role == 'owner':
        return gitlab.OWNER_ACCESS

def check_group_exists(group_name):
    groups = gl.groups.list(search=group_name, all=True)
    if not groups:
        raise gitutils_exception.GitutilsError(const.GROUP_PARAMETER_EMPTY)
    return 0

def group_exists(name):
    group = gl.groups.list(search=name, all=True)
    return bool(group)

def get_group(group_id):
    try:
        group = gl.groups.get(group_id)
    except Exception as e:
        raise gitutils_exception.GitutilsError(const.GROUP_PARAMETER_EMPTY)
    return group

def get_user_id(username):
    user_id = -1
    users = gl.users.list(search=username, all=True)
    for i in users:
        if i.attributes['name'] == username:
            user_id = i.attributes['id']
    return user_id


def project_exists(proj_name):
    project = gl.projects.list(search=project_name, all=True)
    return bool(project)



def check_existing_remote_git(clean, git_repository_id, group_name):
    proj = gl.projects.get(git_repository_id)
    # verifies if such project already exists remotely under
    # any personal project
    projs = get_owned_projects()
    check_exist = False
    id_to_delete = -1
    for own_p in projs:
        if own_p['name'] == proj.name and own_p['username'] == group_name:
            check_exist = True
            id_to_delete = own_p['id']
            break  # If we find something we can abort the loop

    # project exists not clean -> raise error
    if check_exist:
        if not clean:
            raise gitutils_exception.GitutilsError(const.FORK_PROBLEM_REMOTE)
        else:
            # project exists and clean -> clean
            delete_project(id_to_delete)
    # if check_exist is false -> good to go
    return 0

def addldapgroup(git_group_name, group_id, ldap_group_name, role):
    # ldap group must return only one entry
    group = gl.groups.get(group_id)
    try:
        group.add_ldap_group_link(ldap_group_name, role, 'ldapmain')
    except Exception as ex:
        raise gitutils_exception.GitutilsWarning(str(ex))
    # if everything went fine, sync
    print( const.ADDLDAP_SUCCESS_MSG % (
        const.bcolors.BOLD,
        ldap_group_name,
        const.bcolors.ENDC,
        const.bcolors.BOLD,
        role,
        const.bcolors.ENDC,
        const.bcolors.BOLD,
        git_group_name,
        group_id,
        const.bcolors.ENDC,
        ))
    group.ldap_sync()

def get_ldap_groups(ldap_cn):
    return gl.ldapgroups.list(all=True, search=ldap_cn)

def check_existing_local_git(clean, git_repository):
    # verify if there is an previously existing local folder
    if os.path.exists('./' + git_repository) and clean:
        # Try to remove tree directory; if failed show an error using
        # try...except on screen
        print(const.DELETING_LOCAL_STORAGE)
        try:
            shutil.rmtree(git_repository)
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))
    elif os.path.exists('./' + git_repository):
        raise gitutils_exception.GitutilsError(const.FORK_PROBLEM_FOLDER)


def get_user_password():
    global login
    global password
    login = input(const.LOGIN_REQUEST)
    password = getpass.getpass(prompt=const.PASSWORD_REQUEST)
    try:
        access_token = oauth_authentication()['access_token']
    except Exception as ex:
        raise gitutils_exception.GitutilsError(ex)
    return access_token


def connect_gl(access_token):
    global gl
    try:
        gl = gitlab.Gitlab(get_endpoint(), oauth_token=access_token,
                           api_version=4)
        gl.auth()
    except Exception as ex:
        raise gitutils_exception.GitutilsError(ex)


def save_token(access_token):
    if access_token:
        with open(os.path.expanduser('~') + const.GIT_TOKEN_FILE, 'w'
                  ) as tfile:
            tfile.write(access_token)
        os.chmod(os.path.expanduser('~') + const.GIT_TOKEN_FILE, 0o600)


def set_endpoint(endpoint):
    global user_defined_endpoint
    user_defined_endpoint = endpoint


def get_endpoint():
    global user_defined_endpoint
    return user_defined_endpoint


def get_username():
    """
    Gets the username used for authentication.
    :return: Username
    :rtype: str
    """
    global login
    return login

def is_empty(any_structure):
    if any_structure:
        return False
    else:
        return True

def verify_token():
    global gl
    if is_empty(gl.groups.list()):
        print(const.LOGIN_PROBLEM)
    else:
        print(const.LOGIN_SUCCESS)

def oauth_authentication():
    """
    Requests oauth authentication for the current user and login provided to be
    able to perform git operations.
    :return: Dictionary containing details of the authentication request
    (access_token, toke_type, refresh_token, scope and created_at)
    :rtype: dict
    """
    return requests.post(const.OATH_REQUEST + urllib.parse.quote(get_username()) +
                         const.PASSWORD_URL + urllib.parse.quote(password)).json()


def get_groups():
    """
    Retrieves all the groups of the current user.
    :return: Dictionary containing details of the groups (name and id).
    :rtype: dict
    """
    groups = gl.groups.list(all=True)
    return create_group_dict(groups)


def create_group_dict(groups):
    groups_dict = dict()
    for group in groups:
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

    projects_list = gl.projects.list(all=True)
    return get_dict_from_own_projects(projects_list)

def create_project(group_id, project_name):
    project = gl.projects.create({'name': project_name, 'namespace_id': group_id})
    return project

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
        gl.groups.create({'name': group_name,
                          'path': group_name,
                          'description': description})
    except Exception as ex:
        raise gitutils_exception.GitutilsError(ex)
    return exitCode

def print_search_output(group_indication, file_name, results):
    if results:
        # For each result
        for idx,i in enumerate(results):
            # states the file name
            print(const.bcolors.BOLD,str(idx+1),") ",const.bcolors.OKGREEN, file_name, const.bcolors.ENDC, ":\n")
            # group
            print("\t\t Group: "+group_indication)
            # project (project id)
            print("\t\t Project: "+i.get('project_name')+" (id "+ str(i.get('project_id'))+")")
            # branch
            print("\t\t Branch: "+i.get('branch'))
            # path
            print("\t\t Path: "+i.get('path'))
            # direct weblink
            print("\n\t\t Weblink: "+const.bcolors.UNDERLINE+i.get('webpath')+const.bcolors.ENDC)
            print("\n")
    else:
        # Empty search
        print(const.SEARCHFILE_EMPTY % (const.bcolors.FAIL, file_name, const.bcolors.ENDC))


def print_grep_output(group_name, project_name, project_id, search_term, result):
    # States the search_term
    print("\nGroup: ",group_name, "\n",const.bcolors.BOLD,const.bcolors.OKGREEN, search_term, const.bcolors.ENDC, ":\n")
    # direct weblink to such file
    print("\t Weblink: "+const.bcolors.UNDERLINE+result.get('webpath')+const.bcolors.ENDC)
    # removal of empty spaces at the beginning of lines
    print("")
    stopwords = ['']
    resultwords  = [word for word in result.get('excerpt').splitlines() if word not in stopwords]
    # for each line
    for line in resultwords:
        # verifies if this is the line containing the search_term
        if search_term in line:
            # color green
            b = line.split(search_term)
            print("\t\t"+b[0]+const.bcolors.OKGREEN+search_term+const.bcolors.ENDC+b[1])
        else:
            # color regular
            print("\t\t"+line)
    print("\n\n")

def grep_file_in_project(search_term, project_id, project_name, group_name):
    results =[]
    # Gets the project and searches in its file for the search_term
    project_search_results = get_project(project_id).search(const.BLOBS, search_term)
    for match in project_search_results:
        results.append({
            # File name, including path
            'filename':match.get('filename'),
            # 3 lines surrounding the search_term
            'excerpt':match.get('data'),
            # Generation of the diret weblink to the file including the line
            'webpath': const.ENDPOINT+"/"+group_name+"/"+project_name+"/blob/"+match.get('ref')+"/"+match.get('filename')+"#L"+str(match.get('startline'))
        })
    return results


def find_file_by_id(file_name,group_dict,files_only):
    results_file =[]
    results_blob =[]
    # gets all the projects in the group
    if group_dict['name']!='sandbox':
        projects = get_group_projects_by_group_id(group_dict['id'])
        match_files = []
        # for every project found
        for i in projects:
            # For every project's branch
            if not files_only:
                branches = i.get('branches', 0)
                if branches != 0:
                    for b in i['branches']:
                        # gets the project tree for the branch
                        project_tree = get_project_tree(i.get('id'), b.name)
                        for j in project_tree:
                            if file_name == j.get('name'):
                                results_file.append({
                                    'webpath':const.ENDPOINT+"/"+group_dict['name']+"/"+i.get('name')+"/"+j.get('type')+"/"+b.name+"/"+j.get('path'),
                                    'branch':b.name,
                                    'path':j.get('path'),
                                    'project_name':i.get('name'),
                                    'project_id': i.get('id')
                                })
                if len(results_file) > 0 :
                    print_search_output(group_dict['name'], file_name, results_file)
            # Gets the project and searches in its file for the search_term
            project_search_results = get_project(i.get('id')).search(const.BLOBS, file_name)
            for match in project_search_results:
                not_add = False
                for entry in results_blob:
                    if entry['filename'] == match.get('filename'):
                        not_add = True
                if not not_add:
                    results_blob = {
                        # File name, including path
                        'filename':match.get('filename'),
                        # 3 lines surrounding the search_term
                        'excerpt':match.get('data'),
                        # Generation of the diret weblink to the file including the line
                        'webpath': const.ENDPOINT+"/"+group_dict['name']+"/"+i.get('name')+"/blob/"+match.get('ref')+"/"+match.get('filename')+"#L"+str(match.get('startline'))
                    }
            if len(results_blob) > 0:
                if results_blob.get('webpath') not in match_files:
                    match_files.append(results_blob.get('webpath'))
                    print_grep_output(group_dict['name'], i['name'], i['id'], file_name, results_blob)
    return 

def find_file(file_name,group_indication):
    results =[]
    # gets all the projects in the group
    projects = get_group_projects(group_indication)
    # for every project found
    for i in projects:
        # For every project's branch
        for b in i['branches']:
            # gets the project tree for the branch
            project_tree = get_project_tree(i.get('id'), b.name)
            for j in project_tree:
                if file_name == j.get('name'):
                    results.append({
                        'webpath':const.ENDPOINT+"/"+group_indication+"/"+i.get('name')+"/"+j.get('type')+"/"+b.name+"/"+j.get('path'),
                        'branch':b.name,
                        'path':j.get('path'),
                        'project_name':i.get('name'),
                        'project_id': i.get('id')
                    })
    return results

def get_project_web_url(project_name):
    """
    Function to get the web_url attribute of a project based on its name.
    :param project_name: Name of the project
    :type project_name: str
    :return: Returns the web url to the project.
    :rtype: str
    """
    projects_list = gl.projects.list(search=project_name, all=True)
    for project in projects_list:
        if project_name == project.attributes['name']:
            return project.attributes['web_url']
    raise gitutils_exception.GitutilsError(const.PROJECT_NAME_NOT_FOUND)


def check_key(dict_to_search, key):
    if key in dict_to_search:
        return True
    else:
        return False

def get_project_group_simplified(project_name):
    projects_list = gl.projects.list(search=project_name, all=True)
    list_of_groups = []
    for project in projects_list:
        if project_name == project.attributes['name']:
            project_path = project.attributes['path_with_namespace']
            # verify if it's a personal project
            groupFound = project_path.split('/')[0]
            list_of_groups.append(groupFound)
    if len(list_of_groups) == 1:
        return groupFound
    elif len(list_of_groups) >= 2:
        # if there is a personal group
        if get_username() in list_of_groups:
            print("\nGitutils warning: "+const.GROUP_NOT_SPECIFIED_ASSUME_USER)
            return get_username()
        else:
            raise gitutils_exception.GitutilsError(
                const.MULTIPLE_PROJECTS % (list_of_groups))
    raise gitutils_exception.GitutilsError(const.PROJECT_NAME_NOT_FOUND)

def get_project_group(project_name, clean, merge, project_indication):
    """
    Function to get the group of a project based on its name.
    :param project_name: Name of the project
    :type project_name: str
    :return: Returns the name of the group.
    :rtype: str
    """
    projects_list = gl.projects.list(search=project_name, all=True)
    list_of_groups = []
    for project in projects_list:
        if project_name == project.attributes['name']:
            if merge:
                if check_key(project.attributes, 'forked_from_project'):
                    groupFound = \
                        project.attributes['path_with_namespace'].split('/')[0]
                    list_of_groups.append(groupFound)
            elif not merge:
                project_path = project.attributes['path_with_namespace']
                # verify if it's a personal project
                if project_path.split('/')[0] == get_username():
                    # if it's personal, it should be cleaned
                    if clean:
                        delete_project(project.attributes['id'])
                    else:
                        raise gitutils_exception.GitutilsError(
                            const.GIT_FORK_PROBLEM_MULTIPLE)
                else:  # not a personal project
                    groupFound = project_path.split('/')[0]
                    list_of_groups.append(groupFound)
    if len(list_of_groups) == 1 and project_indication:
        return groupFound
    elif len(list_of_groups) >= 2:
        # if there is a personal group
        if get_username() in list_of_groups:
            print("Gitutils warning: "+const.GROUP_NOT_SPECIFIED_ASSUME_USER)
            return get_username()
        else:
            raise gitutils_exception.GitutilsError(
                const.MULTIPLE_PROJECTS % (list_of_groups))
    if not project_indication:
        raise gitutils_exception.GitutilsError(const.PROJECT_NAME_NOT_FOUND)


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
    forked_project = None
    projects = get_owned_projects()
    for project in projects:
        if project['username'] == get_username() \
                and project['name'] == git_repository \
                and 'forked_from_project' in project:

            # check if project is forked from the right project
            if project['forked_from_project']['name'] == git_repository:
                forked_project = project
                break
            else:
                raise gitutils_exception.GitutilsError(
                    const.PROJECT_FORK_NAME_ERROR)
        else:
            raise gitutils_exception.GitutilsError(
                const.PROJECT_FOUND_NOT_FORK)
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
        raise gitutils_exception.GitutilsError(
            const.GIT_UNABLE_TO_FIND_MASTER_BRANCH %
            project['name'])


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
    projects_list = gl.projects.list(search=project_name,all=True)
    for project in projects_list:
        if project.attributes['name'] == project_name and group_name == project.attributes['path_with_namespace'].split(
                '/')[0]:
            logging.info('Found the project id ( %s - %s ) : %s' % (
                group_name, project_name,
                project.attributes['id']))
            return project.attributes['id']
    raise gitutils_exception.GitutilsError(const.PROJECT_ID_NOT_FOUND)


def get_repo_group_names(config, group_indication, clean=False):
    """
    Gets the project name and group name based on the argument given on the cli.
    :param config: String given as argument that can be of different
    formats: full path to the project, groupname/projectname or project name.
    :type config: str
    :return: Returns the project name, group name and a boolean indicating
    if the results are valid.
    :rtype: tuple
    """

    repo_name = None
    group_name = group_indication
    valid = False
    if len(config) > 0:
        project_indication = True
    # config format: "const.ENDPOINT/group_name/project_name"
    if get_endpoint() in config:
        web_url = config
        web_url_split = web_url.split('/')
        if len(web_url_split) == 5:
            repo_name = web_url_split[-1]
            group_name = web_url_split[-2]
            if len(repo_name) <= 1 or len(group_name) <= 1:
                raise gitutils_exception.GitutilsError(
                    const.FULL_GROUP_PROJECT_BAD_FORMAT)
            valid = True
            get_project_group(repo_name, clean, False, project_indication)
        else:
            raise gitutils_exception.GitutilsError(
                const.FULL_GROUP_PROJECT_BAD_FORMAT)
    elif '/' in config:
        # config format: "group_name/project_name"
        path_with_namespace = config.split('/')
        if len(path_with_namespace) == 2:
            group_name = path_with_namespace[0]
            repo_name = path_with_namespace[1]
            valid = True
            project_id = get_project_id(group_name, repo_name)
            project = gl.projects.get(project_id)
            if group_name != project.attributes['namespace']['name']:
                raise gitutils_exception.GitutilsError(
                    const.FORK_GROUP_NOT_FOUND)
            if clean:
                own_projects = get_owned_projects()
                for proj in own_projects:
                    if proj['name'] == repo_name and group_indication == project.attributes['namespace']['name']:
                        delete_project(proj['id'])
        else:
            raise gitutils_exception.GitutilsError(
                const.GROUP_PROJECT_BAD_FORMAT)
    else:
        # config format: "project_name"
        repo_name = config
        group_name = get_project_group(
            repo_name, clean, False, project_indication)
        # warning if multiple and ERROR out - > ambiguous
        valid = True
    project_id = get_project_id(group_name, repo_name)
    return (repo_name, group_name, project_id, valid)


def is_git_repo():
    is_git_repo = subprocess.check_output(
        const.GIT_IS_REPO_PATH,
        shell=True).decode('UTF-8').split('\n')[0]
    if 'true' in is_git_repo:
        raise gitutils_exception.GitutilsError(const.FORK_PROBLEM_GIT_FOLDER)


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
        print(ex)
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
        raise gitutils_exception.GitutilsError(ex)
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
    group_id = -1
    # it could be a personal group -> group name == username
    try:
        group_id = gl.groups.get(group_name).attributes['id']
    except Exception as ex:
        # group not found, it should be a personal group
        try:
            group_id = gl.users.list(username=group_name, all=True)[0].attributes['id']
        except Exception as ex:
            raise gitutils_exception.GitutilsError("Group not found.")
    if group_id != -1:
        logging.info('Group name: %s (id %s)' % (group_name, group_id))
    return group_id


def get_group_projects_by_group_id(group_id):
    """
    Retrieves all the projects of a group, which is given as parameter.
    :param group_name: ID (int) of the group of interest.
    :type group_id: int
    :return: List of the projects (for the specified group id) containing name,
     id, path and url (in a dictionary-type).
    :rtype: list
    """
    try:
        group = gl.groups.get(group_id)
        group_projects = group.projects.list(all=True)
    except Exception as ex:
        raise gitutils_exception.GitutilsError(ex)
    return get_dict_from_own_projects(group_projects)


def get_group_projects(group_name):
    """
    Retrieves all the projects of a group, which is given as parameter.
    :param group_name: Name of the group of interest.
    :type group_id: str
    :return: List of the projects (for the specified group id) containing name,
     id, path and url (in a dictionary-type).
    :rtype: list
    """
    if group_name == get_username():
        group_id = 0
        group_projects = gl.projects.list(owned=True, all=True)
        return get_dict_from_own_projects(group_projects)
    # Retrieve the group's projects
    group_id = get_group_id(group_name)
    try:
        group = gl.groups.get(group_id)
        group_projects = group.projects.list(all=True)
    except Exception as ex:
        try:
            user = gl.users.list(username=group_name, all=True)[0]
            group_projects = user.projects.list(all=True)
        except Exception as ex:
            raise gitutils_exception.GitutilsError(ex)
    return get_dict_from_own_projects(group_projects)


def fork_project(project_id, group_indication):
    """
    Creates a fork of the project given as parameter.
    :param project_id: ID of the project that wants to be forked.
    :type project_id: int
    """
    project = gl.projects.get(project_id)
    try:
        if group_indication != get_username():
            fork = project.forks.create({'namespace': group_indication})
        else:
            fork = project.forks.create({})
    except Exception as ex:
        print(ex)
        if ex.error_message['path'][0] == const.GIT_PATHNAME_IS_TAKEN:
            raise gitutils_exception.GitutilsError(const.FORKED_EXISTS)
        else:
            raise gitutils_exception.GitutilsError(ex)

    logging.info(
        'Adding 3 seconds of idle time after forking to let the server process the new fork.')
    time.sleep(4)
    logging.info('Forked project id %d' % project_id)
    return fork


def create_merge_request(source_tuple,
                         target_tuple,
                         merge_def):
    """
    Creates a merge request based on the parameters given.
    :param source_tuple: Tuple from the source project containing id and source branch
    :type source_tuple: tuple
    :param target_tuple: Tuple from the target project containing id and source branch
    :type target_tuple: tuple
    :param merge_def: Definition of the new merge request containing title and description
    :type merge_def: tuepl
    :return: Returns 0 if successful or -1 if a problem occured.
    :rtype: int
    """

    project = gl.projects.get(source_tuple[0], lazy=True)
    try:
        mr = project.mergerequests.create({
            'source_branch': 'master',
            'target_branch': 'master',
            'title': merge_def[0],
            'description': merge_def[1],
            'target_project_id': target_tuple[0],
        })
    except Exception as ex:
        if const.MERGE_DUPLICATED in ex.error_message[0]:
            raise gitutils_exception.GitutilsDebug(const.MERGE_DUPLICATED)
        raise gitutils_exception.GitutilsError(ex)

    logging.info('Creating merge request %s (Description: %s). Source project \
                id/branch: %s - %s. Targer project id/branch: %s - %s' % (
        merge_def[0],
        merge_def[1],
        source_tuple[0],
        'master',
        target_tuple[0],
        'master'))
    return mr


def get_dict_from_own_projects(own_projects):
    dict_projects = []
    for project in own_projects:
        branches = ""

        dict_projects.append({
            'name': project.attributes['name'],
            'path': project.attributes['path_with_namespace'],
            'url': project.attributes['ssh_url_to_repo'],
            'username': project.attributes['namespace']['name'],
            'id': project.attributes['id'],
        })
        if len(get_project(project.attributes['id']).branches.list()) > 0:
            branches = get_project(project.attributes['id']).branches.list()
            dict_projects[-1]['branches'] = branches
        
        # if it's a fork add the source project
        if 'forked_from_project' in project.attributes:
            dict_projects[-1]['forked_from_project'] = \
                project.attributes['forked_from_project']
    return dict_projects

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
        raise gitutils_exception.GitutilsError(ex)
    return get_dict_from_own_projects(own_projects)


def delete_project(project_id):
    """
    Deletes the project given as parameter
    :return:
    """
    # check if the project id is owned by user
    proj_list = get_dict_from_own_projects(gl.projects.list(owned=True))
    check_allowed = False
    for i in proj_list:
        if i['id'] == project_id and i['path'].split('/')[0] == get_username():
            check_allowed = True
    if check_allowed:
        try:
            gl.projects.delete(project_id)
        except Exception as ex:
            raise gitutils_exception.GitutilsError(ex)
        print(const.DELETE_SUCCESS)
        time.sleep(4)
    else:
        print(const.NO_PERSONAL_FORK_PERMISSIONS, )
        if click.confirm('Do you want to continue?', default=True):
            try:
                gl.projects.delete(project_id)
            except Exception as ex:
                raise gitutils_exception.GitutilsError(ex)
            print(const.DELETE_SUCCESS)
            time.sleep(4)
        else:
            raise gitutils_exception.GitutilsError(const.NO_PERSONAL_FORK)
    return 0
