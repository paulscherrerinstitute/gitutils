#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from unittest import TestCase, main as unittest_main
import os
import shutil
import argparse
import sys
import time
from gitutils import gitutils_parser
from gitutils import gitlab_utils
from gitutils import gitutils
from gitutils import const

class TestGitutils(TestCase):
    group_name = 'gitutils_unittest_group'
    project_1 = 'project_test_unittest1'
    project_2 = 'project_test_unittest2'
    user_ldap = 'unx-sls_bd'
    user_ldap_member = 'ebner'
    user_role = 'guest'
    group_fork = 'controls_highlevel_applications'
    project_fork = 'iocutils'
    merge_request_title = 'title for merge request unit test'
    merge_request_description = 'description for merge request unit test'
    merge_request_description_ref = 'The configuration was changed by hax_l. User description: description for merge request unit test'
    
    def step0(self):
        pass

    ################
    # Create Group #
    ################
    def step1(self):
        # CMD
        sys.argv[1] = 'creategroups'
        # deletes previous args
        del sys.argv[2:]
        # ARG
        sys.argv.append(self.__class__.group_name) 
        # calls main to create group
        gitutils.main()
        # verifies if the group exists
        self.assertTrue(gitlab_utils.group_exists(self.__class__.group_name))
        # gets the id of the newly created group
        self.assertNotEqual(gitlab_utils.get_group_id(self.__class__.group_name),-1)
        time.sleep(2)

    ###################
    # Create Projects #
    ###################
    def step2(self):
        # CMD
        sys.argv[1] = 'createprojects'
        # deletes previous args
        del sys.argv[2:]
        # ARG GROUP
        sys.argv.append(self.__class__.group_name)
        # ARG PROJECTS 
        sys.argv.append(self.__class__.project_1) 
        # ARG PROJECTS 
        sys.argv.append(self.__class__.project_2) 
        # calls main to create projects
        gitutils.main()
        # verifies if the project exists
        self.assertTrue(gitlab_utils.project_exists(self.__class__.project_1))
        # verifies if the project exists
        self.assertTrue(gitlab_utils.project_exists(self.__class__.project_2))
        # gets the id of the newly created projects
        gitlab_utils.get_project_id(self.__class__.group_name,self.__class__.project_1)
        gitlab_utils.get_project_id(self.__class__.group_name,self.__class__.project_2)
        time.sleep(2)

    ########
    # FORK #
    ########
    def step3(self):
        # CMD
        sys.argv[1] = 'fork'
        # deletes previous args
        del sys.argv[2:]
        # ARG PROJECT
        # not clone
        sys.argv.append('-n')
        sys.argv.append(self.__class__.group_name+'/'+self.__class__.project_2)
        # calls main to fork
        gitutils.main()
        # verifies if forked project exists under personal account
        own_projects = gitlab_utils.get_owned_projects()
        found = any(proj['name'] == self.__class__.project_2 for proj in own_projects)
        self.assertTrue(found)
        time.sleep(2)
        # creates a change
        own_projects = gitlab_utils.get_owned_projects()
        project = None
        for proj in own_projects:
            if proj['name'] ==self.__class__.project_2:
                project = gitlab_utils.get_project(proj['id'])
        self.assertIsNotNone(project)
        # creates the commit
        data = {
            'branch': 'master',
            'commit_message': 'unit test commit',
            'actions': [
                {
                    'action': 'create',
                    'file_path': 'README.rst',
                    'content': "UNIT TEST GITUTILS",
                }
            ]
        }
        project.commits.create(data)
        time.sleep(2)
    
    def step31(self):
        # CMD
        sys.argv[1] = 'fork'
        # deletes previous args
        del sys.argv[2:]
        # ARG PROJECT
        # not clone
        sys.argv.append('-n')
        # removes previous fork and creates a new one
        sys.argv.append('-c')
        sys.argv.append(self.__class__.group_name+'/'+self.__class__.project_2)
        # calls main to fork
        gitutils.main()
        # verifies if forked project exists under personal account
        time.sleep(2)
        own_projects = gitlab_utils.get_owned_projects()
        found = any(proj['name'] == self.__class__.project_2 for proj in own_projects)
        self.assertTrue(found)
        time.sleep(2)
        # creates a change
        own_projects = gitlab_utils.get_owned_projects()
        project = None
        for proj in own_projects:
            if proj['name'] ==self.__class__.project_2:
                project = gitlab_utils.get_project(proj['id'])
        self.assertIsNotNone(project)
        # creates the commit
        data = {
            'branch': 'master',
            'commit_message': 'unit test commit',
            'actions': [
                {
                    'action': 'create',
                    'file_path': 'README_new.rst',
                    'content': "UNIT TEST GITUTILS",
                }
            ]
        }
        project.commits.create(data)
        time.sleep(2)

    def step4(self):
        # CMD
        sys.argv[1] = 'fork'
        # deletes previous args
        del sys.argv[2:]
        # not clone
        sys.argv.append('-n')
        # ARG GROUP
        sys.argv.append('-g')
        # ARG PROJECT
        sys.argv.append(self.__class__.group_name+'/'+self.__class__.project_fork)
        # calls main to fork
        gitutils.main()
        # verifies if forked project exists under group projects
        own_projects = gitlab_utils.get_group_projects(self.__class__.group_name)
        found = any(
            proj['name'] == self.__class__.project_fork for proj in own_projects
        )

        self.assertTrue(found)
        time.sleep(2)

    ###########
    # ADDLDAP #
    ###########
    def step5(self):
        # CMD
        sys.argv[1] = 'addldap'
        # deletes previous args
        del sys.argv[2:]
        # group
        sys.argv.append(self.__class__.group_name)
        # ldap user
        sys.argv.append(self.__class__.user_ldap) 
        # role
        sys.argv.append(self.__class__.user_role) 
        # calls main to fork
        gitutils.main()
        time.sleep(2)
        # gets members of group
        members = gitlab_utils.get_group(gitlab_utils.get_group_id(self.__class__.group_name)).members.all(all=True)
        found = False
        # add ldap adds several users that are member of that ldap group
        # we'll be checking for a member of that ldap group : user_ldap_member
        for i in members:
            if i.attributes['name'] == self.__class__.user_ldap_member:
                found = True
                self.assertEqual(i.attributes['access_level'],gitlab_utils.check_role(self.__class__.user_role))
        self.assertTrue(found)
        time.sleep(2)

    # ################
    # # Clone Group #
    # ################
    def step6(self):
        # CMD
        sys.argv[1] = 'clonegroup'
        # deletes previous args
        del sys.argv[2:]
        # ARG 
        sys.argv.append(str(self.__class__.group_name))
        # calls main to create group
        gitutils.main()
        time.sleep(2)
        # verifies if the project folders exists locally
        self.assertTrue(os.path.exists('./'+self.__class__.project_1))
        self.assertTrue(os.path.exists('./'+self.__class__.project_2))
        self.assertTrue(os.path.exists('./'+self.__class__.project_fork))
        # cleanup 
        try:
            shutil.rmtree('./'+self.__class__.project_1)
            shutil.rmtree('./'+self.__class__.project_2)
            shutil.rmtree('./'+self.__class__.project_fork)
        except:
            print("Problem deleting the cloned project's folders.")
        time.sleep(2)

    #########
    # MERGE #
    #########
    def step7(self):
        # creates the merge request
        sys.argv[1] = 'merge'
        del sys.argv[2:]
        
        sys.argv.append('-p')
        sys.argv.append(self.__class__.project_2)
        # ARG TITLE
        sys.argv.append('-t')
        sys.argv.append(self.__class__.merge_request_title)
        # ARG Description
        sys.argv.append('-d')
        sys.argv.append(self.__class__.merge_request_description)        
        gitutils.main()
        time.sleep(2)
        
        # verifies if the merge request exists on the forked project
        project_id = gitlab_utils.get_project_id(self.__class__.group_name, self.__class__.project_2)
        project = gitlab_utils.get_project(project_id)
        mrs = project.mergerequests.list(state='opened')
        self.assertEqual(mrs[0].attributes['title'],self.__class__.merge_request_title)
        self.assertEqual(mrs[0].attributes['description'],self.__class__.merge_request_description_ref)
        time.sleep(2)

    ###########
    # SETROLE #
    ###########
    def step8(self):
        # creates the merge request
        sys.argv[1] = 'setrole'
        del sys.argv[2:]
        # project setrole
        sys.argv.append('-p')
        # ARG role
        sys.argv.append(self.__class__.user_role)
        # ARG user
        sys.argv.append(self.__class__.user_ldap_member)
        # ARG project
        sys.argv.append(self.__class__.project_2)
        gitutils.main()
        time.sleep(2)
        project_id = gitlab_utils.get_project_id('hax_l',self.__class__.project_2)   
        members = gitlab_utils.get_project(project_id).members.all(all=True)
        for i in members:
            if i.attributes['name'] == self.__class__.user_ldap_member:
                found = True
                self.assertEqual(i.attributes['access_level'],gitlab_utils.check_role(self.__class__.user_role))
        self.assertTrue(found)
        time.sleep(2)
        #################################
        ##### CLEANUP OF TEST STUFF #####
        #################################
        # removal of personal project
        gitlab_utils.remove_project(project_id)
        # removal of test group
        gitlab_utils.remove_group(gitlab_utils.get_group_id(self.__class__.group_name))


    ########
    # FIND #
    ########
    #//TODO verify how to test the output 
    # def test_find_without_f(self):
    #     # CMD
    #     sys.argv[1] = 'find'
    #     del sys.argv[2:]
    #     # ARG
    #     sys.argv.append('S_DI_BAM_S10CB04-DBAMT1.config') 
    #     gitutils.main()

    # def test_find_with_f(self):
    #     # CMD
    #     sys.argv[1] = 'find'
    #     del sys.argv[2:]
    #     # ARG
    #     sys.argv.append('-f')
    #     sys.argv.append('S_DI_BAM_S10CB04-DBAMT1.config') 
    #     gitutils.main()

    def _steps(self):
        for name in dir(self): # dir() result is implicitly sorted
            if name.startswith("step"):
                yield name, getattr(self, name)

    def test_steps(self):
        for name, step in self._steps():
            try:
                step()
            except Exception as e:
                self.fail("{} failed ({}: {})".format(step, type(e), e))

if __name__ == '__main__':
    unittest_main()

    