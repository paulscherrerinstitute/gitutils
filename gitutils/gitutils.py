#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from gitutils import gitlab_utils
from gitutils import gitutils_exception
from gitutils import const
import sys
import os
import time
import shutil
import logging
import argparse
import textwrap

def fork(git_repository_id=None, git_repository='', no_clone=False, clean=False):
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
        # Forks the repo
        new_project = gitlab_utils.fork_project(git_repository_id)
        http_url_to_repo = new_project.attributes['http_url_to_repo']
    else: #cloning into the new repo
        # verify if there is an previously existing local folder
        if os.path.exists('./'+git_repository):
            if clean:
                ## Try to remove tree directory; if failed show an error using try...except on screen
                print(const.DELETING_LOCAL_STORAGE)
                try:
                    shutil.rmtree(git_repository)
                except OSError as e:
                    print ("Error: %s - %s." % (e.filename, e.strerror))
            else:
                raise gitutils_exception.GitutilsError(const.FORK_PROBLEM_FOLDER)

        # Forks the repo
        new_project = gitlab_utils.fork_project(git_repository_id)
        try:
            http_url_to_repo = new_project.attributes['http_url_to_repo']
            http_url_to_original_repo = new_project.attributes['forked_from_project']['http_url_to_repo']
        except Exception as ex:
            raise gitutils_exception.GitutilsError(ex)

        # Clone repository
        os.system(const.GIT_CLONE_CMD % http_url_to_repo)

        # Change into git repository
        try:
            os.chdir(git_repository)
        except Exception as ex:
            raise gitutils_exception.GitutilsError(ex)

        # Add upstream repository
        # Configure Git to sync your fork with the original repository
        try:
            os.system(const.GIT_UPSTREAM_REPO_CMD % http_url_to_original_repo)
        except Exception as ex:
            print(const.GIT_UPLINK_PROBLEM % http_url_to_original_repo)


    logging.info('New project forked: [%s] (id: %s) - %s' % (
                 new_project.attributes['path_with_namespace'],
                 new_project.attributes['id'],
                 new_project.attributes['http_url_to_repo']))
    print('New project forked: [%s] (id: %s) - %s' % (
           new_project.attributes['path_with_namespace'],
           new_project.attributes['id'],
           new_project.attributes['http_url_to_repo']))


def merge(git_repository='',
          git_repository_id='',
          description='',
          title='',
          local_project=False):
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
    :param local_project: Indicates if the user has used the -p argument for indicating the project
    :type local_project: bool
    :return:
    """

    git_username = gitlab_utils.get_username()
    if git_username == -1:
        raise gitutils_exception.GitutilsError(const.PROBLEM_USERNAME)

    # Check to see the directory
    if os.path.isfile('.git/config') and local_project:
        next_line = False
        with open(".git/config") as git_search:
            while git_repository is None and git_repository_id is None:
                for line in git_search:
                    line = line.rstrip()
                    if next_line == True:
                        try:
                            git_repository = line.split('=')[-1].split('/')[-1].split('.')[0]
                            git_repository_id = line.split('=')[-1].split('/')[-2]
                        except Exception as ex:
                            raise gitutils_exception.GitutilsError(const.GIT_MERGE_PROBLEM_0)
                    if "[remote \"origin\"]" in line:
                        next_line = True
    else:
        raise gitutils_exception.GitutilsError(const.GIT_MERGE_PROBLEM_1)


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
            git_repository_id,
            source_branch,
            forked_project['forked_from_project']['id'],
            target_branch,
            title,
            final_description)

        if merge_request.attributes['id']:
            print (const.GIT_MERGE_SUCCESS \
                % (merge_request.attributes['id'],
                   merge_request.attributes['created_at']))


def main():

    ############
    # GITUTILS #
    ############

    parser = \
        argparse.ArgumentParser(description=const.GITUTILS_TITLE_DESCRIPTION, formatter_class=argparse.RawTextHelpFormatter)
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

    #sets the endpoins
    gitlab_utils.set_endpoint(arguments.endpoint)

    # Authenticate user
    gitlab_utils.authenticate()

    # retrieve repository and group names
    (repo_name, group_name, project_id) = (None, None, None)
    if arguments.command == 'merge':
        # Verify if project has been indicated
        # otherwise it fetches from local folder .git/HEAD
        no_project_indication = False
        if not arguments.project:
            no_project_indication = True
        if not arguments.project:
            repo_name = os.path.basename(os.getcwd())
        else:
            if const.ENDPOINT in arguments.project:
                web_url_split = arguments.project.split('/')
                if len(web_url_split) == 5:
                    repo_name = web_url_split[-1]
            elif '/' in arguments.project:
                # config format: "group_name/project_name"
                path_with_namespace = arguments.project.split('/')
                if len(path_with_namespace) == 2:
                    repo_name = path_with_namespace[1]
            else:
                repo_name = arguments.project
        group_name = gitlab_utils.get_project_group(repo_name, False, True)
        project_id = gitlab_utils.get_project_id(group_name, repo_name)
    elif arguments.project:
        (repo_name, group_name, project_id, valid) = \
            gitlab_utils.get_repo_group_names(arguments.project[0], arguments.clean)
        # if project is personal, needs to be deleted
        if group_name == gitlab_utils.get_username():
            if arguments.clean:
                gitlab_utils.delete_project(project_id)
                (repo_name, group_name, project_id, valid) = \
                    gitlab_utils.get_repo_group_names(arguments.project, False)
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


    # group_id = gitlab_utils.get_group_id('babic_a')
    # group_id = gitlab_utils.get_group_id('hax_l')
    # group_id = gitlab_utils.get_group_id('controls_highlevel_applications')
    # group_id = gitlab_utils.get_group_id('hax_l')
    # gl = gitlab_utils.get_gl()
    # # group = gl.groups.get(group_id, lazy=True)
    # # print(group.projects.list())
    # projects = gl.projects.list(username='hax_l')
    # for i in projects:
    #     print(i.attributes['name'])


    # hax = gl.users.list(username='ebner')[0]
    # print(hax.projects.list())
    # print('test')
    # print(group_name, gitlab_utils.get_group_id(group_name))
    # print(repo_name, project_id)
    # quit()

    # Command, group and repo are ok
    if arguments.command and \
       repo_name is not None and \
       group_name is not None and \
       project_id is not None:
        try:
            if arguments.command == 'fork':
                fork(git_repository_id=project_id,
                     git_repository=repo_name,
                     no_clone=arguments.no_clone,
                     clean = arguments.clean)
            elif arguments.command == 'merge':
                merge(git_repository=repo_name,
                      git_repository_id=project_id,
                      description=arguments.description,
                      title=arguments.title,
                      local_project=no_project_indication)
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
