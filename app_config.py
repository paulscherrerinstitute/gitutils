import gitlab
import os


def pull(git_group='', git_repository='', basedir='.', clean=False):
    """
    Pull application configuration from central configuration management server
    :param clean: Clean pull - i.e. delete fork and local clone
    """

    git_username = gitlab.get_username()

    option_delete_fork = False

    if clean:
        option_delete_fork = True

    # print(gitlab.get_projects())

    # Get id for git repository
    group_id = gitlab.get_group_id(git_group)
    projects = gitlab.get_group_projects(group_id)

    for project in projects:
        if project['name'] == git_repository:
            git_repository_id = project['id']
            break

    # Check if there is already a fork
    forked_project = None
    projects = gitlab.get_owned_projects()
    for project in projects:
        if project['namespace']['name'] == git_username and project['name'] == git_repository:
            if 'forked_from_project' in project:
                # check whether project is forked from the right project
                if project['forked_from_project']['id'] == git_repository_id:
                    print('A forked repository with the name {} already exists'.format(git_repository))
                    forked_project = project
            else:
                # Either we delete or we have to fail
                print('A repository with the name {} already exists but is not a fork'.format(git_repository))
                if not option_delete_fork:
                    return

            if option_delete_fork:
                # Delete fork
                print("Delete fork")
                gitlab.print_response = True
                gitlab.delete_project(project['id'])
                forked_project = None

            break

    # If there is no fork on the server - fork the repository
    if not forked_project:
        # Need to check whether fork already exists
        # If yes, delete ... or just clone and update ...

        # Fork project
        forked_project = gitlab.fork_project(git_repository_id)

    # Change to base directory
    os.chdir(basedir)

    # Check if directory already exsits
    if os.path.isdir(git_repository):
        print('clone directory already exists')
        # We assume that this is already a clone of a fork

        # Change into git repository
        os.chdir(git_repository)

        # Make sure that clone is up to date ...
        os.system('git pull upstream master')

    else:
        # Clone repository
        os.system('git clone %s' % (forked_project['ssh_url_to_repo']))

        # Change into git repository
        os.chdir(git_repository)

        # Add upstream repository
        os.system('git remote add upstream %s' % (forked_project['ssh_url_to_repo']))


def push(git_group='', git_repository='', basedir='.'):

    git_username = gitlab.get_username()

    # Get id for master git repository
    group_id = gitlab.get_group_id(git_group)
    projects = gitlab.get_group_projects(group_id)

    for project in projects:
        if project['name'] == git_repository:
            git_repository_id = project['id']
            break

    # Get id for forked repository
    projects = gitlab.get_owned_projects()
    for project in projects:
        if project['namespace']['name'] == git_username and project['name'] == git_repository:
            if 'forked_from_project' in project:
                # check whether project is forked from the right project
                if project['forked_from_project']['id'] == git_repository_id:
                    forked_project = project
                else:
                    print('There is no fork on the central server')
                    return

    # We assume that we are in the directory with the forked repository
    os.chdir(basedir+git_repository)

    # Push changes to forked repository
    print('Push changes to central server')
    os.system('git push origin master')

    # Create pull request
    print('Create merge request')
    merge_request = gitlab.create_merge_request(git_repository_id, forked_project['id'])

    if 'message' in merge_request:
        # Merge request already exists
        for m in merge_request['message']:
            print(m)


def commit(message, git_group='', git_repository='', basedir='.'):

    # Change into git repository
    os.chdir(basedir+git_repository)

    # Commit changes
    os.system('git commit -a -m %s' % message)


if __name__ == '__main__':

    configuration = {
        'launcher': {
            'git_group': 'launcher_config',
            'git_repository': 'sf_machine_launcher'
        },
        'archiver': {
            'git_group': 'archiver_config',
            'git_repository': 'sf_archapp'
        }

    }

    import argparse

    parser = argparse.ArgumentParser(description='Application configuration management utility')
    parser.add_argument('configuration')
    parser.add_argument('-b', '--basedir', help='Base directory to clone configurations to', default=os.path.expanduser('~')+'/app_config')

    # TODO add option to overwrite configuration dictionary

    subparsers = parser.add_subparsers(title='command',
                                       description='valid commands',
                                       dest='command',
                                       help='commands')

    parser_pull = subparsers.add_parser('pull', help='pull configuration from central server')
    parser_pull.add_argument('-c', '--clean', action='store_true', help='Create clean fork and clone')

    parser_push = subparsers.add_parser('push', help='push configuration from central server')

    parser_commit = subparsers.add_parser('commit', help='commit configuration changes to local repository')
    parser_commit.add_argument('-m', '--message', help='commit message')

    arguments = parser.parse_args()

    print(arguments.basedir)

    if arguments.configuration not in configuration:
        print('Unsupported configuration')
        parser.print_help()
        exit(-1)

    if arguments.command:
        if arguments.command == 'pull':
            pull(basedir=arguments.basedir, **configuration[arguments.configuration])
        elif arguments.command == 'push':
            push(basedir=arguments.basedir, **configuration[arguments.configuration])
        elif arguments.command == 'commit':
            commit(arguments.message, basedir=arguments.basedir, **configuration[arguments.configuration])
    else:
        parser.print_help()
        exit(-1)

