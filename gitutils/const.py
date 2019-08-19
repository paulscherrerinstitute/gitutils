from urllib.parse import urljoin


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
############
# MESSAGES #
############
EXCEPTION_TEMPLATE = "An exception of type {0} occurred. Arguments:\n{1!r}"
AUTHENTICATE_REQUEST = "To access your Gitlab account, please authenticate: "
LOGIN_REQUEST = "Username:"
PASSWORD_REQUEST = "Password:"
NO_GITLAB_TOKEN = "Before executing this script make sure that you have set GITLAB_PRIVATE_TOKEN"
PROBLEM_USERNAME = "Problem getting the correct username. Please try again."
FORKED_EXISTS = "A forked repository with the name {} already exists."
FORK_PROJECT = "Forking project %s..."
PROJECT_ID_NOT_FOUND = "Project id not found, please check the configuration details."
PROJECT_NAME_NOT_FOUND = "Project name not found, please check the configuration details."
MULTIPLE_PROJECTS= "Multiple projects with the same name found. Please, use the argument -p to indicate group name and project name."
PROJECT_URL_NOT_FOUND = "Project url not found, please check the configuration details."
GIT_CREATE_MERGE_MSG = "Creating merge request..."
GIT_MERGE_SUCCESS = "Merge request successfully created (merge request id: %s, created at %s)."
GIT_MERGE_PROBLEM = "Cannot create merge request as there is no forked."
GIT_MERGE_DESCRIPTION_MSG = 'The configuration was changed by %s'
GIT_UNABLE_TO_FIND_PROJECT_MSG = "Unable to find project - Aborting...\n"
GIT_UNABLE_TO_FIND_MASTER_BRANCH = "Unable to find master branch in project to merge - Aborting...\n"
#####################
# PARSE MSGS / HELP #
#####################
APP_CONFIG_TITLE_DESCRIPTION = 'GITUTILS utility'
BASEDIR_HELP_MSG = "Base directory to clone configurations to."
ENDPOINT_HELP_MSG = "Endpoint of the git server. Default: https://git.psi.ch"
FORK_PROJECT_MESSAGE = "Name of the project to be forked."
MERGE_PROJECT_MESSAGE = "Name of the project to be merged."
COMMAND_NOT_FOUND = "Command not found."
FORK_HELP_MSG = "Creates a fork from the repository."
FORK_NOCLONE_HELP = "If set no_clone, the repo will not be cloned after the fork."
MERGE_HELP_MSG = "Creates a request to merge the defined fork to the original repository."
MERGE_MESSAGE_TITLE = "Merge request title."
MERGE_MESSAGE_DESCRIPTION = "Merge request description."
STORE_TRUE = "store_true"
############
# COMMANDS #
############
GIT_COMMIT_CMD = "git -C %s commit -m \"%s\""
GIT_UPSTREAM_REPO_CMD = "git remote add upstream %s"
GIT_PUSH_CMD = "git push"
GIT_CLONE_CMD = "git clone %s"
GIT_ADD_ALL = "git add ."
GIT_PULL_CMD = "git pull"
GIT_PULL_UPSTREAM_MASTER_CMG = "git pull upstream master"
GIT_GET_CURRENT_BRANCH = "git rev-parse --abbrev-ref HEAD"
