#!/usr/bin/python

''' Python testing file

'''
import platform

print 'Content-type: text/html\n\n'
print 'Hello from python %s<br>' %platform.python_version()

try:
    import _mysql
    print 'Got MySql, woo!'
except Exception:
    print 'No MySql :('

print '<p>__name__ = %s</p>' %__name__
    
try:
    import os
    envs = ['%s = %s' %(k,v) for k,v in os.environ.iteritems()]
    print '<br>'.join(envs)
    
    import cgi
    form = cgi.parse()
    print '<p>%s</p>' %form
    
except Exception, e:
    print '%s' %e