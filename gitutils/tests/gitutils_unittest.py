#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
import os
from gitutils import gitlab_utils
from gitutils import const


class TestGitutilsUnit(unittest.TestCase):

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
        docker = os.environ.get('DOCKER_CONTAINER', False)
        if docker:
            self.assertEqual(gl.user.name, 'root')
        else:
            self.assertEqual(gl.user.name, gitlab_utils.get_username())

    def test_get_groups(self):
        """
        Test get_groups
        """

        list_of_groups = gitlab_utils.get_groups()
        self.assertTrue(len(list_of_groups) > 0)

    def test_roles(self):
        """
        Test roles
        """
        role_guest = gitlab_utils.check_role('guest')
        self.assertEqual(role_guest, 10)
        role_reporter = gitlab_utils.check_role('reporter')
        self.assertEqual(role_reporter, 20)
        role_dev = gitlab_utils.check_role('dev')
        self.assertEqual(role_dev, 30)
        role_maintainer = gitlab_utils.check_role('maintainer')
        self.assertEqual(role_maintainer, 40)
        role_owner = gitlab_utils.check_role('owner')
        self.assertEqual(role_owner, 50)
        


        

    def test_get_project_web_url(self):
        """
        Test get_project_web_url
        """

        web_url = gitlab_utils.get_project_web_url('iocutils')
        default = 'https://git.psi.ch/controls_highlevel_applications/iocutils'
        self.assertEqual(web_url, default)

    def test_checkKey(self):
        """
        Test checkKey
        """

        dict_projects = gitlab_utils.get_owned_projects()
        if len(dict_projects) >= 1:
            self.assertEqual(gitlab_utils.check_key(dict_projects[0],
                             'name'), True)
            self.assertEqual(gitlab_utils.check_key(dict_projects[0],
                             'notKey'), False)

    def test_get_project_group(self):
        """
        Test get_project_group
        """

        group = gitlab_utils.get_project_group('app_config', False, False, True)
        self.assertEqual(group, 'controls_highlevel_applications')

    def test_get_group_id(self):
        """
        Test get_group_id
        """

        group_id = \
            gitlab_utils.get_group_id('controls_highlevel_applications')
        self.assertEqual(group_id, 84)

    def test_get_project_http_url(self):
        """
        Test get_project_url
        """

        http_url_to_repo = gitlab_utils.get_project_http_url('iocutils')
        default = 'https://git.psi.ch/controls_highlevel_applications/iocutils.git'
        self.assertEqual(http_url_to_repo, default)

    def test_get_project_id(self):
        """
        Test get_project_id
        """

        project_id = \
            gitlab_utils.get_project_id('controls_highlevel_applications',
                                        'iocutils')
        self.assertEqual(project_id, 5930)

    def test_get_repo_group_names_1(self):
        """
        Test get_repo_group_names with the full path
        """
        config = 'https://git.psi.ch/controls_highlevel_applications/iocutils'
        (repo_name, group_name, project_id, valid) = \
            gitlab_utils.get_repo_group_names(config, False)
        self.assertEqual(repo_name, 'iocutils')
        self.assertEqual(group_name, 'controls_highlevel_applications')
        self.assertEqual(project_id, 5930)
        self.assertEqual(valid, True)

    def test_get_repo_group_names_2(self):
        """
        Test get_repo_group_names with the group/project path
        """
        config = 'controls_highlevel_applications/iocutils'
        (repo_name, group_name, project_id, valid) = \
            gitlab_utils.get_repo_group_names(config, False)
        self.assertEqual(repo_name, 'iocutils')
        self.assertEqual(group_name, 'controls_highlevel_applications')
        self.assertEqual(project_id, 5930)

    def test_get_repo_group_names_3(self):
        """
        Test get_repo_group_names with the project path
        """

        (repo_name, group_name, project_id, valid) = \
            gitlab_utils.get_repo_group_names('iocutils', False)
        self.assertEqual(repo_name, 'iocutils')
        self.assertEqual(valid, True)
        self.assertEqual(group_name, 'controls_highlevel_applications')
        self.assertEqual(project_id, 5930)

    def test_get_group_projects(self):
        """
        Test get_group_projects
        """
        group_name = 'controls_highlevel_applications'
        projects = \
            gitlab_utils.get_group_projects(group_name)
        if len(projects) >= 1:
            project_name = projects[0]['name']
            group_name = gitlab_utils.get_project_group(project_name, False, False, True)
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
            self.assertEqual('hax_l',
                             project.attributes['namespace']['path'])

    def test_get_all_projects(self):
        """
        Test the retrieval of all projects following a name, overwriting the
        default of 20 projects per list.
        """
        # PROVISORY: A known project with 20+ forks
        project_name = 'sf_daq_sources'
        projects_list = gl.projects.list(search=project_name, all=True)
        self.assertGreater(len(projects_list), 20)

    def test_get_all_groups(self):
        """
        Test the retrieval of all projects, overwriting the
        default of 20 projects per list.
        """
        # PROVISORY: a known group with 20+ projects
        group_name = 'High Performance Detectors Integration'
        group = gl.groups.list(all=True, search=group_name)[0]
        proj_list = group.projects.list(all=True)
        self.assertGreater(len(proj_list), 20)

if __name__ == '__main__':
    unittest.main()
