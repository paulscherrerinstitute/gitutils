Welcome to Gitutils documentation
=======================================

.. meta::
   :description lang=en: Gitutils is a tool to facilitate the server-side operations when developing software that uses git repositories. 


Gitutils is a tool to facilitate the server-side operations when developing software that uses git repositories.

Gitutils functionalities:

      * **addldap**             Add a ldap group user to a group.
      * **clonegroup**          Clones all existing projects within a group.
      * **creategroups**        Create a new group (or multiple).
      * **createprojects**      Create a new project (or multiple) inside the specified group.
      * **find**                General search inside all the groups/projects.
      * **fork**                Creates a fork from the repository. Doing a fork is strongly recommended to freely experiment your changes and/or development in a safe working space without affecting the original project.
      * **login**               Fetches the gitlab token (saved in ~/.gitutils_token).
      * **merge**               Creates a request to merge the defined fork to the original repository. 
      * **setrole**             Sets the role for a specific user on a specific group or project (or multiple)

It is developed using `python`_ on an open-source project (`github repository`_), distributed using anaconda via the Paul Scherrer Institute channel (`anaconda channel`_) and documented here using readthedocs.
Gitutils authenticates on the git server using the OAuth2 protocol. If the token is non-existent or not valid, gitutils will request username and password and store the token in a file located on the user's home directory called ``.gitutils_token``. The user will not be requested for username nor password until the saved token is not valid anymore.

.. _python : https://www.python.org/
.. _github repository : https://git.psi.ch/controls_highlevel_applications/gitutils
.. _anaconda channel : https://anaconda.org/paulscherrerinstitute/gitutils

Contents:

.. toctree::
    :glob:
    :maxdepth: 3

    installation
    getting-started
    usage
    development
    faq
    changelog
    contact
