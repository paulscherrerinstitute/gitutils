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
