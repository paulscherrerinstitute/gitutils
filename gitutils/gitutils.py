#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
import os
import logging
import argparse
import textwrap
import time

from gitutils import gitlab_utils
from gitutils import gitutils_parser
from gitutils import gitutils_exception
from gitutils import const
from gitutils.cmds.addldap import add_ldap
from gitutils.cmds.merge import merge
from gitutils.cmds.setrole import set_role
from gitutils.cmds.clonegroup import clone_group
from gitutils.cmds.creategroups import create_groups
from gitutils.cmds.createprojects import create_projects
from gitutils.cmds.find import find
from gitutils.cmds.fork import fork


def main():
    """
    Main function for gitutils that parses the arguments and
    calls the corresponding method. It is in charge of detecting
    important parameters based on the arguments and treat some
    of the possible errors that might occur.
    """

    # creates the parses
    parser = gitutils_parser.Parser()
    # gets the arguments
    arguments = parser.get_arguments()
    # verifies if there are any arguments
    if arguments.command is None:
        parser.print_help()
        sys.exit(-1)
    # sets the endpoins
    gitlab_utils.set_endpoint(arguments.endpoint)
    # Authenticate user
    gitlab_utils.authenticate()
    ##################
    # INITIALIZATION #
    ##################
    if arguments.verbosity:
        print("\n Gitutils:")
        fmt = '{:<20}{:<20}{}'
        print(fmt.format('', 'Parameter', 'Value'), "\n")
        for i, arg in enumerate(vars(arguments)):
            print(fmt.format(i, arg, getattr(arguments, arg)))
        print("\n")
    # retrieve repository and group names
    (repo_name, group_name, project_id) = (None, None, None)
    # initialization routine
    (repo_name, group_name, project_id) = parser.initialization(arguments)

    # Command, group and repo are ok
    if arguments.command and \
            repo_name is not None and \
            group_name is not None and \
            project_id is not None:

        # list of commands
        list_of_cmds = ['addldap',
                        'clonegroup',
                        'creategroups',
                        'createprojects',
                        'find',
                        'fork',
                        'login',
                        'merge',
                        'setrole']

        try:
            # consider changing this to dictionary
            if arguments.command == 'addldap':
                role_access = gitlab_utils.get_role(arguments.role)
                if not arguments.ldapgroup:
                    print(const.ADDLDAP_PROBLEM)
                    sys.exit(-1)
                add_ldap(git_group=group_name,
                         ldap_cn=arguments.ldapgroup,
                         role=role_access)
            elif arguments.command == 'clonegroup':
                clone_group(group_name=group_name)
            elif arguments.command == 'creategroups':
                create_groups(group_names=group_name)
            elif arguments.command == 'createprojects':
                create_projects(
                    group_name=group_name[0], project_names=repo_name)
            elif arguments.command == 'find':
                find(arguments.term[0], arguments.file)
            elif arguments.command == 'fork':
                fork(fork_group_indication=arguments.group,
                     group_name=group_name,
                     git_repository_id=project_id,
                     git_repository=repo_name,
                     no_clone=arguments.no_clone,
                     verbosity=arguments.verbosity)
            elif arguments.command == 'merge':
                merge(git_repository=repo_name,
                      git_repository_id=project_id,
                      description=arguments.description,
                      title=arguments.title,
                      verbosity=arguments.verbosity)
            elif arguments.command == 'setrole':
                role_access = gitlab_utils.get_role(arguments.role)
                set_role(role=role_access,
                         username=arguments.username,
                         git_groups=group_name,
                         project_flag=arguments.project)
            elif arguments.command not in list_of_cmds:
                print(const.COMMAND_NOT_FOUND)
                parser.print_help()
                exit(-1)
        except Exception as e:
            print(str(e))


if __name__ == '__main__':
    main()
