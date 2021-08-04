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
    : param pattern : Filter of repository patterns (3 characters)
    : type group_name : str
    """
    # check if group exists
    gitlab_utils.check_group_exists(group_name)
    # Gets all the projects from the group
    if not pattern:
        projects = gitlab_utils.get_group_projects(group_name)
    else:
        projects = []
        for pat in pattern:
            if len(pat) <= 2:
                print(const.CLONEGROUP_PATTERN_TOO_SHORT % pat)
            else:
                projs = gitlab_utils.get_group_projects(group_name, pat)
                for p in projs:
                    projects.append(p)

    if projects: 
        cloned_projects = []
        for i in projects:
            # clones into repo
            subprocess.call(['git', 'clone', i['url']])
            # cloned_projects.append(f'{i["name"]} (id {i["id"]})')
            cloned_projects.append("%s (id %s)" % (i['name'], i['id']))
            # 2 sec sleep time in between:
            # Gitlab API refuses if there's no sleep in between (too many requests)
            # error: ssh_exchange_identification: read: Connection reset by peer
            time.sleep(2)
        msg = const.CLONEGROUP_FINISH % cloned_projects
    else:
        msg = const.CLONEGROUP_EMPTY
    # Finishing up, message to user
    print(msg)
    return
