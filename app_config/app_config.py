from . import gitlab
import os


def pull(git_group_id='', git_repository='', basedir='.', clean=False):
    """
    Pull application configuration from central configuration management server
    :param clean: Clean pull - i.e. delete fork and local clone
    :param git_group_id:
    :param git_repository:
    :param basedir:
    """

    git_username = gitlab.get_username()

    option_delete_fork = False

    if clean:
        option_delete_fork = True

    # Get id for git repository
    # group_id = gitlab.get_group_id(git_group)
    group_id = git_group_id
    projects = gitlab.get_group_projects(group_id)

    for project in projects:
        if project['name'] == git_repository:
            git_repository_id = project['id']
            git_repository_upstream = project['url']
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
                # gitlab.print_response = True
                gitlab.delete_project(project['id'])
                forked_project = None

            break

    # If there is no fork on the server - fork the repository
    if not forked_project:
        # Need to check whether fork already exists
        # If yes, delete ... or just clone and update ...

        # Fork project
        print('Fork project')
        forked_project = gitlab.fork_project(git_repository_id)

        import time
        time.sleep(1)

    # Change to base directory
    os.chdir(basedir)

    # Clean cloned repository
    if os.path.isdir(git_repository) and clean:
        print('Removing local clone')
        import shutil
        shutil.rmtree(basedir+'/'+git_repository)

    # Check if directory already exsits
    if os.path.isdir(git_repository):
        print('Clone already exists')
        # We assume that this is already a clone of a fork

        # Change into git repository
        os.chdir(git_repository)

        # Make sure that clone is up to date ...
        os.system('git pull upstream master')


    else:
        print('Clone fork')

        # Clone repository
        os.system('git clone %s' % (forked_project['ssh_url_to_repo']))

        # Change into git repository
        os.chdir(git_repository)

        # Add upstream repository
        os.system('git remote add upstream %s' % (git_repository_upstream))

    print('Configuration is now available at: '+basedir+'/'+git_repository)


def push(git_group_id='', git_repository='', basedir='.', merge_request=None):
    """
    Push changes to fork and create merge request
    :param git_group_id:
    :param git_repository:
    :param basedir:
    :param title:
    :param description:
    :return:
    """

    git_username = gitlab.get_username()

    # Get id for master git repository
    # group_id = gitlab.get_group_id(git_group)
    group_id = git_group_id
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
    os.chdir(basedir+'/'+git_repository)

    # Push changes to forked repository
    print('Push changes to central server')
    os.system('git push origin master')

    if merge_request:
        title = merge_request
        description = 'The configuration was changed by %s' % git_username

        # Create pull request
        print('Create merge request')
        merge_request = gitlab.create_merge_request(git_repository_id, forked_project['id'], title=title, description=description)

        if 'message' in merge_request:
            # Merge request already exists
            for m in merge_request['message']:
                print(m)


def commit(message, git_group='', git_repository='', basedir='.'):
    """
    Commit changes to local clone
    :param message:
    :param git_group:
    :param git_repository:
    :param basedir:
    :return:
    """

    # Change into git repository
    os.chdir(basedir+'/'+git_repository)

    # Commit changes
    os.system('git commit -a -m %s' % message)


def main():

    # Default configuration
    # The group id can be found out by executing following command:
    # curl -v -X GET -H "PRIVATE-TOKEN: aaaaaaaaaaaa" https://git.psi.ch/api/v3/groups?search=sf_config
    configuration = {
        'launcher': {
            # 'git_group': 'launcher_config',
            'git_group_id': 107,
            'git_repository': 'sf_machine_launcher'
        },
        'launcher_controls': {
            # 'git_group': 'launcher_config',
            'git_group_id': 107,
            'git_repository': 'sf_controls_launcher'
        },
        'launcher_magnets': {
            # 'git_group': 'launcher_config',
            'git_group_id': 107,
            'git_repository': 'sf_magnets_launcher'
        },
        'launcher_insertiondevices': {
            # 'git_group': 'launcher_config',
            'git_group_id': 107,
            'git_repository': 'sf_insertiondevices_launcher'
        },
        'launcher_photonics': {
            # 'git_group': 'launcher_config',
            'git_group_id': 107,
            'git_repository': 'sf_photonics_launcher'
        },
        'launcher_timingsynchronization': {
            # 'git_group': 'launcher_config',
            'git_group_id': 107,
            'git_repository': 'sf_timingsynchronization_launcher'
        },
        'launcher_laser': {
            # 'git_group': 'launcher_config',
            'git_group_id': 107,
            'git_repository': 'sf_laser_launcher'
        },
        'launcher_vacuum': {
            # 'git_group': 'launcher_config',
            'git_group_id': 107,
            'git_repository': 'sf_vacuum_launcher'
        },
        'launcher_diagnostics': {
            # 'git_group': 'launcher_config',
            'git_group_id': 107,
            'git_repository': 'sf_diagnostics_launcher'
        },
        'launcher_rf': {
            # 'git_group': 'launcher_config',
            'git_group_id': 107,
            'git_repository': 'sf_rf_launcher'
        },
        'archiver': {
            # 'git_group': 'archiver_config',
            'git_group_id': 302,
            'git_repository': 'sf_archapp'
        },
        'databuffer': {
            # 'git_group': 'sf_config',
            'git_group_id': 321,
            'git_repository': 'sf_daq_config'
        },
        'alarmhandler': {
            # 'git_group': 'alarmhandler_config',
            'git_group_id': 323,
            'git_repository': 'sf_alh_config'
        }

    }

    import argparse

    parser = argparse.ArgumentParser(description='Application configuration management utility')
    parser.add_argument('configuration')
    parser.add_argument('-b', '--basedir', help='Base directory to clone configurations to', default=os.path.expanduser('~')+'/app_config')

    parser.add_argument('-c', '--config', nargs='?', help='Configuration')

    subparsers = parser.add_subparsers(title='command',
                                       description='valid commands',
                                       dest='command',
                                       help='commands')

    parser_pull = subparsers.add_parser('pull', help='pull configuration from central server')
    parser_pull.add_argument('-c', '--clean', action='store_true', help='Create clean fork and clone')

    parser_push = subparsers.add_parser('push', help='push configuration from central server')
    parser_push.add_argument('-m', '--message', required=True, help='Merge request title')

    parser_commit = subparsers.add_parser('commit', help='commit configuration changes to local repository')
    parser_commit.add_argument('-m', '--message', required=True, help='commit message')

    arguments = parser.parse_args()

    print(arguments.basedir)
    os.makedirs(arguments.basedir, exist_ok=True)

    if arguments.config:
        import json
        with open(arguments.config) as data_file:
            configuration = json.load(data_file)

    if arguments.configuration not in configuration:
        print('Unsupported configuration')
        parser.print_help()
        exit(-1)

    if arguments.command:
        if arguments.command == 'pull':
            pull(basedir=arguments.basedir, clean=arguments.clean, **configuration[arguments.configuration])
        elif arguments.command == 'push':
            push(basedir=arguments.basedir, **configuration[arguments.configuration], merge_request=arguments.message)
        elif arguments.command == 'commit':
            commit(arguments.message, basedir=arguments.basedir, **configuration[arguments.configuration])
    else:
        parser.print_help()
        exit(-1)

if __name__ == '__main__':
    main()
