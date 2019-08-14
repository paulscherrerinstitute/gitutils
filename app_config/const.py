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
ROOT_ROUTE = urljoin(ENDPOINT, "/")
SIGN_IN_ROUTE = urljoin(ENDPOINT, "/users/sign_in")
PAT_ROUTE = urljoin(ENDPOINT, "/profile/personal_access_tokens")
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
PROBLEM_OAUTH = "Problem authenticating. Please try again."
PROBLEM_DELETING_PROJECT = "Problem deleting project."
FORKED_EXISTS = "A forked repository with the name {} already exists."
FORKED_PULL = "Pulling from the existing forked repository with the name {}."
NOT_ABLE_TO_DELETE_NON_PERSONAL_REPO = "The existing repository with the name {} is not under your personal projects. Impossible to delete, forking into a personal workspace otherwise."
DELETE_PERSONAL_PROJECT= "The existing repository with the name {} is will be deleted and a new fork is going to be created."
FORK_PROJECT = "Forking project %s..."
PERSONAL_FORK = "Fork project into an own personal group..."
PROJECT_ID_NOT_FOUND = "Project id not found, please check the configuration details."
PROJECT_NAME_NOT_FOUND = "Project name not found, please check the configuration details."
MULTIPLE_PROJECTS= "Multiple projects with the same name found. Please, use the argument -p to indicate group name and project name."
PROJECT_URL_NOT_FOUND = "Project url not found, please check the configuration details."
FORK_WAIT = "Waiting for fork being created ..."
FORK_PROBLEM = "Problem while forking..."
NO_FORK_CENTAL = "There is no fork on the central server."
REMOVE_LOCAL_CLONE = "Removing local clone.."
CLONE_EXISTS = "Clone already exists"
CLONE_FORK = "Cloning into fork..."
PROBLEM = "PROBLEM"
GIT_CREATE_MERGE_MSG = "Creating merge request..."
GIT_MERGE_SUCCESS = "Merge request successfully created (merge request id: %s, created at %s)."
GIT_MERGE_PROBLEM = "Cannot create merge request as there is no forked."
GIT_MERGE_DESCRIPTION_MSG = 'The configuration was changed by %s'
GIT_PUSH_MSG_CENTRAL_SERVER = "Pushings changes to central server..."
GIT_PUSHED = "Successfully pushed changes to central server repository %s."
GIT_PULL_CONFIG_AVAILABLE = "Configuration is now available at: "
GIT_DELETE_FORK_MSG = "Delete fork"
GIT_UNABLE_TO_FIND_PROJECT_MSG = "Unable to find project - Aborting...\n"
GIT_UNABLE_TO_FIND_MASTER_BRANCH = "Unable to find master branch in project to merge - Aborting...\n"
GIT_UNSUPPORTED_CONFIG_MSG = "Unsupported configuration - supported configurations are:\n%s"
GIT_SUPPORTED_CONFIG_MSG = "Supported configurations are:\n%s"
#####################
# PARSE MSGS / HELP #
#####################
APP_CONFIG_TITLE_DESCRIPTION = 'Application configuration management utility'
BASEDIR_HELP_MSG = "Base directory to clone configurations to."
ENDPOINT_HELP_MSG = "Endpoint of the repository. Default: https://git.psi.ch"
CONFIG_LIST_HELP_MSG = "List available configurations to be used"
CONFIG_HELP_MSG = "Configuration"
FORK_PROJECT_MESSAGE = "Name of the project to be forked."
MERGE_PROJECT_MESSAGE = "Name of the project to be merged."
COMMAND_NOT_FOUND = "Command not found."
PULL_HELP_MSG = "pull configuration from central server"
PULL_CLEAN_HELP_MSG = "Create clean fork and clone"
FORK_HELP_MSG = "Creates a fork from the repository."
FORK_NOCLONE_HELP = "If set no_clone, the repo will not be cloned after the fork."
PUSH_HELP_MSG = "push configuration from central server"
PUSH_MERGE_REQUEST_TITLE = "Merge request title"
COMMIT_HELP_MSG = "Commit configuration changes to local repository"
COMMIT_MESSAGE = "Commit message"
MERGE_CLEAN_HELP_MSG = "If set, the merged fork will be deleted."
MERGE_HELP_MSG = "Creates a request to merge the defined fork to the original repository."
MERGE_MESSAGE = "Name of the merge request."
MERGE_MESSAGE_TITLE = "Merge request title."
MERGE_MESSAGE_LABELS = "Merge request labels."
MERGE_MESSAGE_DESCRIPTION = "Merge request description."
MERGE_MESSAGE_TB = "Target branch name. By default it is used the master branch."
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
