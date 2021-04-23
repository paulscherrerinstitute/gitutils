from gitutils import const, gitlab_utils
from gitutils.spinner import Spinner


def find(search_term, files_only):
    """
    Find command searches in all projects/repositories.
    :param search_term: Term to search in the content of files and filenames.
    :type search_term: str
    :return:
    """
    print(const.GREPFILE_INIT_MSG %
          (const.bcolors.BOLD, search_term, const.bcolors.ENDC))
    # get groups
    groups = gitlab_utils.get_groups()
    # search for files in groups
    with Spinner():
        for group in groups:
            gitlab_utils.find_file_by_id(
                search_term, groups[group], files_only)
