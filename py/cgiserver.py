#!/usr/bin/python
''' Service entry point for complexbear
'''
import cgi
import cgitb
import sys
import os

#cgitb.enable()

# Local imports
import cmds



def main():
    try:
        METHOD = os.environ['REQUEST_METHOD']
        
        if METHOD == 'POST':
            postData = cgi.FieldStorage()
            print "Content-Type: text/json\n"
            print >> sys.stderr, 'postData: %s\n' %postData.keys()
            func = postData['cmd'].value
            cmd = getattr(cmds, func, None)
            if cmd:
                cmd(postData['data'].value)
    except Exception, e:
        print >> sys.stderr, str(e)        

if __name__ == '__main__':
    main()
  