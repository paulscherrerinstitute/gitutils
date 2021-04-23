from gitutils import const
from gitutils import gitlab_utils
from gitutils import gitutils_exception
import time


def merge(verbosity,
          git_repository='',
          git_repository_id='',
          description='',
          title=''):
    """
    Creates a merge request to merge a forked repository.
    :param git_group_id: Id of the group to be pulled from.
    :type git_group_id: int
    :param git_repository: Name of the repository to be pulled.
    :type git_repository: str
    :param description: Description of the merge request.
    :type description: str
    :param title: Title of the merge request.
    :type title: str
    :return:
    """
    git_username = gitlab_utils.get_username()
    if git_username == -1:
        raise gitutils_exception.GitutilsError(
            const.PROBLEM_CREATEGROUP_EMPTY)

    # Check if there is already a fork
    forked_project = gitlab_utils.get_forked_project(
        git_repository, False, verbosity)
    # If no title submitted by the user, default title
    if title is None:
        title = const.MERGE_DEFAULT_TITLE % gitlab_utils.get_username()

    if forked_project is None:
        raise gitutils_exception.GitutilsError(const.GIT_MERGE_PROBLEM_2)
    print(const.GIT_CREATE_MERGE_MSG)
    final_description = const.GIT_MERGE_DESCRIPTION_MSG \
        % git_username
    if description is not None:
        final_description += ' User description: ' + description

    # Merge will be from source and target masters branches
    source_branch = 'master'
    target_branch = 'master'

    merge_request = gitlab_utils.create_merge_request(
        (git_repository_id, source_branch),
        (forked_project['forked_from_project']['id'], target_branch),
        (title, final_description))

    if merge_request.attributes['id']:
        print(const.GIT_MERGE_SUCCESS
              % (merge_request.attributes['id'],
                 merge_request.attributes['created_at']))
