import os

remote_name = 'gitlab'


def clone_repository(url, mirror=True):
    mirror_option = ''
    if mirror:
        mirror_option = '--mirror'
    os.system('git clone %s %s' % (url, mirror_option))


def push_repository(remote_url):

    # Set remote url - (assuming repository was already cloned from a remote)
    os.system('git remote add %s %s' % (remote_name, remote_url))

    # Push all branches
    os.system('git push %s --all' % remote_name)
    # Push all tags
    os.system('git push %s --tags' % remote_name)


if __name__ == '__main__':
    current_dir = os.getcwd()
    os.mkdir('tmp')
    os.chdir('tmp')
    clone_repository('ssh://git@github.psi.ch:7999/cor/dropit.psi.ch.git')

    push_repository('git@git.psi.ch:git-tools/stash-migration.git')
    os.chdir(current_dir)
