from sven.bzr import BzrAccess
import os
from versions import show_versions
import subprocess

def rewind(dir, x, y, steps_back):
    versions = show_versions(dir, x, y)
    steps_back = int(steps_back)
    version = versions[steps_back]
    bitfile = os.path.join(dir, "bits", "%s-%s" % (y, x))
    subprocess.call(['bzr', 'revert', '-r%s' % version, bitfile])

import sys
if __name__ == '__main__':
    rewind(*sys.argv[1:])
