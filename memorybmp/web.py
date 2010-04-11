from webob import Request, Response, exc
from read import render
from rewind import rewind
from versions import show_versions
import subprocess

def redirect(req, perm=False):
    qstr = qs(req.GET)
    path = req.script_name + req.path_info + "?" + qstr
    if perm:
        return exc.HTTPMovedPermanently(location=path)
    return exc.HTTPTemporaryRedirect(location=path)

def qs(dict):
    qs = ''
    for key, value in dict.items():
        if value == '':
            qs += '%s&' % key
        else:
            qs += '%s=%s&' % (key, value)
    qs = qs.rstrip('&')
    return qs

def app_factory(*args, **kw):
    return WebApp()

class WebApp(object):
    def __call__(self, environ, start_response):
        req = Request(environ)
        filename = req.GET.get('file')
        if not filename: return Response()(environ, start_response)
        partial = req.GET.get('async')
        if partial: del req.GET['async']
        del req.GET['file']
        if not req.GET:
            subprocess.call(['bzr', 'revert', filename])
            return self.render(filename, partial)(environ, start_response)
        if 'logfor' in req.GET:
            x, y = req.GET['logfor'].split('-')
            return self.show_versions(filename, x, y)(environ, start_response)
        for item in req.GET:
            x, y = item.split(':')
            dt = req.GET[item]
            try:
                rewind(filename, x, y, dt)
            except IndexError:
                del req.GET[item]
                req.GET['file'] = filename
                q = qs(req.GET)
                if partial: return exc.HTTPBadRequest()(environ, start_response)
                return redirect(req)(environ, start_response)
        return self.render(filename, partial)(environ, start_response)

    def show_versions(self, filename, x, y):
        res = Response(content_type="application/json")
        res.body = str(show_versions(filename, x, y))
        return res

    def render(self, filename, partial=None):
        res = Response()
        render(filename, res.body_file, partial or False)
        subprocess.call(['bzr', 'revert', filename])
        return res

    
