# Overview
GITUTILS is a tool to facilitate the server-side operations when developing software that uses git repositories. It allows users to create forks and merge requests directly from the command line interface in a straighforward.

### GIT Credentials
GITUTILS authenticates on the git server using the OAuth2 protocol. If the token is non existant or not valid, gitutils will request username and password and store the token in a file located on the user's home directory called `.gitlab_token`. The user will not need to supply username and password until the expiration time of the saved token.

### Development

The package can be build via

```bash
conda build conda-recipe
```
Remember to increase the package version before the build (inside `setup.py` and `conda-recipe/meta.yaml`)

As the package is mainly used on Linux the package should be build on gfalcd.psi.ch. There, before building you have to source the right anaconda environment by executing the command

```bash
source /opt/gfa/python
```

After building, the package should be uploaded to anaconda.org via the command displayed at the end of the build process.

#### Built With

* [Python-Gitlab](https://python-gitlab.readthedocs.io/en/stable/index.html) - A library for command-line interaction with gitlab servers.

## Installation
The package has to be installed as root on gfalcd.psi.ch .

```
source /opt/gfa/python
conda install -c paulscherrerinstitute gitutils
```

As this will change the global Python distribution, make sure that only the gitutils package gets updated.


## Usage

```
usage: gitutils [-h] [-e ENDPOINT] {fork, merge} ...

GITUTILS utility

positional arguments:
  configuration (e.g. launcher, archiver)

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

If not specified otherwise the default endpoint is https://git.psi.ch.

### Turn gitutils into a command

To make gitutils available as a command, turn it into an executable and add it to your "~/.bash_profile", by executing the gitutils_install.sh script, as in:

```bash
./gitutils_install.sh
```

To do it mannually, do the following:

```bash
cp ./gitutils/gitutils.py ./gitutils/gitutils
chmod +x ./gitutils/gitutils
echo $"export PATH=\$PATH:$(pwd)/gitutils" >> ~/.bash_profile
source ~/.bash_profile
```

# Examples

Currently, there are two commands available: *fork* and *merge request*.

### FORK

To fork and clone into a repository, use the following command:
```bash
gitutils fork -p <group_name>/<repository_name>
```

To fork and **not** clone, add the directive `-n` at the end of the previous command, as in:
```bash
gitutils fork -p <group_name>/<repository_name> -n
```

### MERGE REQUEST

To create a merge request for a repository, use the following command while on a git repository folder:
```bash
gitutils merge -t <title> -d <description>
```

GITUTILS will assume the command is being executed on the git repository folder. Alternatively, one can use the directive `-p` to indicate directly which project should be merged, as in:

```bash
gitutils merge -p <group_name>/<repository_name> -t <title> -d <description>
```

Please note that the title directive is required.

## Tests

Unit tests are available on the folder `tests`. To run the unit tests, navigate into `tests` and use the command:

```bash
$python -m unittest gitutils_test.py
```

# Contact
Questions or problems: Leonardo Hax Damiani - leonardo.hax@psi.ch
