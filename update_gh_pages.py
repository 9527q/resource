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

    # 读取内容
    git.checkout(FROM.branch)
    with open(FROM.file) as f1:
        f1_content = f1.read()
        i = f1_content.index(TAG)
        f1_content = place_blank_tag(f1_content[i:])

    # 更新到目标文件中
    git.checkout(TO.branch)
    with open(TO.file, 'r+') as f2:
        f2_content = f2.read()
        i = f2_content.index(TAG)
        write_content = f2_content[:i] + f1_content
        f2.seek(0, 0)
        f2.write(write_content)

    # 提交改动（没有改动也无妨）
    git.add(TO.file)
    git.commit('update from master')
    git.push()

    git.checkout(FROM.branch)
