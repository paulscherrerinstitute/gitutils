from gitutils import const
from gitutils import gitlab_utils
from gitutils import gitutils_exception

def set_role(role, username, git_groups, project_flag):
    """
    Sets a role to a specified user in a specified group or project
    :param role: Role that will be given to the user.
    :type role: int
    :param username: Username
    :type username: str
    :param git_group: Group or project names
    :type git_group: list
    :param project_flag: Flag to indicate project-level role.
    :type project_flag: bool
    :return:
    """
    # gets user_id
    user_id = gitlab_utils.get_user_id(username)
    if user_id == -1:
        raise gitutils_exception.GitutilsError(const.ROLE_SETROLE_PROBLEM_USERID)
    #################
    # GROUP SETROLE #
    #################
    if not project_flag: 
        for git_group in git_groups:
            group_id = gitlab_utils.get_group_id(git_group)
            print(const.SETROLE_INIT_MSG % (
                const.bcolors.BOLD,
                role,
                const.bcolors.ENDC,
                const.bcolors.BOLD,
                username,
                user_id,
                const.bcolors.ENDC,
                const.bcolors.BOLD,
                git_group,
                group_id,
                const.bcolors.ENDC,
                ), end="")
            # gets group
            group = gitlab_utils.get_group(git_group)
            # adds member with the desired access level to the group
            group.members.create({'user_id': user_id,
                                    'access_level': role})
            # verification
            members = group.members.all(all=True)
            found = False
            for member in members:
                if member.attributes['username'] == username:
                    found = True
            if not found:
                print(' ⨯')
                raise gitutils_exception.GitutilsError(
                        const.SETROLE_PROJECT_VALIDATION_FAILS)
            print(' ✓')
    else:
        ###################
        # PROJECT SETROLE #
        ###################
        #git_groups has projects
        for project_name in git_groups:
            print(const.SETROLE_P_INIT_MSG % (
                const.bcolors.BOLD,
                username,
                role,
                const.bcolors.ENDC,
                const.bcolors.BOLD,
                project_name,
                const.bcolors.ENDC,
                ), end="")
            # gets group name
            group_name = gitlab_utils.get_project_group_simplified(project_name)
            # gets project id
            project_id = gitlab_utils.get_project_id(group_name,project_name)   
            # gets the project
            project = gitlab_utils.get_project(project_id)
            # adds member with the desired role to the project
            project.members.create({'user_id': user_id, 
                                    'access_level': role})
            # verification
            members = project.members.all(all=True)
            found = False
            for member in members:
                if member.attributes['username'] == username:
                    found = True
            if not found:
                print(' ⨯')
                raise gitutils_exception.GitutilsError(
                        const.SETROLE_PROJECT_VALIDATION_FAILS)
            print(' ✓')