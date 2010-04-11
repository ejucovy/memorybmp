import os

def read(dir):
    about = open(os.path.join(dir, "about"))
    w, h = about.read().strip().split(',')
    w = int(w); h = int(h)
    about.close()

    bits = []
    for j in range(h):
        for i in range(w):
            bitfilename = os.path.join(dir, "bits", "%s-%s" % (j,i))
            bitfile = open(bitfilename)
            bit = bitfile.read().strip()
            bits.append(bit)
            bitfile.close()

    return w, h, bits

import sys
def render(dir, out=sys.stdout, partial=False):
    w, h, bits = read(dir)
    width = w * 10
    height = h * 10
    if not partial:
        print >> out, """<html><head>
<script src="http://turtles.zebra-associates.org/lib/jquery.js" type="text/javascript"></script>
<script src="jquery.jqURL.js" type="text/javascript"></script>
<script src="memorybmp.js" type="text/javascript"></script>
<title>%(dir)s</title></head><body>
  <table style="width: %(width)spx; height: %(height)spx; border-collapse: collapse;">
""" % locals() 

    index = 0
    for i in range(h):
        print >> out, "<tr>"
        for j in range(w):
            bit = bits[index]
            print >> out, """<td style="background-color: %(bit)s;
           padding: 0; "></td>""" % locals()
            index += 1
        print >> out, "</tr>"


    if not partial:
        print >> out, """  </table>
</body></html>"""

if __name__ == "__main__":
    import sys
    render(sys.argv[1])
