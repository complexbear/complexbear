# return wsgi application for apache hook
import sys
import os
import logging
import cgi 

location = os.path.dirname(os.path.realpath(__file__))

logging.basicConfig(filename='/tmp/server.log')
logging.getLogger().setLevel(logging.INFO)

sys.path.append(location)
logging.info('Py code location: ' + location)

cmds = None
try:
    cmds = __import__('cmds')
except Exception, e:
    print 'failed to import cmds: %s' %e

def application(environ, start_response):
    try:
        METHOD = environ['REQUEST_METHOD']
        
        if METHOD == 'POST':
            input = environ['wsgi.input']
            environ.setdefault('QUERY_STRING', '')
            postData = cgi.FieldStorage(fp=input,
                          environ=environ,
                          keep_blank_values=1)
            logging.info(postData)
            func = postData.getfirst('cmd',None)
            logging.info('CMD = ' + func)
            cmd = cmds.Cmd(environ['REMOTE_PORT'])
            if cmd:
                return cmd.process(func, postData['data'].value)
            else:
                return 'unknown cmd: %s' %func
    except Exception, e:
        logging.exception(e)
        return str(e)