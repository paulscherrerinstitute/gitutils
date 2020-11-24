from urllib.parse import urljoin


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

######################
# NOTIFICATION LEVEL #
######################
NOTIFICATION_LEVEL_DISABLED = "disabled"
NOTIFICATION_LEVEL_PARTICIPATING = "participating"
NOTIFICATION_LEVEL_WATCH = "watch"
NOTIFICATION_LEVEL_GLOBAL = "global"
NOTIFICATION_LEVEL_MENTION = "mention"
NOTIFICATION_LEVEL_CUSTOM = "custom"
####################
# VISIBILITY LEVEL #
####################
VISIBILITY_PRIVATE = 0
VISIBILITY_INTERNAL = 10
VISIBILITY_PUBLIC = 20
##########
# ROUTES #
##########
ENDPOINT = "https://git.psi.ch"
OAUTH_ROUTE = urljoin(ENDPOINT, "/oauth/token")
OATH_REQUEST = urljoin(OAUTH_ROUTE, "?grant_type=password&username=")
PASSWORD_URL = "&password="

SEARCH_ROUTE= urljoin(ENDPOINT, "/search?")
CODE_URL ="&search_code=true"
############
# MESSAGES #
############
EXCEPTION_TEMPLATE = "An exception of type {0} occurred. Arguments:\n{1!r}"
AUTHENTICATE_REQUEST = "To access your Gitlab account, please authenticate: "
AUTHENTICATE_REQUEST_INVALID_TOKEN = "Git token found is not valid. To access your Gitlab account, please authenticate: "
UPDATE_TOKEN = "Updating token in file ~/.gitutils_token ..."
LOGIN_REQUEST = "Username:"
PASSWORD_REQUEST = "Password:"
NO_GITLAB_TOKEN = "Before executing this script make sure that you have set GITLAB_PRIVATE_TOKEN"
PROBLEM_USERNAME = "Problem getting the correct username. Please try again."
FORKED_EXISTS = "A forked repository with the same name already exists. Use -c to clean existing fork."
FORK_PROJECT = "Forking project %s (id: %s)..."
PROJECT_ID_NOT_FOUND = "Project id not found. Please, indicate group name and project name or check if you have permission to access such group/project."
PROJECT_NAME_NOT_FOUND = "Project name not found. Please, indicate group name and project name or check if you have permission to access such group/project."
GIT_INCONSISTENCY_NAME = "The name of the project extracted from the .git/config and the folder are not equal."
PROJECT_FOUND_NOT_FORK = "The requested project is not a fork. Gitutils is not able to continue..."
PROJECT_FORK_NAME_ERROR = "The requested project has been forked from a different repository. Gitutils is not able to continue..."
GROUP_NOT_SPECIFIED_ASSUME_USER = "The group was not specified. Default is to use your personal project."
MULTIPLE_PROJECTS = "Multiple projects with the same name found under different groups. Please, indicate group name and project name. List of groups found: %s"
DELETING_LOCAL_STORAGE = "Deleting local folder..."
GIT_FORK_PROBLEM_MULTIPLE = "Not possible to fork the requested project. There is already one fork under the personal group with the same name. Use the argument -c to clean previous personal forks."
FORK_PROBLEM_FOLDER = "Existing folder with the same name. Please indicate -c if you want to delete local files or use the fork command on a different folder."
FORK_PROBLEM_REMOTE = "Existing repo with the same name. Please indicate -c if you want to delete the remote repo."
FORK_PROBLEM_GIT_FOLDER = "Fork is not recommended inside a repository folder. Please execute the fork command outside a repository folder."
FORK_PROBLEM_PERSONAL = "Not possible to fork your own personal project."
CLONEGROUP_PROBLEM = "Not possible to clonegroup if the group name parameter is not provided. Use 'gitutils clonegroup -h' for help."
SEARCHFILE_PROBLEM = "Not possible to search for a file if the group or file are not provided. Use 'gitutils search -h' for help."
FORK_GROUP_NOT_FOUND = "The requested fork project could not be found under the specified group or check if you have permission to access such group/project."
GROUP_NAME_PROBLEM = "The requested project was found under a different group or check if you have permission to access such group/project."
PROJECT_URL_NOT_FOUND = "Project url not found, please check the configuration details or check if you have permission to access such group/project.."
GROUP_PROJECT_BAD_FORMAT = "Please use the following format: <group_name>/<project_name>"
FULL_GROUP_PROJECT_BAD_FORMAT = "Please use the following format: https://git.psi.ch/<group_name>/<project_name>"
GIT_CREATE_MERGE_MSG = "Creating merge request..."
DELETING_EXISTING_FORK = "Deleting existing fork..."
NO_PERSONAL_FORK = "Impossible to delete. The desired project is not under your personal projects."
NO_PERSONAL_FORK_PERMISSIONS = "The desired project is not under your personal projects, this action depends on your permissions."
DELETE_SUCCESS = "Project successfully deleted. Waiting 4 seconds of idle time after deleting a project to let the server process it."
GROUP_PARAMETER_EMPTY = "The group provided as parameter was not found. Please check for typo or if the group really exists."
GIT_MERGE_SUCCESS = "Merge request successfully created (merge request id: %s, created at %s)."
GIT_CONFIG = "Forked group and project extracted from .git/config: "
GIT_MERGE_PROBLEM = "Cannot create merge request as there is no forked."
GIT_MERGE_PROBLEM_0 = "Cannot create merge. Problem while extracting group and project name from .git/config file."
GIT_MERGE_PROBLEM_1 = "Cannot create merge. Git config file not found and project not indicated by user. Use -p <group_name>/<project_name>."
GIT_MERGE_PROBLEM_2 = "Cannot create merge. Forked project was not found or check if you have permission to access such group/project.."
GIT_UPLINK_PROBLEM = "Problem creating the upstream link. Please do it mannualy with the command: \'git remote add upstream %s\'"
PROBLEM_FETCHING_NAME = "Problem fetching the group and projects name. Please check if the group and projects are correct and if you have the correct permissions to access such repository."
CLEAN_PROBLEM = "Gitutils is not able to delete a repo that is not a fork."
GIT_MERGE_DESCRIPTION_MSG = 'The configuration was changed by %s.'
SSH_GIT_GIT = 'git@git'
MERGE_DUPLICATED = 'Another open merge request already exists for this source branch'
GIT_UNABLE_TO_FIND_PROJECT_MSG = "Unable to find project - Aborting...\n"
GIT_UNABLE_TO_FIND_MASTER_BRANCH = "Unable to find master branch in project to merge - Aborting...\n"
GIT_PATHNAME_IS_TAKEN = 'has already been taken'
MERGE_DEFAULT_TITLE = "Merge request submitted by %s."

#####################
# PARSE MSGS / HELP #
#####################
GITUTILS_TITLE_DESCRIPTION = 'GITUTILS is a tool to facilitate the server-side operations when developing software that uses git repositories.'
BASEDIR_HELP_MSG = "Base directory to clone configurations to."
ENDPOINT_HELP_MSG = "Endpoint of the git server. Default: https://git.psi.ch"
FORK_PROJECT_MESSAGE = '''(REQUIRED) Indicates the project to be forked. It can be of three different formats:
- https://git.psi.ch/<group_name>/<project_name> : The user provides
   the direct http to the git repository.
- <group_name>/<project_name> : The user provides a combination of
   group_name and project_name divided by \"/\".
- <project_name> : The user provides the name of the project name.
   Gitutils will fetch the name of the group (keep in mind, that this may
   cause ambiguity problems).'''
MERGE_PROJECT_MESSAGE = '''Indicates the project to be forked. It can be of four different formats:
- \"\" : (DEFAULT) The user doesn't provide this argument, the project's group and name
      will be fetched from the /.git/config folder within the path where the
      gitutils is being called.
- https://git.psi.ch/<group_name>/<project_name> : The user provides the direct
      http to the git repository.
- <group_name>/<project_name> : The user provides a combination of group_name and
      project_name divided by "/".
- <project_name> : The user provides the name of the project name. Gitutils will
      fetch the name of the group (keep in mind, that this may cause ambiguity
      problems).'''
FORK_CLEAN_MSG = '''Indicates to delete any existing fork project under your personal group.
This might be necessary to fork and clone into a clean copy of the original
repository. The desired forked project must not be a pre-existing forked
project under your personal projects.'''
FORK_GROUP_MSG = ''' Indicates the group that the fork is going to be created. The default is the username.'''
COMMAND_NOT_FOUND = "Command not found."
FORK_HELP_MSG = "Creates a fork from the repository."
FORK_NOCLONE_HELP = '''Indicates that the forked project will not be cloned after forking. A fork
will be created on the server-side and no clone nor upstream will be
generated on the local git server.'''
LOGIN_HELP_MSG = "Fetches the gitlab token (saved in ~/.gitutils_token)."
LOGIN_TEST = "As a verification for the gitutils-gitlab token, gitutils will fetch the list of groups..."
LOGIN_PROBLEM = "Problem with the token. Please, check your credentials."
LOGIN_SUCCESS = "Credentials successfully stored and token is valid.."
MERGE_HELP_MSG = "Creates a request to merge the defined fork to the original repository."
MERGE_MESSAGE_TITLE = ''' The title of the merge request that is going to be created.'''
MERGE_MESSAGE_DESCRIPTION = '''The description of the merge request that is going to be created.'''
CLONEGROUP_HELP_MSG = "Clones all existing projects within a group."
CLONEGROUP_GROUP_NAME = "Group name"
SEARCHFILE_HELP_MSG = "DEPRECATED. Use find instead."
SEARCHFILE_FILE_MSG = "File's name."
GREP_PROJECT_MSG = "Project's name."
GREP_TERM_MSG = "Term to search."
SEARCHFILE_GROUP_MSG = "Group's name"
SEARCHFILE_INIT_MSG = '\nGitutils searching inside group%s %s %sfor file%s %s %s...'
GREPFILE_INIT_MSG = '\nGitutils searching inside project%s %s %sfor term \"%s %s %s\"...'
GREPFILE_PROBLEM = "Not possible to search for a term if the project or the term itself are not provided. Use 'gitutils grep -h' for help."
GREPFILE_HELP_MSG = "DEPRECATED. Use find instead."
GREP_EMPTY = "The term %s %s %s was not found in such project."
SEARCHFILE_EMPTY = "The file %s %s %s was not found in such group."
STORE_TRUE = "store_true"
BLOBS = 'blobs'
GREPFILE_INIT_MSG = '\nGitutils searching for term \"%s %s %s\"...'
ADDLDAP_INIT_MSG = '\nGitutils adding ldap group %s %s %s to group %s %s %s ...'
ADDLDAP_LDAP_GROUP_PROBLEM= "ldap_cn needs to be unique."
ADDLDAP_PROBLEM = "Not possible to add ldap group to a group if both are not provided. Use 'gitutils addldap -h' for help."
ADDLDAP_HELP_MSG = "Add a ldap group user to a group."
ADDLDAP_LDAP_GROUP_NAME = "LDAP group common name."
ADDLDAP_GROUP_NAME = "Group that the LDAP group will be added to."
ADDLDAP_GROUP_PROBLEM = "The group id to be added wasn't found."
ADDLDAP_SUCCESS_MSG = "The LDAP group %s %s %s was successfully added to group %s %s %s. Syncing and exiting now...\n"
FIND_HELP_MSG = "General search inside all the groups/projects."
DEPRECATED_GREP_SEARCH = "Grep and search are deprecated. Gitutils will use find %s instead."
CREATEGROUP_HELP_MSG = "Create a new group (or multiple)."
CREATEGROUP_GROUP_NAME = "Group name to be created (or multiple separated with spaces)."
CREATEGROUP_PROBLEM = "Not possible to creategroup if the group name parameter is not provided. Use 'gitutils creategroup -h' for help."
PROBLEM_CREATEGROUP_EMPTY = "Not possible to create groups if no name is provided. Use 'gitutils creategroup -h' for help."
CREATEGROUP_CREATING = "\t %s) %s "
CREATEGROUP_START = "\nGitutils creategroups...\n"
CREATEGROUP_TAKEN = "Group %s already exists."
CREATEGROUP_END = "\nGitutils creategroups summary: \n\tgroups created: %s/%s.\n"
CREATEPROJECT_HELP_MSG = "Create a new project (or multiple) inside the specified group."
PROBLEM_CREATEPROJECT_EMPTY = "Not possible to create projects if no name is provided. Use 'gitutils createprojects -h' for help."
CREATEPROJECT_GROUP_NAME = "Group name"
CREATEPROJECT_PROJECTS_NAME = "Name of the new project (or multiple separated with spaces)."
CREATEPROJECT_NOGROUP = "\nGroup %s doesn't exist. Creating group %s first..."
CREATEPROJECT_TAKEN = "\t %s) Group %s already has a project named %s. This will be skipped."
CREATEGROUP_ID = " (id: %s) ✓\n"
CREATEPROJECT_CREATING = "\t %s) %s "
CREATEPROJECT_START = "\nGitutils createprojects: creating project in group %s %s (id: %s) %s ...\n"
CREATEPROJECT_END = "\nGitutils createprojects summary: \n\tprojects created: %s/%s.\n"
############
# COMMANDS #
############
GIT_COMMIT_CMD = "git -C %s commit -m \"%s\""
GIT_UPSTREAM_REPO_CMD = "git remote add upstream %s"
GIT_CLONE_CMD = "git clone %s"
GIT_PULL_UPSTREAM_MASTER_CMG = "git pull upstream master"
GIT_GET_CURRENT_BRANCH = "git rev-parse --abbrev-ref HEAD"
GIT_IS_REPO_PATH = "git rev-parse --is-inside-work-tree"
GIT_TOKEN_FILE = "/.gitutils_token"
