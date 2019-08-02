import gitlab_utils
import const
import os
import time

def pull(git_group_id='', git_repository_id='', git_repository_upstream='', git_repository='', basedir='.', clean=False):
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
    if git_username == const.RETURN_PROBLEM:
        print(const.PROBLEM_USERNAME)

    option_delete_fork = False

    if clean:
        option_delete_fork = True

    if git_repository_upstream is None or git_repository_id is None:
        raise Exception(const.GIT_UNABLE_TO_FIND_PROJECT_MSG % project['name'])

    # Check if there is already a fork
    forked_project = None
    projects = gitlab_utils.get_owned_projects()
    for project in projects:
        if project['username'] == git_username and project['name'] == git_repository:
            if 'forked_from_project' in project:
                # check whether project is forked from the right project
                if project['forked_from_project']['id'] == git_repository_id:
                    print(const.FORKED_EXISTS.format(git_repository))
                    forked_project = project
            else:
                # Either we delete or we have to fail
                print(const.REPO_EXISTS_NOT_FORK.format(git_repository))
                if not option_delete_fork:
                    return

            if option_delete_fork:
                # Delete fork
                print(const.GIT_DELETE_FORK_MSG)
                # gitlab_utils.print_response = True
                r = gitlab_utils.delete_project(project['id'])
                forked_project = None
            break

    # If there is no fork on the server - fork the repository
    if not forked_project:
        # Fork project
        print(const.FORK_PROJECT)
        rs = gitlab_utils.fork_project(git_repository_id)
        if rs == -1:
            print(const.FORK_PROBLEM)
            exit(-1)
        else:
            ssh_url_to_fork = rs
    
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
        os.system(const.GIT_CLONE_CMD % (ssh_url_to_fork))
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


def push(git_group_id='', git_repository='', basedir='.', merge_request=None):
    """
    Push changes to fork and create merge request
    :param git_group_id: Id of the group to be pulled from.
    :type git_group_id: int
    :param git_repository: Name of the repository to push.
    :type git_repository: str
    :param basedir: Base directory
    :type basedir: str
    :param title: Title of the push command.
    :type title: str
    :param description: Description of the push command.
    :type description: str
    :return:
    """

    git_username = gitlab_utils.get_username()

    # Get id for master git repository
    # group_id = gitlab_utils.get_group_id(git_group)
    group_id = git_group_id
    projects = gitlab_utils.get_group_projects(group_id)
    forked_project = None
    git_repository_id = None

    for project in projects:
        if project['name'] == git_repository:
            git_repository_id = project['id']
            break

    # Get id for forked repository
    projects = gitlab_utils.get_owned_projects()
    for project in projects:
        if project['namespace']['name'] == git_username and project['name'] == git_repository:
            if 'forked_from_project' in project:
                # check whether project is forked from the right project
                if project['forked_from_project']['id'] == git_repository_id:
                    forked_project = project
                else:
                    print(const.NO_FORK_CENTAL)
                    return

    # We assume that we are in the directory with the forked repository
    os.chdir(basedir+'/'+git_repository)

    # Push changes to forked repository
    print(const.GIT_PUSH_MSG)
    os.system(const.GIT_PUSH_CMD)

    if merge_request:

        title = merge_request
        description = const.GIT_MERGE_DESCRIPTION_MSG % git_username

        # Create pull request
        if forked_project is None:
            raise Exception(const.GIT_MERGE_PROBLEM)

        print(const.GIT_CREATE_MERGE_MSG)
        merge_request = gitlab_utils.create_merge_request(git_repository_id, forked_project['id'], title=title, description=description)

        if 'message' in merge_request:
            # Merge request already exists
            for m in merge_request['message']:
                print(m)


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

    
    # TODO Add a --list option. This is currently not possible because the way the arguments are done right now
    # (configuration is a required option and the parsing would fail before coming to the --list option)
    # The usage should be like this: app_config <subparser> configuration

    parser = argparse.ArgumentParser(description=const.APP_CONFIG_TITLE_DESCRIPTION)
    # parser.add_argument('configuration', nargs='?', default=None)
    parser.add_argument('-b', '--basedir', help=const.BASEDIR_HELP_MSG, default='./')

    parser.add_argument('-c', '--config', nargs='?', help=const.CONFIG_HELP_MSG)
    # parser.add_argument('-l', '--list', help=const.CONFIG_LIST_HELP_MSG, action=const.STORE_TRUE)

    subparsers = parser.add_subparsers(title='command',
                                       description='valid commands',
                                       dest='command',
                                       help='commands')

    parser_pull = subparsers.add_parser('pull', help=const.PULL_HELP_MSG)
    parser_pull.add_argument('-c', '--clean', action=const.STORE_TRUE, help=const.PULL_CLEAN_HELP_MSG)

    parser_push = subparsers.add_parser('push', help=const.PUSH_HELP_MSG)
    parser_push.add_argument('-m', '--message', required=True, help=const.PUSH_MERGE_REQUEST_TITLE)

    parser_commit = subparsers.add_parser('commit', help=const.COMMIT_HELP_MSG)
    parser_commit.add_argument('-m', '--message', required=True, help=const.COMMIT_MESSAGE)

    arguments = parser.parse_args()

    os.makedirs(arguments.basedir, exist_ok=True)

    repo_name, group_name = None, None
    if arguments.config:
        repo_name, group_name, valid  = gitlab_utils.get_repo_group_names(arguments.config)
        group_id = gitlab_utils.get_group_id(group_name)
        if not valid or group_id == -1:
            parser.print_help()
            exit(-1)
    else:
        parser.print_help()
        exit(-1)


    if arguments.command and repo_name != None and group_name != None:
        try:
            if arguments.command == 'pull':
                pull(git_group_id = group_id, 
                     git_repository_id = gitlab_utils.get_project_id(group_name, repo_name), 
                     git_repository_upstream = gitlab_utils.get_project_url(group_id, repo_name), 
                     git_repository=repo_name,
                     basedir=arguments.basedir, 
                     clean=arguments.clean)
            elif arguments.command == 'push':
                push(basedir=arguments.basedir, **configuration[arguments.configuration], merge_request=arguments.message)
            elif arguments.command == 'commit':
                commit(message = arguments.message, 
                       basedir=arguments.basedir, 
                       git_repository=repo_name,)
        except Exception as e:
            print(str(e))
    else:
        parser.print_help()
        exit(-1)

if __name__ == '__main__':
    main()
