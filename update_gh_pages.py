import os
from collections import namedtuple

Addr = namedtuple('Addr', ['branch', 'path'])

FROM = Addr('master', 'README.md')
TO = Addr('gh-pages', 'index.md')

def checkout(branch):
    os.system('git checkout {}'.format(branch))


checkout(TO.branch)
