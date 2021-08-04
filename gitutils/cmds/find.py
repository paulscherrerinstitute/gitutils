from gitutils import const, gitlab_utils
from gitutils.spinner import Spinner


def find(search_term, files_only, verbosity):
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
    if verbosity:
        print(" Verbose Gitutils: ")
    # search for files in groups
    with Spinner():
        for group in groups:
            if verbosity:
                print("\t Searching inside group: ",
                      groups[group]['name'], "(id ", groups[group]['id'], ").")
            gitlab_utils.find_file_by_id(
                search_term, groups[group], files_only, verbosity)
    if verbosity:
        print("\t Gitutils exiting...")
