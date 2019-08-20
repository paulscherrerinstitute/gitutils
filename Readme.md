# Overview
GITUTILS is a tool to facilitate the server-side operations when developing software that uses git repositories. It allows users to create forks and merge requests directly from the command line interface in a straighforward.

## GIT Credentials
GITUTILS authenticates on the git server using the OAuth2 protocol. If the token is non existant or not valid, gitutils will request username and password and store the token in a file located on the user's home directory called `.gitlab_token`. The user will not need to supply username and password until the expiration time of the saved token.

# Development

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


# Usage

```
usage: gitutils.py [-h] [-e ENDPOINT] {fork,merge} ...

GITUTILS utility

optional arguments:
  -h, --help            show this help message and exit
  -e ENDPOINT, --endpoint ENDPOINT
                        Endpoint of the git server. Default:
                        https://git.psi.ch

command:
  valid commands

  {fork,merge}          commands
    fork                Creates a fork from the repository.
    merge               Creates a request to merge the defined fork to the
                        original repository.
```

> If not specified otherwise the default endpoint is ```https://git.psi.ch```.


## Examples

Currently, there are two commands available: *fork* and *merge request*.

### FORK

#### Gitutils Fork Walk through
1. Define a project to fork and issue the command. Once a repository is forked, it also creates a local clone and an upstream link to the reference repository. Arguments:
  * ___-p___ (___required___): Indicates the project to be forked. It can be of three different formats:
       * "https://git.psi.ch/group_name/project_name" : The user provides the direct http to the git repository.
       * "group_name/project_name" : The user provides a combination of group_name and project_name divided by "/".
       * "project_name" : The user provides the name of the project name. Gitutils will fetch the name of the group (keep in mind, that this may cause ambiguity problems).
  * ___-n___ : Indicates that the forked project *will not* be cloned after forking. A fork will be created on the server-side and no clone nor upstream will be generated on the local git server.
  * ___-c___ : Indicates to delete any existing fork project under your personal group. This might be necessary to fork and clone into a clean copy of the original repository. The desired forked project *must not* be a pre-existing forked project under your personal projects. 
2. Implement the changes/development necessary on the forked repository.
3. Commit changes.
4. Push changes to the forked repository.

> Remarks: When a successful fork happens, it already creates the upstream link. This is done automatically.

#### Fork usage

1. To fork and clone into a repository, use the following command:
  ```bash
  > gitutils fork -p <group_name>/<repository_name>
  ```

2. To fork and **not** clone, add the directive ___-n___ at the end of the previous command, as in:
  ```bash
  > gitutils fork -p <group_name>/<repository_name> -n
  ```

3. To delete existing fork and create a clean fork of a repository, use the following command:
  ```bash
  > gitutils fork -p <group_name>/<repository_name> -c
  ```

4. To fork (using the full path) and not clone an existing repository:
```bash
  > gitutils fork -p https://git.psi.ch/<group_name>/<repository_name> -n -c
  ```


### MERGE REQUEST

#### Gitutils Merge Walk through
1. Once all the necessary changes/development have been commited and pushed to a forked repository.
2. Navigate to the home folder of your forked repository (where the ```/.git``` folder is). Issue the command to merge. Arguments:
  * ___-t___ (___required___): The title of the merge request that is going to be created.
  * ___-d___ : The description of the merge request that is going to be created.
  * ___-p___ : Indicates the project to be forked. It can be of four different formats:
       * "" : The user doesn't provide this argument, the project's group and name will be fetched from the ```/.git``` folder within the path where the gitutils is being called.
       * "https://git.psi.ch/group_name/project_name" : The user provides the direct http to the git repository.
       * "group_name/project_name" : The user provides a combination of group_name and project_name divided by "/".
       * "project_name" : The user provides the name of the project name. Gitutils will fetch the name of the group (keep in mind, that this may cause ambiguity problems).
  


#### Merge usage

Please note that the ___-t___ title directive is required. GITUTILS will assume the command is being executed on the git repository folder. Alternatively, one can use the directive `-p` to indicate directly which project should be merged.

1. To create a merge request for a repository, use the following command while on a git repository folder: 
```bash
  > gitutils merge -t <title> -d <description>
  ```

2. To create a merge request for a repository by using the argument ```-p``` to indicate the project:
```bash
  > gitutils merge -p <group_name>/<repository_name> -t <title> -d <description>
  ```

3. To create a merge request indicating the full-path to the repository and without giving a description:
```bash
  > gitutils merge -p https://git.psi.ch/<group_name>/<repository_name> -t <title>
  ```

# Built With

* [Python-Gitlab](https://python-gitlab.readthedocs.io/en/stable/index.html) - A library for command-line interaction with gitlab servers.

# Contact
Questions or problems: Leonardo Hax Damiani - leonardo.hax@psi.ch
