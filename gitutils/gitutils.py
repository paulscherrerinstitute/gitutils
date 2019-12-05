#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
import logging
import argparse
import textwrap

##### MOVE BACK TO from gitutils import blablabal
import gitlab_utils
import gitutils_exception
import const


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
        gitlab_utils.check_existing_remote_git(clean, git_repository, fork_group_indication)
        # Forks the repo
        new_project = gitlab_utils.fork_project(git_repository_id, fork_group_indication)
        http_url_to_repo = new_project.attributes['http_url_to_repo']
    else:  # cloning into the new repo
        # verify if there is an previously existing local folder
        gitlab_utils.check_existing_local_git(clean, git_repository)
        # verify if there is an previously existing remote folder
        gitlab_utils.check_existing_remote_git(clean, git_repository_id, fork_group_indication)
        try:
            # Forks the repo
            new_project = gitlab_utils.fork_project(git_repository_id, fork_group_indication)
            http_url_to_repo = new_project.attributes['http_url_to_repo']
            http_url_to_original_repo = new_project.attributes[
                'forked_from_project']['http_url_to_repo']
        except Exception as ex:
            raise gitutils_exception.GitutilsError(ex)
        # Clone repository
        os.system('git clone %s' % http_url_to_repo)

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
    parser_fork.add_argument('-g',
                             '--group',
                             help=const.FORK_GROUP_MSG)
    parser_fork.add_argument('-c',
                             '--clean',
                             action=const.STORE_TRUE,
                             help=const.FORK_CLEAN_MSG)

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


    arguments = parser.parse_args()
    # verifies if there are any arguments
    if arguments.command is None:
        parser.print_help()
        sys.exit(-1)
    
    # sets the endpoins
    gitlab_utils.set_endpoint(arguments.endpoint)

    # Authenticate user
    gitlab_utils.authenticate()

    if not arguments.group:
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
                        line = line.rstrip()
                        if next_line is True and git_extracted_repo_name is None:
                            try:
                                git_extracted_repo_name = line.split(
                                    '=')[-1].split('/')[-1].split('.')[0]
                                group_name = line.split('=')[-1].split('/')[-2]
                            except Exception:
                                raise gitutils_exception.GitutilsError(
                                    const.GIT_MERGE_PROBLEM_0)
                        if "[remote \"origin\"]" in line:
                            next_line = True
                if git_extracted_repo_name != repo_name:
                    raise gitutils_exception.GitutilsError(
                        const.GIT_INCONSISTENCY_NAME)
            else:
                raise gitutils_exception.GitutilsError(
                    const.GIT_MERGE_PROBLEM_1)
        # if arguments.group is not None:
        #     group_name = arguments.group
        if group_name is None:
            group_name = gitlab_utils.get_project_group(
                repo_name, False, True, project_indication)
        project_id = gitlab_utils.get_project_id(group_name, repo_name)
    elif arguments.project:
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
