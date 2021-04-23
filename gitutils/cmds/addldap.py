from gitutils import const
from gitutils import gitlab_utils
from gitutils import gitutils_exception

def add_ldap(git_group, ldap_cn, role):
    """
    Assign ldap group sync to a git group
    :param ldap_cn: LDAP USER CN (common name)
    :type ldap_cn: str
    :param git_group: Git group that the ldap will be added
    :type git_group: str
    :param role: Role that will be given to the user
    :type role: str
    :return:
    """
    print(const.ADDLDAP_INIT_MSG % (
        const.bcolors.BOLD,
        ldap_cn,
        role,
        const.bcolors.ENDC,
        const.bcolors.BOLD,
        git_group,
        const.bcolors.ENDC,
    ))
    # verify if ldap_cn is a real ldap group
    list_of_ldap_cns = gitlab_utils.get_ldap_groups(ldap_cn)
    found = False
    # verifies if the ldap group is actually a ldap group
    for i in list_of_ldap_cns:
        if ldap_cn == i.attributes['cn']:
            found = True
    # gets group id
    group_id = -1
    try:
        group_id = gitlab_utils.get_group_id(git_group)
    except Exception as ex:
        raise gitutils_exception.GitutilsError(ex)
    if found is True and group_id != -1:
        gitlab_utils.addldapgroup(git_group, group_id, ldap_cn, role)
    else:
        gitutils_exception.GitutilsError(const.ADDLDAP_LDAP_NAME_PROBLEM)
