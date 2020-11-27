[![Conda](https://img.shields.io/conda/pn/paulscherrerinstitute/gitutils?color=success)](https://anaconda.org/paulscherrerinstitute/gitutils) [![Documentation Status](https://readthedocs.org/projects/gitutils/badge/?version=latest)](https://gitutils.readthedocs.io/en/latest) [![GitHub](https://img.shields.io/github/license/paulscherrerinstitute/gitutils)](https://github.com/paulscherrerinstitute/gitutils/blob/master/LICENSE) ![GitHub Release Date](https://img.shields.io/github/release-date/paulscherrerinstitute/gitutils) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/f62b70884d5d4dd9896be7ba7d637626)](https://www.codacy.com/manual/lhdamiani/gitutils?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=paulscherrerinstitute/gitutils&amp;utm_campaign=Badge_Grade)![conda_publish](https://github.com/paulscherrerinstitute/gitutils/workflows/conda_publish/badge.svg)![Lint](https://github.com/paulscherrerinstitute/gitutils/workflows/Lint/badge.svg)


# Overview
Gitutils is a python tool to facilitate the server-side operations when developing software that uses git repositories. It allows users to create forks and merge requests directly from the command line interface.

[Detailed readthedocs documentation](https://gitutils.readthedocs.io/en/latest/index.html)

Please note that Gitutils depends on the Oauth2 authentication via the GITLAB EE API v4. Because of this, gitlab accounts with the two-factor authentication (2FA) activated are not allowed to use the Oauth2 authentication and,therefore, the gitutils token can't be generated.
> for more information: https://docs.gitlab.com/ee/user/profile/account/two_factor_authentication.html and https://docs.gitlab.com/ee/api/oauth2.html#resource-owner-password-credentials-flow

# Usage

## gitutils
```bash
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
```

> To see the gitutils help message use: ```> gitutils -h```. If not specified otherwise the default endpoint is ```https://git.psi.ch```.

## clonegroup
```bash
usage: gitutils.py clonegroup [-h] group

positional arguments:
  group       Group name

optional arguments:
  -h, --help  show this help message and exit
```

> To see the clonegroup help message use: ```> gitutils clonegroup -h```


## creategroups

```bash
usage: gitutils.py creategroups [-h] name [name ...]

positional arguments:
  name        Group name or multiple (if multiple groups should be created).

optional arguments:
  -h, --help  show this help message and exit
```

## createprojects
```bash
usage: gitutils.py createprojects [-h] group name [name ...]

positional arguments:
  group       Group name
  name        Name of the new project (or multiple separated with spaces).

optional arguments:
  -h, --help  show this help message and exit
```

## find
```bash
usage: gitutils find [-h] term

positional arguments:
  term        Term to search.

optional arguments:
  -h, --help  show this help message and exit
```

> To see the clonegroup help message use: ```> gitutils find -h```

## fork
```bash
usage: gitutils fork [-h] [-n] [-c] [-g GROUP] project

positional arguments:
  project               (REQUIRED) Indicates the project to be forked. It can be of three different formats:
                        - https://git.psi.ch/<group_name>/<project_name> : The user provides
                           the direct http to the git repository.
                        - <group_name>/<project_name> : The user provides a combination of
                           group_name and project_name divided by "/".
                        - <project_name> : The user provides the name of the project name.
                           Gitutils will fetch the name of the group (keep in mind, that this may
                           cause ambiguity problems).

optional arguments:
  -h, --help            show this help message and exit
  -n, --no_clone        Indicates that the forked project will not be cloned after forking. A fork
                        will be created on the server-side and no clone nor upstream will be
                        generated on the local git server.
  -c, --clean           Indicates to delete any existing fork project under your personal group.
                        This might be necessary to fork and clone into a clean copy of the original
                        repository. The desired forked project must not be a pre-existing forked
                        project under your personal projects.
  -g GROUP, --group GROUP
                         Indicates the group that the fork is going to be created. The default is the username.
```

> To see the fork help message use: ```> gitutils fork -h```

## merge

```bash
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
                        - https://git.psi.ch/<group_name>/<project_name> : The user provides the direct
                              http to the git repository.
                        - <group_name>/<project_name> : The user provides a combination of group_name and
                              project_name divided by "/".
                        - <project_name> : The user provides the name of the project name. Gitutils will
                              fetch the name of the group (keep in mind, that this may cause ambiguity
                              problems).
  -d DESCRIPTION, --description DESCRIPTION
                        The description of the merge request that is going to be created.
```

> To see the merge help message use: ```> gitutils merge -h```

## setrole

```bash
usage: gitutils.py setrole [-h] [-p] role username group [group ...]

positional arguments:
  role           The role defines the permissions. Options: guest, reporter, dev, maintainer, owner
  username       Username that will be given the role.
  group          Group in which the user will be given such role.

optional arguments:
  -h, --help     show this help message and exit
  -p, --project  If indicated, the setrole gives the access on a project level (and not on the default group level).
```

> To see the merge help message use: ```> gitutils setrole -h```

## Examples

### LOGIN

1. The login command creates the token file and stores it for further usage. 
    - To fetch the token and create/update, use the following command:

        ```bash
        > gitutils login
        ```
> After the username and password are provided the token is fetched and saved on the local home directory in ~/.gitutils_token. As a verification, a list of owned projects will be fetched to validate the token.

### CLONEGROUP

1. The clonegroup command clones all the existing projects from a specified group.
    - To clone all projects of ```group_name```:

        ```bash
        > gitutils clonegroup <group_name>
        ```
        
    > This will clone each repo into its specific folder, depending on the amount of projects this command might take a while. Additionally, a 2 seconds sleep time had to be added in between clones in order not to be blocked by Gitlab API.

### FIND

1. The find command will do a general search for all projects and groups.
    - To search for ```term```:

        ```bash
        > gitutils find <term>
        ```
        > Keep in mind that depending the number of groups and projects, this task can take some minutes...

    - The output will display the group and the enumerated matching cases according to this example:

        ```bash
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
        ```


### FORK

#### Gitutils fork walk-through

1. Define a project to fork and issue the command. Once a repository is forked, it also creates a local clone and an upstream link to the reference repository. Arguments: ___-n___, ___-c___ and project. Examples:
    - To fork and clone into a repository, use the following command:

        ```bash
        > gitutils fork <group_name>/<repository_name>
        ```

    - To fork and not clone, add the directive ___-n___ :

        ```bash
        > gitutils fork -n <group_name>/<repository_name>
        ```

    - To delete existing fork and create a clean fork of a repository, use the following command:

        ```bash
        > gitutils fork -c <group_name>/<repository_name>
        ```
    - To fork (using the full path), clean existing fork and not clone an existing repository:
    
        ```bash
        > gitutils fork -n -c https://git.psi.ch/<group_name>/<repository_name>
        ```

    - To fork into a different group, use the ___-g___ to indicate which group:
    
        ```bash
        > gitutils fork -g <destination_group> https://git.psi.ch/<group_name>/<repository_name>
        ```

2. Implement the changes/development necessary on the forked repository.

3. Add all changes, commit and push the changes to your forked repository.

    ```bash
    > git add .
    > git commit -m <commit_message>
    > git push
    ```

> Remark: When a successful fork happens, it already creates the upstream link. This is done automatically. Therefore, to synchronize your fork with the current state of the original repository and deal with possible merge conflicts, do the following:

    ```bash
    > git fetch upstream
    > git merge upstream/master
    ```

> Tip: To update your current fork state, use the fork command with -c directive. It will delete your personal fork and pull the latest state of the original project.

### MERGE REQUEST

#### Gitutils merge walk-through

1. Once all the necessary changes/development have been commited and pushed to a forked repository.

2. Navigate to the home folder of your forked repository (where the ```/.git``` folder is). Issue the command to merge. Arguments:___-t___, ___-d___, ___-p___.

    - To create a merge request for a repository, use the following command while on a git repository folder:

        ```bash
        > gitutils merge -t <title> -d <description>
        ```
    - To create a merge request for a repository by using the argument ```-p``` to indicate the project:

        ```bash
        > gitutils merge -p <group_name>/<repository_name> -t <title> -d <description>
        ```
    - To create a merge request indicating the full-path to the repository and without giving a description:

        ```bash
        > gitutils merge -p https://git.psi.ch/<group_name>/<repository_name> -t <title>
        ```

> If ```-p``` is not indicated, ```gitutils``` fetches the group and project from the ```.git/config``` file (it assumes that the command is executed within the root directory of the git repository). Alternatively, one can use the directive `-p` to indicate directly which project should be merged.

> If title and description are not provided, gitutils uses a default title and description indicating the user who is creating the merge request.

### Full walk-through example

 1. Fork and clone a repository:
    ```bash
    > gitutils fork <group_name>/<repository_name>
    ```

 2. Change the current working directory to your local project ```cd <repository_name>```.

 3. Do the changes and/or development necessary.

 4. Stage your changes to commit by adding them:

    ```bash
    > git add .
    ```

 5. Commit your changes with a descriptive commit_message:

    ```bash
    > git commit -m <commit_message>
    ```

 6. Push changes to the forked repository:
    ```bash
    > git push
    ```

 7. Once you're ready to create the merge request, fetch and merge changes from original repository:
    ```bash
    > git fetch upstream
    ```

    > Fetch the branches and their respective commits from the upstream repository.

    ```bash
    > git merge upstream/master
    ```
    > This brings your fork's 'master' branch into sync with the upstream repository without losing your changes.

    > You might have to deal with existing conflicts between your changes and the original repo changes. Decide if you want to keep only your branch's changes, keep only the other branch's changes, or make a brand new change, which may incorporate changes from both branches. If this is the case, go back to step 4 after solving the merge conflicts (add, commit and push the resolved merge conflicts files).

 8. Finally, create a merge request:

    ```bash
    > gitutils merge -p <group_name>/<repository_name> -t <title> -d <description>
    ```
    if you are located on the repository folder, simply:

    ```bash
    > gitutils merge  -t <title> -d <description>
    ```

# Development & extra details

Checkout the project:
```bash
> git clone git@git.psi.ch:controls_highlevel_applications/gitutils.git
```

## Tests

(Preliminary) Unit tests are available on the folder `tests`. To run the unit tests, use the command:

```bash
> python -m unittest gitutils/tests/gitutils_test.py
```

## Building the conda package

First, login into ```gfa-lc6-64```, source the right anaconda environment by executing the command:

```bash
> source /opt/gfa/python
```

After that, clone into the repository or pull the latest changes (if you've already cloned it before). The package can be build via

```bash
> conda build conda-recipe
```

Remember to increase the package version before the build (inside `setup.py` and `conda-recipe/meta.yaml`)

After building, the package should be uploaded to anaconda.org via the command displayed at the end of the build process (similar to the shown below).

```bash
> anaconda -t <PERSONAL_CONDA_TOKEN> upload <PATH_TO_THE_PACKAGE>
```

If you need to build for different python versions, use the command (where X.X is the specific needed version of python):

```bash
> conda build conda-recipe --python=X.X
```

## Installation
The package has to be installed as root on gfalcd.psi.ch .

```
> source /opt/gfa/python
> conda install -c paulscherrerinstitute gitutils
```

As this will change the global Python distribution, make sure that only the gitutils package gets updated.


## Built With

* [Python-Gitlab](https://python-gitlab.readthedocs.io/en/stable/index.html) - A library for command-line interaction with gitlab servers.

## Official documentation

The readthedocs documentation is generated based on the files inside the ```docs``` folder in the github repository. 

[Detailed readthedocs documentation](https://gitutils.readthedocs.io/en/latest/index.html)

## GIT Credentials
Gitutils authenticates on the git server using the OAuth2 protocol. If the token is non existant or not valid, gitutils will request username and password and store the token in a file located on the user's home directory (`~/.gitutils_token`). The user will not be requested for username nor password until the saved token is not valid anymore.

# Contact / Questions
Questions or problems: Leonardo Hax Damiani - leonardo.hax@psi.ch

