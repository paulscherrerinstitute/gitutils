import os
import subprocess
import time

from gitutils import const, gitlab_utils



def clone_group(group_name='', pattern=None):
    """
    Based on the group name, it clones all existing
    projects from the specified group.
    : param group_name : Name of group to be cloned
    : type group_name : str
    """
    # check if group exists
    gitlab_utils.check_group_exists(group_name)
    # Gets all the projects from the group
    projects = gitlab_utils.get_group_projects(group_name)
    # Filter name pattern
    if pattern:
        projects = gitlab_utils.filter_name_pattern(projects, pattern)

    # clones all the projects from group
    print(const.CLONEGROUP_WARNING)
    for i in projects:
        # clones into repo
        subprocess.call(['git', 'clone', i['http_url']])
        # 2 sec sleep time in between:
        # Gitlab API refuses if there's no sleep in between (too many requests)
        # error: ssh_exchange_identification: read: Connection reset by peer
        time.sleep(2)
    # Finishing up, message to user
    print(const.CLONEGROUP_FINISH)
