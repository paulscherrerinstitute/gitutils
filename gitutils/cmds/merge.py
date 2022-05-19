import time

from gitutils import const, gitlab_utils, gitutils_exception


def merge(verbosity,
          git_repository='',
          git_repository_id='',
          description='',
          title='',
          source_branch='',
          target_branch=''
          ):
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
    if verbosity:
        print(" Verbose Gitutils: ")
    git_username = gitlab_utils.get_username()
    if verbosity:
        print(" \t (-v) Gitutils merge username: ", git_username)
    if git_username == -1:
        raise gitutils_exception.GitutilsError(
            const.PROBLEM_CREATEGROUP_EMPTY)

    # Check if there is already a fork
    forked_project = gitlab_utils.get_forked_project(
        git_repository, False, verbosity)
    # If no title submitted by the user, default title
    if title is None:
        title = const.MERGE_DEFAULT_TITLE % gitlab_utils.get_username()
    if verbosity:
        print(" \t (-v) Gitutils merge title: ", title)

    if forked_project is None:
        if verbosity:
            print(" \t (-v) Gitutils merge forked project not found.")
        raise gitutils_exception.GitutilsError(const.GIT_MERGE_PROBLEM_2)
    print(const.GIT_CREATE_MERGE_MSG)
    final_description = const.GIT_MERGE_DESCRIPTION_MSG \
        % git_username
    if description is not None:
        final_description += f' User description: {description}'
    if verbosity:
        print(" \t (-v) Gitutils merge definition: ", title)

    try:
        forked_from_project_id = forked_project['forked_from_project']['id']
    except:
        raise gitutils_exception.GitutilsError(
            const.GIT_MERGE_PROBLEM_3)

    try:
        if verbosity:
            print(" \t (-v) Gitutils forked project details: ",
                  forked_from_project_id)
        merge_request = gitlab_utils.create_merge_request(
            (git_repository_id, source_branch),
            (forked_project['forked_from_project']['id'], target_branch),
            (title, final_description))

        if merge_request.attributes['id']:
            print(const.GIT_MERGE_SUCCESS
                  % (merge_request.attributes['id'],
                     merge_request.attributes['created_at']))
    except Exception as ex:
        raise gitutils_exception.GitutilsError(ex)
