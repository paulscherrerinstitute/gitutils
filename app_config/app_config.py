import gitlab_utils
import const
import sys
import os
import time
import subprocess
import logging


def fork(git_repository_id=None, git_repository='', no_clone=False):
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
        print(const.CLONE_FORK)        
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
        os.system(const.GIT_UPSTREAM_REPO_CMD % git_repository_upstream)
    else:
        print(const.FORKED_BUT_NOT_CLONED)

    logging.info('New project forked: [%s] (id: %s) - %s' % (new_project.attributes['path_with_namespace'], 
                                    new_project.attributes['id'], 
                                    new_project.attributes['http_url_to_repo']))
    print('New project forked: [%s] (id: %s) - %s' % (new_project.attributes['path_with_namespace'], 
                                    new_project.attributes['id'], 
                                    new_project.attributes['http_url_to_repo']))

def pull(git_group_id='', git_repository_id=None, git_repository_upstream=None, 
                                    git_repository='', basedir='.', clean=False):
    """
    Pull application configuration from central configuration management server
    :param git_group_id: Id of the group to be pulled from.
    :type git_group_id: int
    :param git_repository: Name of the repository to be pulled.
    :type git_repository: str
    :param basedir: Base directory.
    :type basedir: str
    :param clean: Clean pull - i.e. delete fork and local clone
    :type clean: Boolean
    """
    git_username = gitlab_utils.get_username()
    if git_username == -1:
        raise Exception(const.PROBLEM_USERNAME)
        
    if git_repository_upstream is None or git_repository_id is None:
        raise Exception(const.GIT_UNABLE_TO_FIND_PROJECT_MSG % project['name'])

    # Check if there is already a fork
    forked_project = gitlab_utils.get_forked_project(git_repository, 
                                                     git_repository_id)


    # not forked -> fork
    if not forked_project:
        print(const.FORK_PROJECT)
        http_url_to_repo = gitlab_utils.fork_project(git_repository_id)
    else:
        # forked and clean
        if clean:
            # personal group -> delete + fork
            if git_group_id == 0:
                print(const.DELETE_PERSONAL_PROJECT)
                source_project_id = forked_project['forked_from_project']['id']
                r = gitlab_utils.delete_project(git_repository_id)
                if r == 0:
                    http_url_to_repo = gitlab_utils.fork_project(source_project_id)
                else:
                    raise Exception(const.PROBLEM_DELETING_PROJECT)
            else:# not personal group -> warning about not deletion and fork
                print(const.NOT_ABLE_TO_DELETE_NON_PERSONAL_REPO.format(forked_project['name']))
                # check if personal project already exists
                own_projects = gitlab_utils.get_owned_projects()
                for project in own_projects:
                    if project['name'] == forked_project['name']:
                        http_url_to_repo = git_repository_upstream
        else: # forked and not clean
            print(const.FORKED_PULL.format(git_repository))
        

    # Change to base directory
    os.chdir(basedir)

    # Clean cloned repository
    if os.path.isdir(git_repository) and clean:
        print(const.REMOVE_LOCAL_CLONE)
        import shutil
        shutil.rmtree(basedir+'/'+git_repository)

    # Check if directory already exsits
    if os.path.isdir(git_repository):
        print(const.CLONE_EXISTS)
        # Change into git repository
        os.chdir(git_repository)

        # Make sure that clone is up to date ...
        os.system(const.GIT_PULL_CMD)

    else:
        # Needed because of problems with the git server
        time.sleep(2)
        print(const.CLONE_FORK)
        
        # Clone repository
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
        os.system(const.GIT_UPSTREAM_REPO_CMD % git_repository_upstream)

    print(const.GIT_PULL_CONFIG_AVAILABLE+basedir+'/'+git_repository)


def push(basedir='', git_group_name='', git_repository='',  git_repository_id = '', 
                                    git_repository_upstream = ''):
    """
    Push changes to fork
    :param git_group_name: Name of the group push.
    :type git_group_name: str
    :param git_repository_id: Id of the group to push.
    :type git_repository_id: Int
    :param git_repository: Name of the repository to push.
    :type git_repository: str
    :param basedir: Base directory
    :type basedir: str
    
    :return:
    """

    git_username = gitlab_utils.get_username()
    if git_username == -1:
        raise Exception(const.PROBLEM_USERNAME)

    # We assume that we are in the directory with the forked repository
    os.chdir(basedir+'/'+git_repository)
    # Push changes to forked repository
    print(const.GIT_PUSH_MSG_CENTRAL_SERVER)
    try:
        os.system(const.GIT_PUSH_CMD)
    except Exception as ex:
        template = const.EXCEPTION_TEMPLATE
        message = template.format(type(ex).__name__, ex.args)
        print(message)
        sys.exit(-1)
    
    print(const.GIT_PUSHED % git_repository_upstream)

def merge_request(basedir='.', 
                    git_repository='',
                    git_repository_id='',
                    description='',
                    title=''):
    """
    Creates a merge request to merge a forked repository.
    :param basedir: Base directory.
    :type basedir: str
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
        os.chdir(basedir+'/'+git_repository)
        source_branch = subprocess.check_output(
                        const.GIT_GET_CURRENT_BRANCH, shell=True).decode("utf-8").rstrip() 
        # Gets the target branch (assuming the master as target branch)
        target_branch = gitlab_utils.get_branch(forked_project['forked_from_project']['id'])
        
        merge_request = gitlab_utils.create_merge_request(git_repository_id, 
                                    source_branch,
                                    forked_project['forked_from_project']['id'], 
                                    target_branch, title, final_description)
        
        if merge_request.attributes['id']:
            print(const.GIT_MERGE_SUCCESS.format(merge_request.attributes['id'], 
                                            merge_request.attributes['created_at']))


def commit(message, basedir='.', git_repository=''):
    """
    Commit changes to local clone of repository.
    :param message: Commit message.
    :type message: str
    :param git_repository: Repository name.
    :type git_repository: str
    :param basedir: Base directory for the commit.
    :type basedir: str 
    :return:
    """
    # Checks the username+login validation
    git_username = gitlab_utils.get_username()
    if git_username == -1:
        raise Exception(const.PROBLEM_USERNAME)

    # Change into git repository
    os.chdir(basedir+'/'+git_repository)
    # Add all changes to commit
    os.system(const.GIT_ADD_ALL)
    # Commit changes
    dir_c = basedir+'/'+git_repository
    os.system(const.GIT_COMMIT_CMD % (dir_c, message))
    # Message
    print(const.GIT_PULL_CONFIG_AVAILABLE+basedir+'/'+git_repository)


def main():
    import argparse

    parser = argparse.ArgumentParser(description=const.APP_CONFIG_TITLE_DESCRIPTION)
    parser.add_argument('-e', '--endpoint', help=const.BASEDIR_HELP_MSG, default=const.ENDPOINT)

    subparsers = parser.add_subparsers(title='command',
                                       description='valid commands',
                                       dest='command',
                                       help='commands')

    parser_fork = subparsers.add_parser('fork', help=const.FORK_HELP_MSG)
    parser_fork.add_argument('-p', '--project', required=True, 
                                                help=const.FORK_PROJECT_MESSAGE)
    parser_fork.add_argument('-n', '--no_clone', action=const.STORE_TRUE, 
                                                help=const.FORK_NOCLONE_HELP)

    parser_mr = subparsers.add_parser('merge_request', help=const.MERGE_HELP_MSG)
    parser_mr.add_argument('-p', '--project', required=True, 
                                                help=const.FORK_PROJECT_MESSAGE)
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
            elif arguments.command == 'merge_request':
                merge_request(basedir=arguments.basedir,
                    git_repository = repo_name,
                    git_repository_id = gitlab_utils.get_project_id(group_name, 
                                                                    repo_name), 
                    description=arguments.description,
                    title = arguments.title)
        except Exception as e:
            print(str(e))
    else:
        parser.print_help()
        exit(-1)

if __name__ == '__main__':
    main()
