from urllib.parse import urljoin

NOTIFICATION_LEVEL_DISABLED = "disabled"
NOTIFICATION_LEVEL_PARTICIPATING = "participating"
NOTIFICATION_LEVEL_WATCH = "watch"
NOTIFICATION_LEVEL_GLOBAL = "global"
NOTIFICATION_LEVEL_MENTION = "mention"
NOTIFICATION_LEVEL_CUSTOM = "custom"

VISIBILITY_PRIVATE = 0
VISIBILITY_INTERNAL = 10
VISIBILITY_PUBLIC = 20

ENDPOINT = "https://git.psi.ch"
ROOT_ROUTE = urljoin(endpoint, "/")
SIGN_IN_ROUTE = urljoin(endpoint, "/users/sign_in")
PAT_ROUTE = urljoin(endpoint, "/profile/personal_access_tokens")
OAUTH_ROUTE = urljoin(endpoint, "/oauth/token")
OATH_REQUEST = urljoin(OAUTH_ROUTE, "?grant_type=password&username=")
PASSWORD_URL = "&password="

EXCEPTION_TEMPLATE = "An exception of type {0} occurred. Arguments:\n{1!r}"

AUTHENTICATE_REQUEST = "To access your Gitlab account, please authenticate: "
LOGIN_REQUEST = "Username:"
PASSWORD_REQUEST = "Password:"

RETURN_PROBLEM = "problem"