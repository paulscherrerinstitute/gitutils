# Changelog
All notable changes to gitutils projecct will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.4.6] - 2019-08-26
### Added
- GitutilsError exception class. It hides stack when reaching an exception and prints the error in a friendly way.
- Gitutils can't be executed from a git-controlled folder.
### Changed
- Show help when no argument is provided (previously, the token file was generated).
- Project argument when forking is now a positional argument.
- Title for merge request is not required. A default title will be used in case nothing is provided by the user.
- Usage of a generic endpoint. (set/get_endpoint function)
- Name of the file to save the token was changed to ```/.gitutils_token```
- Bugfix: problem using tuple to print exception error.

## [1.4.2] - 2019-08-22
### Added
- Unit Tests.
### Changed
- Improved readme instructions.
- Usage of a generic endpoint function get_endpoint(), which deals with a possible generic endpoint provided by the user as argument.
- Python3 correct way of importing modules.
- Bugfix: preventing the usage of an empty token from empty but existing file.
### Removed
- Installation script makes no sense when using a conda environment and installing it.
- Fixed endpoint.


## [1.4.1] - 2019-08-20
### Added
- Possibility to clean existing forks and have a fresh fork from a reference repository.
- Oauth2 authentication token is now saved on a file for future usage. If not valid, it requests again.
### Changed
- Improved readme instructions.
- Not request username/login at every interation.
- Removed pull and push commands.
- Removal of local directory when '-c' is used.
- Bugfix: when working on an existing fork, group name and project name can now be fetched from git repository in the folder where gitutils is utilized or directly indicated by the user.

## [1.4.0] - 2019-08-19
### Added
- First release of the gitutils library.
- Pull, push, fork and merge functions using oath2 authentication.
- Usage of Python-Gitlab library instead of gitlab api.
- Usage of a const.py file with all constant values necessary.












