import imp
import os
import sys


sys.path.insert(0, os.path.dirname(__file__))

wsgi = imp.load_source('wsgi', 'run.py')
application = wsgi.application

#def appl(environ, start_response):
#    start_response('200 OK', [('Content-Type', 'text/plain')])
#    message = 'Hello, World!\n'
#    version = 'Python %s\n' % sys.version.split()[0]
#    response = '\n'.join([message, version])
#    return [response.encode()]
