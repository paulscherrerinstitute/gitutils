#####
Usage
#####

Gitutils
--------

.. code-block:: bash

usage: gitutils.py [-h] [-e ENDPOINT]
                   {addldap,clonegroup,creategroups,createprojects,find,fork,login,merge,setrole}
                   ...

GITUTILS is a tool to facilitate the server-side operations when developing software that uses git repositories.

optional arguments:
  -h, --help            show this help message and exit
  -e ENDPOINT, --endpoint ENDPOINT
                        Endpoint of the git server. Default: https://git.psi.ch

command:
  valid commands

  {addldap,clonegroup,creategroups,createprojects,find,fork,login,merge,setrole}
                        commands
    addldap             Add a ldap group user to a group.
    clonegroup          Clones all existing projects within a group.
    creategroups        Create a new group (or multiple).
    createprojects      Create a new project (or multiple) inside the specified group.
    find                General search inside all the groups/projects.
    fork                Creates a fork from the repository.
    login               Fetches the gitlab token (saved in ~/.gitutils_token).
    merge               Creates a request to merge the defined fork to the original repository.
    setrole             Sets the role for a specific user on a specific group or project (or multiple)

.. note:: To see the gitutils usage help, you can use::

      $ gitutils -h

Addldap
-------

.. code-block:: bash

      usage: gitutils.py addldap [-h] group ldapgroup [role]

      positional arguments:
      group       Group that the LDAP group will be added to.
      ldapgroup   LDAP group common name.
      role        The role defines the permissions. Options: guest, reporter, dev, maintainer, owner

optional arguments:
  -h, --help  show this help message and exit


.. note:: To see the addldap usage help, you can use::

      $ gitutils addldap -h

Clonegroup
----------

.. code-block:: bash

      usage: gitutils.py clonegroup [-h] group

      positional arguments:
      group       Group name

      optional arguments:
      -h, --help  show this help message and exit

.. note:: To see the clonegroup usage help, you can use::

      $ gitutils clonegroup -h

Creategroups
------------

.. code-block:: bash

      usage: gitutils.py creategroups [-h] name [name ...]

      positional arguments:
      name        Group name or multiple (if multiple groups should be created).

      optional arguments:
      -h, --help  show this help message and exit

.. note:: To see the creategroups usage help, you can use::

      $ gitutils creategroups -h

Createprojects
--------------

.. code-block:: bash

      usage: gitutils.py createprojects [-h] group name [name ...]

      positional arguments:
      group       Group name
      name        Name of the new project (or multiple separated with spaces).

      optional arguments:
      -h, --help  show this help message and exit

.. note:: To see the createprojects usage help, you can use::

      $ gitutils createprojects -h


Find
----
.. code-block:: bash

      usage: gitutils find [-h] term

      positional arguments:
      term        Term to search.

      optional arguments:
      -h, --help  show this help message and exit

.. note:: To see the find usage help, you can use::

      $ gitutils find -h


Fork
----

.. code-block:: bash

usage: gitutils.py fork [-h] [-n] [-c] [project]

positional arguments:
  project         (REQUIRED) Indicates the project to be forked. It must be indicated as follow:
                  - <group_name>/<project_name>.

optional arguments:
  -h, --help      show this help message and exit
  -n, --no_clone  Indicates that the forked project will not be cloned after forking. A fork
                  will be created on the server-side and no clone nor upstream will be
                  generated on the local git repository.
  -c, --clean     Flag to delete personal fork of the project.


.. note:: To see the fork usage help, you can use::

      $ gitutils fork -h

Merge
-----

.. code-block:: bash


      usage: gitutils merge [-h] [-t TITLE] [-p PROJECT] [-d DESCRIPTION] project

      optional arguments:
        -h, --help            show this help message and exit
        -t TITLE, --title TITLE
                               The title of the merge request that is going to be created.
        -p PROJECT, --project PROJECT
                              Indicates the project to be forked. It can be of four different formats:
                              - "" : (DEFAULT) The user doesn't provide this argument, the project's group and name
                                    will be fetched from the /.git/config folder within the path where the
                                    gitutils is being called.
                              - <group_name>/<project_name> : The user provides a combination of group_name and
                                    project_name divided by "/".
        -d DESCRIPTION, --description DESCRIPTION
                              The description of the merge request that is going to be created.

.. note:: To see the merge usage help, you can use::

      $ gitutils merge -h
             
setrole
-------

.. code-block:: bash

      usage: gitutils.py setrole [-h] [-p] role username group [group ...]

      positional arguments:
      role           The role defines the permissions. Options: guest, reporter, dev, maintainer, owner
      username       Username that will be given the role.
      group          Group in which the user will be given such role.

      optional arguments:
      -h, --help     show this help message and exit
      -p, --project  If indicated, the setrole gives the access on a project level (and not on the default group level).

.. note:: To see the setrole usage help, you can use::

      $ gitutils setrole -h