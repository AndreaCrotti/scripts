#!/usr/bin/env python2.7
from subprocess import Popen, PIPE

KEEP_BRANCHES = ['release_13022014', 'master', 'dev', 'selenium_tests', 'staging']


def all_branches():
    cmd = Popen('git branch -a', stdout=PIPE, stderr=PIPE, shell=True)
    out, err = cmd.communicate()
    return [x.strip() for x in out.split('\n')]


def delete_remote_branch(branch):
    cmd = 'git push origin :{}'.format(branch)
    print("Calling {}".format(cmd))
    cmd = Popen(cmd, shell=True)
    out, err = cmd.communicate()
    print(out, err)


if __name__ == '__main__':
    for branch in all_branches():
        if branch.startswith('remotes/origin/'):
            br_name = branch[len('remotes/origin/'):]
            if br_name not in KEEP_BRANCHES:
                delete_remote_branch(br_name)
            else:
                print("Keeping branch {}".format(br_name))
