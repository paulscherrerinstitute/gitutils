import argparse
import textwrap
import time
import sys
import os
from gitutils import const
from gitutils import gitlab_utils
from gitutils import gitutils_exception


class Parser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description=const.GITUTILS_TITLE_DESCRIPTION,
            formatter_class=argparse.RawTextHelpFormatter)
        self.parser_find = None
        self.parser_createp = None
        self.parser_mr = None
        self.parser_fork = None
        self.parser_addldap = None
        self.parser_createg = None
        self.parser_cg = None
        self.init_parser()

    def get_parser(self):
        return self.parser

    def get_help(self):
        self.parser.print_help()
        sys.exit(-1)

    def get_arguments(self):
        return self.parser.parse_args()

    def init_parser(self):
        ############
        # GITUTILS #
        ############
        self.parser.add_argument('-e', '--endpoint',
                                 help=const.ENDPOINT_HELP_MSG,
                                 default=const.ENDPOINT)

        self.parser.add_argument(
            '-v', dest='verbosity', help=const.VERBOSITY_HELP_MSG,
            action='store_true')

        subparsers = self.parser.add_subparsers(title='command',
                                                description='valid commands',
                                                dest='command',
                                                help='commands')
        ############
        # ADD LDAP #
        ############
        self.parser_addldap = subparsers.add_parser(
            'addldap', help=const.ADDLDAP_HELP_MSG,
            formatter_class=argparse.RawTextHelpFormatter)
        self.parser_addldap.add_argument(
            'group', metavar='group', help=textwrap.dedent(
                const.ADDLDAP_GROUP_NAME))
        self.parser_addldap.add_argument(
            'ldapgroup', metavar='ldapgroup', help=textwrap.dedent(
                const.ADDLDAP_LDAP_GROUP_NAME))
        self.parser_addldap.add_argument(
            'role', metavar='role', nargs='?', default=None,
            help=textwrap.dedent(const.ADDLDAP_ROLE))

        ###############
        # CLONE GROUP #
        ###############
        self.parser_cg = subparsers.add_parser(
            'clonegroup', help=const.CLONEGROUP_HELP_MSG,
            formatter_class=argparse.RawTextHelpFormatter)
        self.parser_cg.add_argument('group', nargs=1, metavar='group',
                                    default='', help=textwrap.dedent(
                                        const.CLONEGROUP_GROUP_NAME))
        self.parser_cg.add_argument(
            'url', nargs='?', metavar='url', default='http_url',
            choices=['url', 'http_url'],
            help=textwrap.dedent(const.CLONEGROUP_MODE))
        self.parser_cg.add_argument(
            'pattern', nargs='*', metavar='pattern', default=None,
            help=textwrap.dedent(const.CLONEGROUP_PATTERN))

        ################
        # CREATE GROUP #
        ################
        self.parser_createg = subparsers.add_parser(
            'creategroups', help=const.CREATEGROUP_HELP_MSG,
            formatter_class=argparse.RawTextHelpFormatter)
        self.parser_createg.add_argument('name', nargs='+', metavar='name',
                                         help=textwrap.dedent(const.CREATEGROUP_GROUP_NAME))

        ###################
        # CREATE PROJECTS #
        ###################
        self.parser_createp = subparsers.add_parser(
            'createprojects', help=const.CREATEPROJECT_HELP_MSG,
            formatter_class=argparse.RawTextHelpFormatter)

        self.parser_createp.add_argument(
            'group', nargs=1, metavar='group', help=textwrap.dedent(
                const.CLONEGROUP_GROUP_NAME))
        self.parser_createp.add_argument('name', nargs='+', metavar='name',
                                         help=textwrap.dedent(const.CREATEPROJECT_PROJECTS_NAME))

        ########
        # FIND #
        ########
        self.parser_find = subparsers.add_parser(
            'find', help=const.FIND_HELP_MSG,
            formatter_class=argparse.RawTextHelpFormatter)
        self.parser_find.add_argument('term', nargs=1, metavar='term',
                                      help=textwrap.dedent(const.GREP_TERM_MSG))
        self.parser_find.add_argument('-f',
                                      '--file',
                                      action=const.STORE_TRUE,
                                      help=const.FIND_FILES_ONLY_MSG)

        ############
        # FORK CMD #
        ############
        self.parser_fork = subparsers.add_parser(
            'fork', help=const.FORK_HELP_MSG,
            formatter_class=argparse.RawTextHelpFormatter)
        self.parser_fork.add_argument('-n',
                                      '--no_clone',
                                      action=const.STORE_TRUE,
                                      help=const.FORK_NOCLONE_HELP)
        self.parser_fork.add_argument('-c',
                                      '--clean',
                                      action=const.STORE_TRUE,
                                      help=const.FORK_CLEAN_MSG)
        self.parser_fork.add_argument('-g',
                                      '--group',
                                      action=const.STORE_TRUE,
                                      help=const.FORK_GROUP_MSG)
        self.parser_fork.add_argument(
            'project', nargs='?', metavar='project', default=None,
            help=textwrap.dedent(const.FORK_PROJECT_MESSAGE))

        #############
        # LOGIN CMD #
        #############
        subparsers.add_parser('login',
                              help=const.LOGIN_HELP_MSG,
                              formatter_class=argparse.RawTextHelpFormatter)

        #############
        # MERGE CMD #
        #############
        self.parser_mr = subparsers.add_parser(
            'merge', help=const.MERGE_HELP_MSG,
            formatter_class=argparse.RawTextHelpFormatter)
        self.parser_mr.add_argument('-t',
                                    '--title',
                                    help=const.MERGE_MESSAGE_TITLE)
        self.parser_mr.add_argument('-p',
                                    '--project',
                                    help=const.MERGE_PROJECT_MESSAGE)
        self.parser_mr.add_argument('-d',
                                    '--description',
                                    help=const.MERGE_MESSAGE_DESCRIPTION)

        self.parser_mr.add_argument('-s',
                                    '--source_branch',
                                    help=const.MERGE_SOURCE_DESCRIPTION,
                                    default='master')

        self.parser_mr.add_argument('-o',
                                    '--original_branch',
                                    help=const.MERGE_DST_DESCRIPTION,
                                    default='master')

        ###########
        # SETROLE #
        ###########
        self.parser_sr = subparsers.add_parser(
            'setrole', help=const.SETROLE_HELP_MSG,
            formatter_class=argparse.RawTextHelpFormatter)
        self.parser_sr.add_argument('-p',
                                    '--project',
                                    action=const.STORE_TRUE,
                                    help=const.SETROLE_PROJECT_FLAG_HELP)
        self.parser_sr.add_argument(
            'role', metavar='role', nargs='?', default=None,
            help=textwrap.dedent(const.ADDLDAP_ROLE))
        self.parser_sr.add_argument(
            'username', metavar='username', help=textwrap.dedent(
                const.SETROLE_USER_NAME))
        self.parser_sr.add_argument('group', nargs='+', metavar='group',
                                    help=textwrap.dedent(const.SETROLE_GROUP_NAME))

    def initialization(self, arguments):
        ###########
        # ADDLDAP #
        ###########
        if arguments.command == 'addldap':
            repo_name = 'all'
            group_name = arguments.group
            project_id = 'all'
        ##############
        # CLONEGROUP #
        ##############
        elif arguments.command == 'clonegroup':
            if not arguments.group:
                print(const.CLONEGROUP_PROBLEM)
                sys.exit(-1)
            repo_name = 'all'
            group_name = arguments.group[0]
            project_id = 'all'
        ################
        # CREATEGROUPS #
        ################
        elif arguments.command == 'creategroups':
            if not arguments.name:
                print(const.CREATEGROUP_PROBLEM)
                sys.exit(-1)
            repo_name = 'none'
            group_name = arguments.name
            project_id = 'none'
        ##################
        # CREATEPROJECTS #
        ##################
        elif arguments.command == 'createprojects':
            if not arguments.name:
                print(const.CREATEGROUP_PROBLEM)
                sys.exit(-1)
            repo_name = arguments.name
            group_name = arguments.group
            project_id = 'none'
        ########
        # FIND #
        ########
        elif arguments.command == 'find':
            repo_name = 'all'
            group_name = 'all'
            project_id = 'all'
        ########
        # FORK #
        ########
        elif arguments.command == 'fork':
            if arguments.project is None:
                print(const.PROBLEM_FETCHING_NAME_PROJECT)
                self.parser_fork.print_help()
                sys.exit(-1)
            if arguments.project.count('/') != 1:
                print(const.GROUP_PROJECT_BAD_FORMAT)
                self.parser_fork.print_help()
                sys.exit(-1)
            group_name = arguments.project.split('/')[0]
            repo_name = arguments.project.split('/')[1]
            if arguments.clean:
                forked_project = gitlab_utils.get_forked_project(
                    repo_name, arguments.clean, arguments.verbosity)
                if forked_project is not None:
                    project_id = forked_project['forked_from_project']['id']
                    gitlab_utils.delete_project(forked_project['id'])
                else:
                    print(const.IGNORE_CLEAN % (group_name, repo_name))
                    project_id = gitlab_utils.get_project_id(
                        group_name, repo_name)
            else:
                if not arguments.group:
                    project_id = gitlab_utils.get_project_id(
                        group_name, repo_name)
                else:
                    project_id = gitlab_utils.get_project_id_without_group(
                        repo_name)
        #########
        # LOGIN #
        #########
        elif arguments.command == 'login':
            # login/user has already been requested and token retrieved
            print(const.LOGIN_TEST)
            # verifies if access if correctly done
            gitlab_utils.verify_token()
            # exits
            sys.exit(-1)
        #########
        # MERGE #
        #########
        elif arguments.command == 'merge':
            group_name = None
            # Verify if project has been indicated
            project_indication = False
            repo_name = os.path.basename(os.getcwd())
            if arguments.project:
                project_indication = True
                if arguments.project.count('/') != 1:
                    print(const.GROUP_PROJECT_BAD_FORMAT)
                    self.parser_mr.print_help()
                    sys.exit(-1)
                group_name = arguments.project.split('/')[0]
                repo_name = arguments.project.split('/')[1]
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
                                        git_extracted_repo_name = line.split(
                                            '=')[-1].split('/')[-1][:-4]
                                    except:
                                        raise gitutils_exception.GitutilsError(
                                            const.GIT_MERGE_PROBLEM_0)
                                else:
                                    try:
                                        git_extracted_repo_name = line.split(
                                            '=')[-1].split('/')[-1].split('.')[0]
                                        group_name = line.split(
                                            '=')[-1].split('/')[-2]
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
        ###########
        # SETROLE #
        ###########
        elif arguments.command == 'setrole':
            role_access = None
            if not arguments.group:
                print(const.SETROLE_PROBLEM)
                sys.exit(-1)
            if arguments.role not in [
                    'guest', 'reporter', 'dev', 'maintainer', 'owner']:
                print(const.ROLE_ADDLDAP_PROBLEM)
                sys.exit(-1)
            else:
                role_access = gitlab_utils.check_role(arguments.role)
            repo_name = 'all'
            group_name = arguments.group
            project_id = 'all'
        else:
            self.parser.print_help()
            sys.exit(-1)
        return (repo_name, group_name, project_id)
