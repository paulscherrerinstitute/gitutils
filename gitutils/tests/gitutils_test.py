#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
import sys
import os
from gitutils import gitlab_utils
from gitutils import const


class TestGitlabUtils(unittest.TestCase):

    global gl

    def test_authenticate(self):
        """
        Test the authentication.
        """

        global gl
        gitlab_utils.set_endpoint(const.ENDPOINT)
        gitlab_utils.authenticate()
        gl = gitlab_utils.get_gl()
        if os.path.isfile(os.path.expanduser('~') + const.GIT_TOKEN_FILE):
            with open(os.path.expanduser('~') + const.GIT_TOKEN_FILE, 'r'
                      ) as tfile:
                private_token = tfile.read().replace('\n', '')
        self.assertEqual(private_token, gl.oauth_token)

    def test_get_username(self):
        """
        Test the username
        """
        global gl
        self.assertEqual(gl.user.name, gitlab_utils.get_username())

    def test_get_groups(self):
        """
        Test get_groups
        """

        list_of_groups = gitlab_utils.get_groups()
        self.assertTrue(list_of_groups)

    def test_get_projects(self):
        """
        Test get_projects
        """

        list_of_projects = gitlab_utils.get_projects()
        self.assertTrue(list_of_projects)

    def test_get_project_web_url(self):
        """
        Test get_project_web_url
        """

        web_url = gitlab_utils.get_project_web_url('app_config')
        default = 'https://git.psi.ch/controls_highlevel_applications/app_config'
        self.assertEqual(web_url, default)

    def test_checkKey(self):
        """
        Test checkKey
        """

        dict_projects = gitlab_utils.get_owned_projects()
        if len(dict_projects) >= 1:
            self.assertEqual(gitlab_utils.checkKey(dict_projects[0],
                             'name'), True)
            self.assertEqual(gitlab_utils.checkKey(dict_projects[0],
                             'notKey'), False)

    def test_get_project_group(self):
        """
        Test get_project_group
        """

        group = gitlab_utils.get_project_group('app_config', False, False)
        self.assertEqual(group, 'controls_highlevel_applications')

    def test_get_group_id(self):
        """
        Test get_group_id
        """

        group_id = \
            gitlab_utils.get_group_id('controls_highlevel_applications')
        self.assertEqual(group_id, 84)

    def test_get_project_url(self):
        """
        Test get_project_url
        """

        http_url_to_repo = gitlab_utils.get_project_url(84, 'app_config')
        default = 'https://git.psi.ch/controls_highlevel_applications/app_config.git'
        self.assertEqual(http_url_to_repo, default)

    def test_get_project_id(self):
        """
        Test get_project_id
        """

        project_id = \
            gitlab_utils.get_project_id('controls_highlevel_applications',
                                        'app_config')
        self.assertEqual(project_id, 941)

    def test_get_repo_group_names_1(self):
        """
        Test get_repo_group_names with the full path
        """
        config = 'https://git.psi.ch/controls_highlevel_applications/app_config'
        (repo_name, group_name, project_id, valid) = \
            gitlab_utils.get_repo_group_names(config, False)
        self.assertEqual(repo_name, 'app_config')
        self.assertEqual(group_name, 'controls_highlevel_applications')
        self.assertEqual(project_id, 941)

    def test_get_repo_group_names_2(self):
        """
        Test get_repo_group_names with the group/project path
        """
        config = 'controls_highlevel_applications/app_config'
        (repo_name, group_name, project_id, valid) = \
            gitlab_utils.get_repo_group_names(config, False)
        self.assertEqual(repo_name, 'app_config')
        self.assertEqual(group_name, 'controls_highlevel_applications')
        self.assertEqual(project_id, 941)

    def test_get_repo_group_names_3(self):
        """
        Test get_repo_group_names with the project path
        """

        (repo_name, group_name, project_id, valid) = \
            gitlab_utils.get_repo_group_names('app_config', False)
        self.assertEqual(repo_name, 'app_config')
        self.assertEqual(group_name, 'controls_highlevel_applications')
        self.assertEqual(project_id, 941)

    def test_get_group_projects(self):
        """
        Test get_group_projects
        """
        group_name = 'controls_highlevel_applications'
        projects = \
            gitlab_utils.get_group_projects(group_name)
        if len(projects) >= 1:
            project_name = projects[0]['name']
            group_name = gitlab_utils.get_project_group(project_name, False, False)
            self.assertEqual(group_name,
                             'controls_highlevel_applications')

    def test_get_owned_projects(self):
        """
        Test get_owned_projects
        """

        owned_projects = gitlab_utils.get_owned_projects()
        if len(owned_projects) >= 1:
            project_id = owned_projects[0]['id']
            project = gl.projects.get(project_id)
            self.assertEqual(gitlab_utils.get_username(),
                             project.attributes['owner']['username'])


if __name__ == '__main__':
    unittest.main()
