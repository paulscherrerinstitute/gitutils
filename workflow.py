import gitlab

def main():
    gitlab.print_response = True
    # print(gitlab.get_projects())
    group_id = gitlab.get_group_id('launcher_config')
    print(group_id)
    projects = gitlab.get_group_projects(group_id)

    for project in projects:
        if project['name'] == 'sf_machine_launcher':
            project_id = project['id']
            break

    print(project_id)
    gitlab.fork_project(project_id)

if __name__ == '__main__':
    main()
