#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
import logging
import argparse
import textwrap
import time

from gitutils import gitlab_utils
from gitutils import gitutils_exception
from gitutils import const
from gitutils.spinner import Spinner

def find(search_term):
    """
    Find command searches in all projects/repositories.
    :param search_term: Term to search in the content of files and filenames.
    :type search_term: str
    :return:
    """
    print(const.GREPFILE_INIT_MSG % (const.bcolors.BOLD, search_term, const.bcolors.ENDC))
    # get groups
    groups = gitlab_utils.get_groups()
    results_group = []
    # search for files in groups
    for group in groups:
        if groups[group]['name'] != 'sandbox':
            gitlab_utils.find_file_by_id(search_term,groups[group])
        

def grep(group_name, project_name, project_id, search_term):
    """
    Grep command searches in filenames and content for a term in a specific project.
    :param group_name: Name of the group.
    :type group_name: str
    :param project_name: Name of the project.
    :type project_name: str
    :param project_id: Id of the project.
    :type project_id: int
    :param search_term: Term to search in the content of files and filenames.
    :type search_term: str
    :return:
    """
    # Initial message
    print(const.GREPFILE_INIT_MSG % (const.bcolors.BOLD, project_name, const.bcolors.ENDC, const.bcolors.BOLD, search_term, const.bcolors.ENDC))
    # Gets all the projects from the specified group and gets the results
    with Spinner():
        results = gitlab_utils.grep_file_in_project(search_term, project_id,project_name,group_name)
    # Display the results
    gitlab_utils.print_grep_output(project_name, project_id, search_term, results)

def search(group_indication, file_name):
    """
    Search command searches for filenames inside a specified group.
    :param group_indication: Name of the group.
    :type group_indication: str
    :param file_name: Name of the file to be searched.
    :type file_name: str
    :return:
    """
    # Initial message
    print(const.SEARCHFILE_INIT_MSG % (const.bcolors.BOLD, group_indication, const.bcolors.ENDC, const.bcolors.BOLD, file_name, const.bcolors.ENDC))
    # # Gets all the projects from the specified group and gets the results
    with Spinner():
        results = gitlab_utils.find_file(file_name, group_indication)
    # Display the results
    gitlab_utils.print_search_output(group_indication, file_name, results)

def fork(
        fork_group_indication='',
        git_repository_id=None,
        git_repository='',
        no_clone=False,
        clean=False):
    """
    Creates a fork repository of the repository given as parameter.
    :param git_repository_id: Id of the repository to be pulled.
    :type git_repository_id: int
    :param git_repository: Name of the repository to be pulled.
    :type git_repository: str
    :param no_clone: Flag to clone or not the forked repository.
    :type no_clone: bool
    :param clean: Flag to clean or not the previously existing repository.
    :type clean: bool
    :return:
    """
    # checks if fork is executed inside git repo
    # gitlab_utils.is_git_repo()
    # Message user about forking project
    print(const.FORK_PROJECT % (git_repository, git_repository_id))
    # not cloning into the new repo
    if no_clone:
        # verify if there is an previously existing remote folder
        gitlab_utils.check_existing_remote_git(clean, git_repository_id, fork_group_indication)
        # Forks the repo
        new_project = gitlab_utils.fork_project(git_repository_id, fork_group_indication)
        # http_url_to_repo = new_project.attributes['http_url_to_repo']
    else:  # cloning into the new repo
        # verify if there is an previously existing local folder
        gitlab_utils.check_existing_local_git(clean, git_repository)
        # verify if there is an previously existing remote folder
        gitlab_utils.check_existing_remote_git(clean, git_repository_id, fork_group_indication)
        try:
            # Forks the repo
            new_project = gitlab_utils.fork_project(git_repository_id, fork_group_indication)
            ssh_url_to_repo = new_project.attributes['ssh_url_to_repo']
            http_url_to_original_repo = new_project.attributes[
                'forked_from_project']['http_url_to_repo']
        except Exception as ex:
            raise gitutils_exception.GitutilsError(ex)
        # Clone repository

        time.sleep(2) # waiting another 2 seconds before cloning - AFS gitserver issue
        os.system('git clone %s' % ssh_url_to_repo)

        # Change into git repository
        try:
            os.chdir(git_repository)
        except Exception as ex:
            raise gitutils_exception.GitutilsError(ex)

        # Add upstream repository
        # Configure Git to sync your fork with the original repository
        try:
            os.system('git remote add upstream %s' % http_url_to_original_repo)
        except Exception as ex:
            print(const.GIT_UPLINK_PROBLEM % http_url_to_original_repo)
    info_msg = 'New project forked: [%s] (id: %s) - %s' % (
        new_project.attributes['path_with_namespace'],
        new_project.attributes['id'],
        new_project.attributes['http_url_to_repo'])

    logging.info(info_msg)
    print(info_msg)

def clonegroup(group_name=''):
    """
    Based on the group name, it clones all existing
    projects from the specified group.
    : param group_name : Name of group to be cloned
    : type group_name : str
    """
    # check if group exists
    gitlab_utils.check_group_exists(group_name)
    # Gets all the projects from the group
    projects = gitlab_utils.get_group_projects(group_name)
    # clones all the projects from group
    for i in projects:
        # clones into repo
        os.system('git clone %s' % i['url'])
        # 2 sec sleep time in between:
        # Gitlab API refuses if there's no sleep in between
        # error: ssh_exchange_identification: read: Connection reset by peer
        time.sleep(2)
    # Finishing up, message to user
    print("All projects have been cloned. Exiting now...")

def merge(git_repository='',
          git_repository_id='',
          description='',
          title=''):
    """
    Creates a merge request to merge a forked repository.
    :param git_group_id: Id of the group to be pulled from.
    :type git_group_id: int
    :param git_repository: Name of the repository to be pulled.
    :type git_repository: str
    :param description: Description of the merge request.
    :type description: str
    :param title: Title of the merge request.
    :type title: str
    :return:
    """

    git_username = gitlab_utils.get_username()
    if git_username == -1:
        raise gitutils_exception.GitutilsError(const.PROBLEM_USERNAME)

    # Check if there is already a fork
    forked_project = gitlab_utils.get_forked_project(git_repository,
                                                     git_repository_id)
    # If no title submitted by the user, default title
    if title is None:
        title = const.MERGE_DEFAULT_TITLE % gitlab_utils.get_username()

    if forked_project is None:
        raise gitutils_exception.GitutilsError(const.GIT_MERGE_PROBLEM_2)
    else:
        print(const.GIT_CREATE_MERGE_MSG)
        final_description = const.GIT_MERGE_DESCRIPTION_MSG \
            % git_username
        if description is not None:
            final_description += ' User description: ' + description

        # Merge will be from source and target masters branches
        source_branch = 'master'
        target_branch = 'master'

        merge_request = gitlab_utils.create_merge_request(
            (git_repository_id, source_branch),
            (forked_project['forked_from_project']['id'], target_branch),
            (title, final_description))

        if merge_request.attributes['id']:
            print(const.GIT_MERGE_SUCCESS
                  % (merge_request.attributes['id'],
                     merge_request.attributes['created_at']))


def main():
    """
    Main function for gitutils that parses the arguments and
    calls the corresponding method. It is in charge of detecting
    important parameters based on the arguments and treat some
    of the possible errors that might occur.
    """


    ############
    # GITUTILS #
    ############

    parser = argparse.ArgumentParser(
        description=const.GITUTILS_TITLE_DESCRIPTION,
        formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-e', '--endpoint',
                        help=const.ENDPOINT_HELP_MSG,
                        default=const.ENDPOINT)

    subparsers = parser.add_subparsers(title='command',
                                       description='valid commands',
                                       dest='command',
                                       help='commands')

    ############
    # FORK CMD #
    ############

    parser_fork = subparsers.add_parser('fork',
                                        help=const.FORK_HELP_MSG,
                                        formatter_class=argparse.RawTextHelpFormatter)

    parser_fork.add_argument('-n',
                             '--no_clone',
                             action=const.STORE_TRUE,
                             help=const.FORK_NOCLONE_HELP)

    parser_fork.add_argument('-c',
                             '--clean',
                             action=const.STORE_TRUE,
                             help=const.FORK_CLEAN_MSG)

    parser_fork.add_argument('-g',
                             '--group',
                             help=const.FORK_GROUP_MSG)

    parser_fork.add_argument('project', nargs=1, metavar='project',
                             help=textwrap.dedent(const.FORK_PROJECT_MESSAGE))

    #############
    # MERGE CMD #
    #############

    parser_mr = subparsers.add_parser('merge',
                                      help=const.MERGE_HELP_MSG,
                                      formatter_class=argparse.RawTextHelpFormatter)
    parser_mr.add_argument('-t',
                           '--title',
                           help=const.MERGE_MESSAGE_TITLE)

    parser_mr.add_argument('-p',
                           '--project',
                           help=const.MERGE_PROJECT_MESSAGE)

    parser_mr.add_argument('-d',
                           '--description',
                           help=const.MERGE_MESSAGE_DESCRIPTION)

    ###############
    # SEARCH FILE #
    ###############
    parser_sf = subparsers.add_parser('search',
                                    help=const.SEARCHFILE_HELP_MSG,
                                    formatter_class=argparse.RawTextHelpFormatter)
    parser_sf.add_argument('group', nargs=1, metavar='group',
                             help=textwrap.dedent(const.SEARCHFILE_GROUP_MSG))
    parser_sf.add_argument('file', nargs=1, metavar='file',
                             help=textwrap.dedent(const.SEARCHFILE_FILE_MSG))

    #############
    # GREP TERM #
    #############
    parser_grep = subparsers.add_parser('grep',
                                    help=const.GREPFILE_HELP_MSG,
                                    formatter_class=argparse.RawTextHelpFormatter)
    parser_grep.add_argument('project', nargs=1, metavar='project',
                             help=textwrap.dedent(const.GREP_PROJECT_MSG))
    parser_grep.add_argument('term', nargs=1, metavar='term',
                             help=textwrap.dedent(const.GREP_TERM_MSG))

    ########
    # FIND #
    ########
    parser_find = subparsers.add_parser('find',
                                    help=const.FIND_HELP_MSG,
                                    formatter_class=argparse.RawTextHelpFormatter)
    parser_find.add_argument('term', nargs=1, metavar='term',
                             help=textwrap.dedent(const.GREP_TERM_MSG))

    ###################
    # CLONE GROUP CMD #
    ###################

    parser_cg = subparsers.add_parser('clonegroup',
                                      help=const.CLONEGROUP_HELP_MSG,
                                      formatter_class=argparse.RawTextHelpFormatter)

    parser_cg.add_argument('group', nargs=1, metavar='group',
                             help=textwrap.dedent(const.CLONEGROUP_GROUP_NAME))

    #############
    # LOGIN CMD #
    #############

    subparsers.add_parser('login',
                        help=const.LOGIN_HELP_MSG,
                        formatter_class=argparse.RawTextHelpFormatter)

    arguments = parser.parse_args()
    # verifies if there are any arguments
    if arguments.command is None:
        parser.print_help()
        sys.exit(-1)

    # sets the endpoins
    gitlab_utils.set_endpoint(arguments.endpoint)

    # Authenticate user
    gitlab_utils.authenticate()

    if arguments.command == 'fork' and not arguments.group:
        arguments.group = gitlab_utils.get_username()

    # retrieve repository and group names
    (repo_name, group_name, project_id) = (None, None, None)
    if arguments.command == 'merge':
        # Verify if project has been indicated
        project_indication = False
        repo_name = os.path.basename(os.getcwd())
        if arguments.project:
            project_indication = True
            if const.ENDPOINT in arguments.project:
                web_url_split = arguments.project.split('/')
                if len(web_url_split) == 5:
                    repo_name = web_url_split[-1]
                    group_name = web_url_split[-2]
            elif '/' in arguments.project:
                # config format: "group_name/project_name"
                path_with_namespace = arguments.project.split('/')
                if len(path_with_namespace) == 2:
                    repo_name = path_with_namespace[1]
                    group_name = path_with_namespace[0]
            else:
                repo_name = arguments.project
        else:
            # Check to see the directory
            if os.path.isfile('.git/config'):
                next_line = False
                git_extracted_repo_name = None
                with open(".git/config") as git_search:
                    for line in git_search:
                        line = line.strip()
                        if next_line is True and git_extracted_repo_name is None:

                            if not line.startswith("url ="):
                                # go to next line
                                continue

                            # Detect if ssh or http has been used to clone
                            if const.SSH_GIT_GIT in line:
                                try:
                                    group_name = line.split('=')[-1].split(
                                        '/')[0].split(':')[-1]
                                    git_extracted_repo_name = line.split('=')[-1].split(
                                        '/')[-1][:-4]
                                except:
                                    raise gitutils_exception.GitutilsError(
                                        const.GIT_MERGE_PROBLEM_0)
                            else:
                                try:
                                    git_extracted_repo_name = line.split(
                                        '=')[-1].split('/')[-1].split('.')[0]
                                    group_name = line.split('=')[-1].split('/')[-2]
                                except Exception:
                                    raise gitutils_exception.GitutilsError(
                                        const.GIT_MERGE_PROBLEM_0)
                            break
                        if "[remote \"origin\"]" in line:
                            next_line = True
                if git_extracted_repo_name != repo_name:
                    raise gitutils_exception.GitutilsError(
                        const.GIT_INCONSISTENCY_NAME)
            else:
                raise gitutils_exception.GitutilsError(
                    const.GIT_MERGE_PROBLEM_1)

        if group_name is None:
            group_name = gitlab_utils.get_project_group(
                repo_name, False, True, project_indication)
        project_id = gitlab_utils.get_project_id(group_name, repo_name)
    elif arguments.command == 'login':
        # login/user has already been requested and token retrieved
        # verifies if access if correctly done
        print(const.LOGIN_TEST)
        gitlab_utils.verify_token()
    elif arguments.command == 'clonegroup':
        if not arguments.group:
            print(const.CLONEGROUP_PROBLEM)
            sys.exit(-1)
        repo_name = 'all'
        group_name = arguments.group[0]
        project_id = 'all'
    elif arguments.command == 'search':
        if not arguments.group or not arguments.file:
            print(const.SEARCHFILE_PROBLEM)
            sys.exit(-1)
        repo_name = 'all'
        group_name = arguments.group[0]
        project_id = 'all'
    elif arguments.command == 'find':
        repo_name = 'all'
        group_name = 'all'
        project_id = 'all'
    elif arguments.command == 'grep':
        if not arguments.project or not arguments.term:
            print(const.GREPFILE_PROBLEM)
            sys.exit(-1)
        # Initially we assume there's no group indication
        repo_name = arguments.project[0]
        # if there's group indication
        if '/' in repo_name:
            group_name = repo_name.split('/')[0]
            repo_name = repo_name.split('/')[1]
        else:
            group_name = gitlab_utils.get_project_group_simplified(repo_name)
        project_id = gitlab_utils.get_project_id(group_name, repo_name)
    elif arguments.project and arguments.command == 'fork':
        (repo_name, group_name, project_id, valid) = gitlab_utils.get_repo_group_names(
            arguments.project[0], arguments.group, arguments.clean)

        # if project is personal, needs to be deleted
        if group_name == gitlab_utils.get_username():
            if arguments.clean:
                gitlab_utils.delete_project(project_id)
                (repo_name, group_name, project_id, valid) = gitlab_utils.get_repo_group_names(
                    arguments.project, False)
            else:
                print(const.FORK_PROBLEM_PERSONAL)
                parser.print_help()
                sys.exit(-1)
        if not valid:
            print(const.PROBLEM_FETCHING_NAME)
            parser.print_help()
            sys.exit(-1)
    else:
        parser.print_help()
        sys.exit(-1)

    # Command, group and repo are ok
    if arguments.command and \
        repo_name is not None and \
        group_name is not None and \
        project_id is not None:
        try:
            if arguments.command == 'fork':
                fork(fork_group_indication=arguments.group,
                    git_repository_id=project_id,
                    git_repository=repo_name,
                    no_clone=arguments.no_clone,
                    clean=arguments.clean)
            elif arguments.command == 'merge':
                merge(git_repository=repo_name,
                    git_repository_id=project_id,
                    description=arguments.description,
                    title=arguments.title)
            elif arguments.command == 'clonegroup':
                clonegroup(group_name=group_name)
            if arguments.command == 'find':
                find(arguments.term[0])
            elif arguments.command == 'search':
                search(group_name, arguments.file[0])
            elif arguments.command == 'grep':
                grep(group_name, repo_name, project_id, arguments.term[0])
            else:
                print(const.COMMAND_NOT_FOUND)
                parser.print_help()
                exit(-1)
        except Exception as e:
            print(str(e))
    else:
        parser.print_help()
        exit(-1)


if __name__ == '__main__':
    main()
