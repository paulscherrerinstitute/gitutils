from gitutils import const
from gitutils import gitlab_utils
import time


def create_projects(group_name, project_names=[]):
    """
    It create groups based on the list provided.
    : param group_name : group name in which the projects will be created
    : type group_name : str
    : param project_names : List of name(s) of group to be created
    : type project_names : list
    """
    total_proj_names = len(project_names)
    group_id = 0
    # checks if group exists and create if it doesnt exists yet
    if not gitlab_utils.group_exists(group_name):
        # if not, creates the new group
        print(const.CREATEPROJECT_NOGROUP % (group_name, group_name))
        print(const.CREATEGROUP_CREATING % (1, group_name), end="")
        gitlab_utils.create_group(group_name, "-")
        time.sleep(1)
        group_id = gitlab_utils.get_group_id(group_name)
        if group_id != -1:
            print(const.CREATEGROUP_ID % group_id)
    # if group existed before
    if group_id == 0:
        group_id = gitlab_utils.get_group_id(group_name)
    # gets all projects from this group
    group_projects = gitlab_utils.get_group_projects(group_name)

    # iterates over all entries of new projects
    count = 1
    print(const.CREATEPROJECT_START % (
        const.bcolors.BOLD,
        group_name,
        group_id,
        const.bcolors.ENDC
    ))
    for project in project_names:
        skip_proj = False
        for existing_project in group_projects:
            if existing_project['name'] == project:
                print(const.CREATEPROJECT_TAKEN % (count, group_name, project))
                skip_proj = True
        if not skip_proj:
            print(const.CREATEPROJECT_CREATING % (count, project), end="")
            new_proj = gitlab_utils.create_project(group_id, project)
            project_id = gitlab_utils.get_project_id(group_name, project)
            if project_id != -1:
                print(const.CREATEGROUP_ID % project_id)
            count += 1
    print(const.CREATEPROJECT_END % (count-1, total_proj_names))
