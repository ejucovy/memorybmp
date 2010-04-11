from PIL import Image
import os

def fromfile(orig, dest):
    x = Image.open(orig)
    pixels = x.getdata()
    w, h = x.size
    os.mkdir(dest)
    about = os.path.join(dest, "about")
    fp = open(about, 'w')
    fp.write("%s,%s" % (w,h))
    fp.close()
    bits = os.path.join(dest, "bits")
    os.mkdir(bits)
    index = 0
    for j in range(h):
        for i in range(w):
            color = pixels[index]
            color = "rgb(%s,%s,%s)" % color
            bit = open(os.path.join(dest, "bits", "%s-%s" % (j,i)), 'w')
            bit.write(color)
            bit.close()
            index += 1

if __name__ == "__main__":
    import sys
    file = sys.argv[1]
    todir = sys.argv[2]
    fromfile(file, todir)
    from read import render
    render(sys.argv[2])

