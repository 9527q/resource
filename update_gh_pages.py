# -*- coding:utf-8 -*-
import os
from collections import namedtuple

Addr = namedtuple('Addr', ['branch', 'file'])

FROM = Addr('master', 'README.md')
TO = Addr('gh-pages', 'index.md')
TAG = '资源'


class Git:
    def _run(self, cmd):
        return os.popen(cmd)

    def checkout(self, branch):
        return self._run('git checkout {}'.format(branch))

    def add(self, *files):
        return self._run('git add {}'.format(', '.join(files)))

    def commit(self, msg):
        return self._run('git commit -m {}'.format(msg))


git = Git()
git.checkout(FROM.branch)
with open(FROM.file) as f:
    read_content = f.read()
    i = read_content.index(TAG)
    read_content = read_content[i:]

git.checkout(TO.branch)
with open(TO.file, 'r+') as f:
    write_content = f.read()
    i = write_content.index(TAG)
    write_content = write_content[:i] + read_content
    f.seek(0, 0)
    f.write(write_content)

git.add(TO.file)
git.commit('update from master')