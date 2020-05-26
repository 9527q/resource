import os
import re
from collections import namedtuple

Addr = namedtuple('Addr', ['branch', 'file'])

FROM = Addr('master', 'README.md')
TO = Addr('gh-pages', 'index.md')
TAG = '</div>'


class Git:
    def _run(self, cmd):
        return os.system(cmd)

    def checkout(self, branch):
        return self._run('git checkout {}'.format(branch))

    def add(self, *files):
        return self._run('git add {}'.format(', '.join(files)))

    def commit(self, msg):
        return self._run('git commit -m "{}"'.format(msg))

    def push(self):
        return self._run('git push')


def place_blank_tag(sentence):
    """给 MD 格式的链接加上 {:target="_blank"} 后缀，方便 GitHub Pages 实现链接在新 Tab 打开"""
    return re.sub('\[.+?\]\(.+?\)(?!{:target="_blank"})', '\g<0>{:target="_blank"}', sentence)


if __name__ == '__main__':
    git = Git()
    git.checkout(FROM.branch)
    with open(FROM.file) as f:
        read_content = f.read()
        i = read_content.index(TAG)
        read_content = place_blank_tag(read_content[i:])

    git.checkout(TO.branch)
    with open(TO.file, 'r+') as f:
        write_content = f.read()
        i = write_content.index(TAG)
        write_content = write_content[:i] + read_content
        f.seek(0, 0)
        f.write(write_content)

    git.add(TO.file)
    git.commit('update from master')
    git.push()
    git.checkout(FROM.branch)
