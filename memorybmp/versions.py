from sven.bzr import BzrAccess
import os

def show_versions(dir, x, y):
    fs = BzrAccess(dir)
    bit_uri = os.path.join("bits", "%s-%s" % (y, x))
    return fs.revisions(bit_uri)

import sys
if __name__ == '__main__':
    print show_versions(*sys.argv[1:])
