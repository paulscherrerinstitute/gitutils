import gitlab_utils
import const
import sys
import os
import time
import subprocess
import logging


def fork(git_repository_id=None, git_repository='', no_clone=False):
    """
    Creates a fork repository of the repository given as parameter.
    :param git_repository_id: Id of the repository to be pulled.
    :type git_repository_id: int
    :param git_repository: Name of the repository to be pulled.
    :type git_repository: str
    :param no_clone: Flag to clone or not the forked repository.
    :type no_clone: bool
    :return: 
    """
    git_username = gitlab_utils.get_username()
    if git_username == -1:
        raise Exception(const.PROBLEM_USERNAME)
        
    if git_repository_id is None:
        raise Exception(const.GIT_UNABLE_TO_FIND_PROJECT_MSG % project['name'])

    print(const.FORK_PROJECT % git_repository)

    # Forks and copy the direct http to the repo
    new_project = gitlab_utils.fork_project(git_repository_id)
    http_url_to_repo = new_project.attributes['http_url_to_repo']

    if not no_clone:
        # Clone repository
        time.sleep(2)
        os.system(const.GIT_CLONE_CMD % (http_url_to_repo))
        # Change into git repository
        try:
            os.chdir(git_repository)
        except Exception as ex:
            template = const.EXCEPTION_TEMPLATE
            message = template.format(type(ex).__name__, ex.args)
            print(message)
            return -1

        # Add upstream repository
        os.system(const.GIT_UPSTREAM_REPO_CMD % http_url_to_repo)

    logging.info('New project forked: [%s] (id: %s) - %s' % (new_project.attributes['path_with_namespace'], 
                                    new_project.attributes['id'], 
                                    new_project.attributes['http_url_to_repo']))
    print('New project forked: [%s] (id: %s) - %s' % (new_project.attributes['path_with_namespace'], 
                                    new_project.attributes['id'], 
                                    new_project.attributes['http_url_to_repo']))

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
        raise Exception(const.PROBLEM_USERNAME)

    # Check to see the directory
    if not os.path.isdir('.git/'):
        raise Exception(const.GIT_MERGE_PROBLEM)

    # Check if there is already a fork
    forked_project = gitlab_utils.get_forked_project(git_repository, 
                                                     git_repository_id)
    
    if forked_project is None:
            raise Exception(const.GIT_MERGE_PROBLEM)
    else:
        print(const.GIT_CREATE_MERGE_MSG)
        title = title
        final_description = const.GIT_MERGE_DESCRIPTION_MSG % git_username
        final_description += ". User definition: "+description
        # Gets the source branch (assuming the current branch is the one to be merged)
        source_branch = subprocess.check_output(
                        const.GIT_GET_CURRENT_BRANCH, shell=True).decode("utf-8").rstrip() 
        # Gets the target branch (assuming the master as target branch)
        target_branch = gitlab_utils.get_branch(forked_project['forked_from_project']['id'])
        
        merge_request = gitlab_utils.create_merge_request(git_repository_id, 
                                    source_branch,
                                    forked_project['forked_from_project']['id'], 
                                    target_branch, title, final_description)
        
        if merge_request.attributes['id']:
            print(const.GIT_MERGE_SUCCESS % (merge_request.attributes['id'], 
                                            merge_request.attributes['created_at']))

def main():
    import argparse

    parser = argparse.ArgumentParser(description=const.APP_CONFIG_TITLE_DESCRIPTION)
    parser.add_argument('-e', '--endpoint', help=const.ENDPOINT_HELP_MSG, default=const.ENDPOINT)

    subparsers = parser.add_subparsers(title='command',
                                       description='valid commands',
                                       dest='command',
                                       help='commands')

    parser_fork = subparsers.add_parser('fork', help=const.FORK_HELP_MSG)
    parser_fork.add_argument('-p', '--project', required=True, 
                                                help=const.FORK_PROJECT_MESSAGE)
    parser_fork.add_argument('-n', '--no_clone', action=const.STORE_TRUE, 
                                                help=const.FORK_NOCLONE_HELP)

    parser_mr = subparsers.add_parser('merge', help=const.MERGE_HELP_MSG)
    parser_mr.add_argument('-p', '--project', help=const.MERGE_PROJECT_MESSAGE)
    parser_mr.add_argument('-t', '--title', required=True, 
                                                help=const.MERGE_MESSAGE_TITLE)
    parser_mr.add_argument('-d', '--description', help=const.MERGE_MESSAGE_DESCRIPTION)

    arguments = parser.parse_args()


    # Authenticate
    gitlab_utils.authenticate(arguments.endpoint)

    repo_name, group_name = None, None
    if arguments.project:
        repo_name, group_name, valid  = gitlab_utils.get_repo_group_names(
                                                                arguments.project)
        group_id = gitlab_utils.get_group_id(group_name)        
        if not valid or group_id == -1:
            parser.print_help()
            sys.exit(-1)
    elif arguments.command == 'merge':
        repo_name = os.path.basename(os.getcwd())
        group_name = gitlab_utils.get_project_group(repo_name, True)
    else:
        parser.print_help()
        sys.exit(-1)
        
    if arguments.command and repo_name != None and group_name != None:
        try:
            if arguments.command == 'fork':
                fork(git_repository_id = gitlab_utils.get_project_id(group_name, 
                                                                    repo_name), 
                     git_repository=repo_name, 
                     no_clone=arguments.no_clone)
            elif arguments.command == 'merge':
                merge(git_repository = repo_name,
                    git_repository_id = gitlab_utils.get_project_id(group_name, 
                                                                    repo_name), 
                    description=arguments.description,
                    title = arguments.title)
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
