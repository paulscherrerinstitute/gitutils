Changelog
=========

All notable changes to gitutils projecct will be documented in this
file.

[1.0.3] - 2019-12-06
Added
~~~~~

-  New parameter on the fork command. -g indicates the group/namespace that the fork will be created. Permissions to do operations in different groups are needed.

Changed
~~~~~~~

-  Username and password are now appropriately url encoded by using urllib.parse.quote.
-  Python-Gitlab method returns only 20 itens per search. Fixed by additions parameter all=True in all retrieval of projects or groups.

[1.0.1] - 2019-09-13
--------------------

Added
~~~~~

-  First release of the gitutils library.
-  Gitutils implements fork and merge (server-side) functions using oauth2 authentication.
-  Usage of Python-Gitlab library instead of gitlab api.
-  Gitutils recovers from an invalid token (fetched from .gitutils_token) by requesting username and password again.
-  Gitutils offers a readthedocs documentation.
-  gitutils argument '-e' to indicate a different repository endpoint.
-  fork argument 'project' is a positional required argument.
-  fork argument '-c' to clean existing forks or local folders.
-  fork argument '-n' to not clone into forked repository.
-  Allow merge argumentless possibility when executing from within the repository's folder.
-  Merge allows project indication without the usage of the '-p' flag. Project can also be a positional argument.
-  When forking a project that is exists in multiple groups, a list of the groups is displayed.
-  Unit tests.
-  Oauth2 token saved on user's home directory file '.gitutils_token'.
-  Merge allows possibility to define project, title and description. If merge command is executed inside the forked repository's folder, gitutils detects it and does not need the '-p' argument to indicate the project.


.. note:: The format is based on `Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`__, and this project adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`__.