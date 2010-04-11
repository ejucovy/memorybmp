import os

from sven.bzr import BzrAccess
def write(dir, x, y, value):
    fs = BzrAccess(dir)
    bit_uri = os.path.join("bits", "%s-%s" % (y, x))
    fs.write(bit_uri, value)

if __name__ == "__main__":
    import sys
    write(*sys.argv[1:])
    from read import render
    render(sys.argv[1])
