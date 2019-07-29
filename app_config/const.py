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
ROOT_ROUTE = urljoin(endpoint, "/")
SIGN_IN_ROUTE = urljoin(endpoint, "/users/sign_in")
PAT_ROUTE = urljoin(endpoint, "/profile/personal_access_tokens")
OAUTH_ROUTE = urljoin(endpoint, "/oauth/token")
OATH_REQUEST = urljoin(OAUTH_ROUTE, "?grant_type=password&username=")
PASSWORD_URL = "&password="
############
# MESSAGES #
############
EXCEPTION_TEMPLATE = "An exception of type {0} occurred. Arguments:\n{1!r}"
AUTHENTICATE_REQUEST = "To access your Gitlab account, please authenticate: "
LOGIN_REQUEST = "Username:"
PASSWORD_REQUEST = "Password:"
RETURN_PROBLEM = "problem"
NO_GITLAB_TOKEN = "Before executing this script make sure that you have set GITLAB_PRIVATE_TOKEN"
PROBLEM_USERNAME = "Problem getting the correct username. Please try again."
FORKED_EXISTS = "A forked repository with the name {} already exists"
REPO_EXISTS_NOT_FORK = "A repository with the name {} already exists but is not a fork"
FORK_PROJECT = "Fork project..."
FORK_WAIT = "Waiting for fork being created ..."
NO_FORK_CENTAL = "There is no fork on the central server"
REMOVE_LOCAL_CLONE = "Removing local clone"
CLONE_EXISTS = "Clone already exists"
CLONE_FORK = "Clone fork"
GIT_CREATE_MERGE_MSG = "Create merge request"
GIT_MERGE_PROBLEM = "Cannot create merge request as there is no forked"
GIT_MERGE_DESCRIPTION_MSG = 'The configuration was changed by %s'
GIT_PUSH_MSG = "Push changes to central server"
GIT_PULL_CONFIG_AVAILABLE = "Configuration is now available at: "
GIT_DELETE_FORK_MSG = "Delete fork"
GIT_UNABLE_TO_FIND_PROJECT_MSG = "Unable to find project %s - Aborting...\n"
GIT_UNSUPPORTED_CONFIG_MSG = "Unsupported configuration - supported configurations are:\n%s"
GIT_SUPPORTED_CONFIG_MSG = "Supported configurations are:\n%s"
#####################
# PARSE MSGS / HELP #
#####################
APP_CONFIG_TITLE_DESCRIPTION = 'Application configuration management utility'
BASEDIR_HELP_MSG = "Base directory to clone configurations to"
CONFIG_LIST_HELP_MSG = "List available configurations to be used"
CONFIG_HELP_MSG = "Configuration"
PULL_HELP_MSG = "pull configuration from central server"
PULL_CLEAN_HELP_MSG = "Create clean fork and clone"
PUSH_HELP_MSG = "push configuration from central server"
PUSH_MERGE_REQUEST_TITLE = "Merge request title"
COMMIT_HELP_MSG = "Commit configuration changes to local repository"
COMMIT_MESSAGE = "Commit message"
STORE_TRUE = "store_true"
############
# COMMANDS #
############
GIT_COMMIT_CMD = "git commit -a -m %s"
GIT_UPSTREAM_REPO_CMD = "git remote add upstream %s"
GIT_PUSH_CMD = "git push origin master"
GIT_CLONE_CMD = "git clone %s"
GIT_PULL_CMD = "git pull upstream master"