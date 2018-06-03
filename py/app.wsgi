# return wsgi application for apache hook
import cmds

def application(environ, start_response):
    try:
        METHOD = environ['REQUEST_METHOD']
        
        if METHOD == 'POST':
            postData = environ['wsgi.input'].read()
            print postData
            func = 'none'
            cmd = getattr(cmds, func, None)
            if cmd:
                return cmd(postData['data'].value)
            else:
            	return 'unknown cmd: %s' %func
    except Exception, e:
        return str(e)