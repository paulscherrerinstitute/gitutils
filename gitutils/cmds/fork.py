from gitutils import const
from gitutils import gitlab_utils
import time
import os


def fork(verbosity,
         fork_group_indication='',
         group_name='',
         git_repository_id=None,
         git_repository='',
         no_clone=False):
    """
    Creates a fork repository of the repository given as parameter.
    :param git_repository_id: Id of the repository to be pulled.
    :type git_repository_id: int
    :param git_repository: Name of the repository to be pulled.
    :type git_repository: str
    :param no_clone: Flag to clone or not the forked repository.
    :type no_clone: bool
    :return:
    """
    # Message user about forking project
    print(const.FORK_PROJECT % (git_repository, git_repository_id))
    # fork
    try:
        new_project = gitlab_utils.fork_project(
            git_repository_id, fork_group_indication, group_name)
        time.sleep(2)
        info_msg = 'New project forked: [%s] (id: %s) - %s' % (
            new_project.attributes['path_with_namespace'],
            new_project.attributes['id'],
            new_project.attributes['http_url_to_repo'])
        print(info_msg)
    except Exception as ex:
        raise gitutils_exception.GitutilsError(ex)
    if not no_clone:
        ssh_url_to_repo = new_project.attributes['ssh_url_to_repo']
        http_url_to_original_repo = new_project.attributes[
            'forked_from_project']['http_url_to_repo']
        # waiting another 2 seconds before cloning - AFS gitserver issue
        time.sleep(2)
        # verify if there's a local folder and delete it
        gitlab_utils.check_existing_local_git(git_repository)

        try:
            os.system('git clone %s' % ssh_url_to_repo)
            time.sleep(2)
            os.chdir(git_repository)
        except Exception as ex:
            raise gitutils_exception.GitutilsError(ex)
        try:
            os.system('git remote add upstream %s' % http_url_to_original_repo)
            time.sleep(2)
        except Exception as ex:
            print(const.GIT_UPLINK_PROBLEM % http_url_to_original_repo)
    else:
        print("\nGitutils warning: "+const.FORK_NO_CLONE)
    return None
