from gitutils import const
from gitutils import gitlab_utils
import time
import os 

def fork(
        fork_group_indication='',
        git_repository_id=None,
        git_repository='',
        no_clone=False,
        clean=False):
    """
    Creates a fork repository of the repository given as parameter.
    :param git_repository_id: Id of the repository to be pulled.
    :type git_repository_id: int
    :param git_repository: Name of the repository to be pulled.
    :type git_repository: str
    :param no_clone: Flag to clone or not the forked repository.
    :type no_clone: bool
    :param clean: Flag to clean or not the previously existing repository.
    :type clean: bool
    :return:
    """
    # checks if fork is executed inside git repo
    # gitlab_utils.is_git_repo()
    # Message user about forking project
    print(const.FORK_PROJECT % (git_repository, git_repository_id))
    # not cloning into the new repo
    if no_clone:
        # verify if there is an previously existing remote folder
        gitlab_utils.check_existing_remote_git(clean, git_repository_id, fork_group_indication)
        # Forks the repo
        new_project = gitlab_utils.fork_project(git_repository_id, fork_group_indication)
        # http_url_to_repo = new_project.attributes['http_url_to_repo']
    else:  # cloning into the new repo
        # verify if there is an previously existing local folder
        gitlab_utils.check_existing_local_git(clean, git_repository)
        # verify if there is an previously existing remote folder
        gitlab_utils.check_existing_remote_git(clean, git_repository_id, fork_group_indication)
        try:
            # Forks the repo
            new_project = gitlab_utils.fork_project(git_repository_id, fork_group_indication)
            ssh_url_to_repo = new_project.attributes['ssh_url_to_repo']
            http_url_to_original_repo = new_project.attributes[
                'forked_from_project']['http_url_to_repo']
        except Exception as ex:
            raise gitutils_exception.GitutilsError(ex)
        # Clone repository

        time.sleep(2) # waiting another 2 seconds before cloning - AFS gitserver issue
        os.system('git clone %s' % ssh_url_to_repo)

        # Change into git repository
        try:
            os.chdir(git_repository)
        except Exception as ex:
            raise gitutils_exception.GitutilsError(ex)

        # Add upstream repository
        # Configure Git to sync your fork with the original repository
        try:
            os.system('git remote add upstream %s' % http_url_to_original_repo)
        except Exception as ex:
            print(const.GIT_UPLINK_PROBLEM % http_url_to_original_repo)
    info_msg = 'New project forked: [%s] (id: %s) - %s' % (
        new_project.attributes['path_with_namespace'],
        new_project.attributes['id'],
        new_project.attributes['http_url_to_repo'])
    print(info_msg)