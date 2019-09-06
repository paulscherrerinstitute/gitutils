# Overview
Gitutils is a tool to facilitate the server-side operations when developing software that uses git repositories. It allows users to create forks and merge requests directly from the command line interface.

A detailed documentation is also found on https://gitutils.readthedocs.io/en/latest/index.html

A gitutils clean sheet can be downloaded here: https://www.cheatography.com/leonardo-hax-damiani/cheat-sheets/gitutils/

# Usage

## gitutils
```
usage: gitutils.py [-h] [-e ENDPOINT] {fork,merge} ...

GITUTILS is a tool to facilitate the server-side operations when developing software that uses git repositories.

optional arguments:
  -h, --help            show this help message and exit
  -e ENDPOINT, --endpoint ENDPOINT
                        Endpoint of the git server. Default: https://git.psi.ch

command:
  valid commands

  {fork,merge}          commands
    fork                Creates a fork from the repository.
    merge               Creates a request to merge the defined fork to the original repository.
```

> To see the gitutils help message use: ```> gitutils -h```. If not specified otherwise the default endpoint is ```https://git.psi.ch```.

## fork
```bash
usage: gitutils fork [-h] [-n] [-c] project

positional arguments:
  project         (REQUIRED) Indicates the project to be forked. It can be of three different formats:
                  - https://git.psi.ch/<group_name>/<project_name> : The user provides
                     the direct http to the git repository.
                  - <group_name>/<project_name> : The user provides a combination of
                     group_name and project_name divided by "//".
                  - <project_name> : The user provides the name of the project name.
                     Gitutils will fetch the name of the group (keep in mind, that this may
                     cause ambiguity problems).

optional arguments:
  -h, --help      show this help message and exit
  -n, --no_clone  Indicates that the forked project will not be cloned after forking. A fork
                  will be created on the server-side and no clone nor upstream will be
                  generated on the local git server.
  -c, --clean     Indicates to delete any existing fork project under your personal group.
                  This might be necessary to fork and clone into a clean copy of the original
                  repository. The desired forked project must not be a pre-existing forked
                  project under your personal projects.
```

> To see the fork help message use: ```> gitutils fork -h```

## merge

```bash
usage: gitutils merge [-h] [-t TITLE] [-p PROJECT] [-d DESCRIPTION]

optional arguments:
  -h, --help            show this help message and exit
  -t TITLE, --title TITLE
                         The title of the merge request that is going to be created.
  -p PROJECT, --project PROJECT
                        Indicates the project to be forked. It can be of four different formats:
                        - "" : The user doesn't provide this argument, the project's group and name
                              will be fetched from the ```/.git``` folder within the path where the
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

## Examples

### FORK

#### Gitutils fork walk-through
1. Define a project to fork and issue the command. Once a repository is forked, it also creates a local clone and an upstream link to the reference repository. Arguments: ___-n___, ___-c___ and project. Examples:
- To fork and clone into a repository, use the following command:

    ```bash
    > gitutils fork <group_name>/<repository_name>
    ```
- To fork and not clone, add the directive ___-n___ at the end of the previous command, as in:

    ```bash
    > gitutils fork <group_name>/<repository_name> -n
    ```
- To delete existing fork and create a clean fork of a repository, use the following command:

    ```bash
    > gitutils fork <group_name>/<repository_name> -c
    ```
- To fork (using the full path), clean existing fork and not clone an existing repository:
 
    ```bash
    > gitutils fork https://git.psi.ch/<group_name>/<repository_name> -n -c
    ```

2. Implement the changes/development necessary on the forked repository.
3. Add all changes, commit and push the changes to your forked repository.

    ```bash
    > git add .
    > git commit -m <commit_message>
    > git push
    ```

    > Remarks: When a successful fork happens, it already creates the upstream link. This is done automatically. Therefore, to synchronize your fork with the current state of the original repository and deal with possible merge conflicts, do the following:

    ```bash
    > git fetch upstream
    > git merge upstream/master
    ```

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
> anaconda -t <PERSONAL_CONDA_TOKEN> upload /afs/psi.ch/user/<PATH_TO_USER>/conda-bld/linux-64/<PACKAGE_NAME>
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

Due to problems in synchronization between [readthedocs](https://readthedocs.org) and a third party hosted git repository (https://git.psi.ch/controls_highlevel_applications/gitutils), the readthedocs documentation is generated based on [this](https://github.com/lhdamiani/gitutils) github repository.

To update the documentation run the script on the home folder of the documentation repository:

```
> python update_doc.py
```

The script is located on the home directory of the github-hosted gitutils repository. Once the changes are incorporated the documentation will be automatically updated.

## GIT Credentials
Gitutils authenticates on the git server using the OAuth2 protocol. If the token is non existant or not valid, gitutils will request username and password and store the token in a file located on the user's home directory (`~/.gitutils_token`). The user will not be requested for username nor password until the saved token is not valid anymore.

# Contact
Questions or problems: Leonardo Hax Damiani - leonardo.hax@psi.ch
