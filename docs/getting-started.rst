#############################
Getting started with Gitutils
#############################

It is assumed that the gitutils' user is familiar with basic git commands (as add, commit, push and pull). If not, we refer to in `atlassian tutorial`_ to learn the basics.

.. _atlassian tutorial : https://www.atlassian.com/git/tutorials

Before any command, a token will be fetched to validate the access to the gitlab server. If the user wants to create the token without any specific command, one can use::

    $ gitutils login

A file (~/.gitutils_token) will be created on the home directory and it will store the token. 

Fork Walk-through
-----------------
1. Define a project to fork and issue the command. Once a repository is forked, it also creates a local clone and an upstream link to the reference repository. Arguments: **-p**, **-n**, **-c**. Examples:

    - To fork and clone into a repository, use the following command::

        $ gitutils fork <group_name>/<repository_name>

    - To fork and not clone, add the directive **-n** at the end of the previous command, as in::

            $ gitutils fork -n <group_name>/<repository_name> 

    - To delete existing fork and create a clean fork of a repository, use the following command::

            $ gitutils fork -c <group_name>/<repository_name> 

    - To fork (using the full path), clean existing fork and not clone an existing repository::

            $ gitutils fork  -n -c https://git.psi.ch/<group_name>/<repository_name>

2. Implement the changes/development necessary on the forked repository.
3. Add all changes, commit and push the changes to your forked repository using git command line, as in::

    $ git add .
    $ git commit -m <commit_message>
    $ git push


.. note:: When a successful fork happens, it already creates the upstream link. This is done automatically. Therefore, to synchronize your fork with the current state of the original repository and deal with possible merge conflicts, do the following::

    $ git fetch upstream
    $ git merge upstream/master

Merge Walk-through
------------------
1. Once all the necessary changes/development have been commited and pushed to a forked repository.
2. Navigate to the home folder of your forked repository (where the ``/.git`` folder is). Issue the command to merge. Arguments:**-t**, **-d**, **-p**.
    - To create a merge request for a repository, use the following command while on a git repository folder::

        $ gitutils merge -t <title> -d <description>

    - To create a merge request for a repository by using the argument **-p** to indicate the project::

        $ gitutils merge -p <group_name>/<repository_name> -t <title> -d <description>

    - To create a merge request indicating the full-path to the repository and without giving a description::

        $ gitutils merge -p https://git.psi.ch/<group_name>/<repository_name> -t <title>

.. note:: Gitutils will assume the command is being executed on the git repository folder. Alternatively, one can use the directive **-p** to indicate directly which project should be merged. If title or description are not provided by the user, default values are going to be used.


Find
----

1. The find command will do a general search for all projects and groups.

    - To search for term:

        $ gitutils find <term>
    
    .. note:: This task can take some minutes depending the number of groups and projects. 

    - The output will display the group and the enumerated matching cases according to this example:

    .. code-block:: bash

        Gitutils searching for term " S10CB04-CVME-DBAMT1 "...
        Group:  archiver_config 
            1 )   S10CB04-CVME-DBAMT1  :

            Weblink: https://git.psi.ch/archiver_config/sf_archapp/blob/master/S_DI_BAM_S10CB04-DBAMT1.config#L6

                    #  BAM vme ioc cpu/memory usage
                    #
                    S10CB04-CVME-DBAMT1:MEM_USED                    Monitor 1 60
                    S10CB04-CVME-DBAMT1:MEM_FREE                    Monitor 1 60
                    S10CB04-CVME-DBAMT1:IOC_CPU_LOAD                Monitor 1 60
                    S10CB04-CVME-DBAMT1:UPTIME                      Monitor 1 60
                    S10CB04-CVME-DBAMT1:STATUS                      Monitor 1 60
                    #
                    S10CB04-CVME-DBAMT2:MEM_USED                    Monitor 1 60

Clonegroup
----------

1. The clonegroup command clones all the existing projects from a specified group.
    - To clone all projects of group_name:

        $ gitutils clonegroup <group_name>

    .. note:: This will clone each repo into its specific folder, depending on the amount of projects this command might take a while. Additionally, a 2 seconds sleep time had to be added in between clones in order not to be blocked by Gitlab API.

Fork & Merge walk-through
-------------------------

1. Fork and clone a repository:

    $ gitutils fork <group_name>/<repository_name>

2. Change the current working directory to your local project cd <repository_name>. Do the changes and/or development necessary.

3. Stage your changes to commit by adding them:

    $ git add .

4. Commit your changes with a descriptive commit_message:

    $ git commit -m <commit_message>

5. Push changes to the forked repository:

    $ git push

6. Once you're ready to create the merge request, fetch and merge changes from original repository:

    $ git fetch upstream

7. Fetch the branches and their respective commits from the upstream repository.

    $ git merge upstream/master

    .. note:: This brings your fork's 'master' branch into sync with the upstream repository without losing your changes. You might have to deal with existing conflicts between your changes and the original repo changes. Decide if you want to keep only your branch's changes, keep only the other branch's changes, or make a brand new change, which may incorporate changes from both branches. If this is the case, go back to step 4 after solving the merge conflicts (add, commit and push the resolved merge conflicts files).

8. Finally, create a merge request:

    $ gitutils merge -p <group_name>/<repository_name> -t <title> -d <description>

    .. note:: if you are located on the repository folder, simply:

        $ gitutils merge  -t <title> -d <description>
