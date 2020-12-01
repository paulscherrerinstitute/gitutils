from gitutils import const
from gitutils import gitlab_utils
import time

def create_groups(group_names=[]):
    """
    It create groups based on the list provided.
    : param group_name : List of name(s) of group to be created
    : type group_name : list
    """
    total_group_names = len(group_names)
    if total_group_names < 1:
        gitutils_exception.GitutilsError(const.PROBLEM_CREATEGROUP_EMPTY)
    count = 1
    print(const.CREATEGROUP_START)
    for group_name in group_names:
        # check if group exists
        if not gitlab_utils.group_exists(group_name):
            print(const.CREATEGROUP_CREATING % (count, group_name), end="")
            gitlab_utils.create_group(group_name, "-")
            time.sleep(1)
            group_id = gitlab_utils.get_group_id(group_name)
            if group_id != -1:
                print(const.CREATEGROUP_ID % group_id)
            count += 1
        else:
            print(const.CREATEGROUP_TAKEN % group_name)
    print(const.CREATEGROUP_END % (count-1, total_group_names))