import os
import time
from gitutils import const
from gitutils import gitlab_utils


def clone_group(group_name=''):
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
    # clones all the projects from group
    for i in projects:
        # clones into repo
        os.system('git clone %s' % i['url'])
        # 2 sec sleep time in between:
        # Gitlab API refuses if there's no sleep in between
        # error: ssh_exchange_identification: read: Connection reset by peer
        time.sleep(2)
    # Finishing up, message to user
    print("All projects have been cloned. Exiting now...")