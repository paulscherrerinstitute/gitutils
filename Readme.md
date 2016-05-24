# Overview
Tools to facilitate the configuration change workflows for archiver, launcher, etc..
app_config provides utility functions to fork and clone configuration repositories and to push changes to the fork and create a pull/merge request for the changes.


# Usage

```
usage: app_config [-h] [-b BASEDIR] [-c [CONFIG]]
                  configuration {pull,push,commit} ...

Application configuration management utility

positional arguments:
  configuration (e.g. launcher, archiver)

optional arguments:
  -h, --help            show this help message and exit
  -b BASEDIR, --basedir BASEDIR
                        Base directory to clone configurations to
  -c [CONFIG], --config [CONFIG]
                        Configuration

command:
  valid commands

  {pull,push,commit}    commands
    pull                pull configuration from central server
    push                push configuration from central server
    commit              commit configuration changes to local repository
```

Currently *app_config* supports the _launcher_ and _archiver_ as _configuration_ parameter by default.
These 2 configurations will checkout the SwissFEL machine launcher and archiver configuration to a local working directory.
If not specified otherwise the configuration will end up in `~/app_config/*`.

# Development

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

# Installation
The package has to be installed as root on gfalcd.psi.ch .

```
source /opt/gfa/python
conda install -c paulscherrerinstitute app_config
```

As this will change the global Python distribution, make sure that only the app_config package gets updated.
