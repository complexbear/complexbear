# return wsgi application for apache hook
import sys
import os
import logging
from flask import Flask, jsonify, request

location = os.path.dirname(os.path.realpath(__file__))
sys.path.append(location)

logging.basicConfig(
    format='%(asctime)s %(levelname)s\t- [%(name)s] %(message)s',
    level='DEBUG', 
    filename='/tmp/server.log'
)
logging.info('Py code location: ' + location)

import cmds

def blogserver():
    try:
        post_data = request.get_json(silent=True)           
        logging.info(request.data)     
        func = post_data.get('cmd')
        logging.info('CMD = ' + func)
        cmd = cmds.Cmd(request.environ.get('REMOTE_PORT'))
        if cmd:
            return cmd.process(func, post_data['data'])
        else:
            return 'unknown cmd: {}'.format(func)
    except Exception as e:
        logging.exception(e)
        return str(e)

def application():
    app = Flask(__name__)
    # app.debug = True

    @app.route('/', methods=['GET','POST'])
    def handler():
        try:
            return jsonify(blogserver()), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return app
        
if __name__ == '__main__':
    app = application()
    app.run(host='0.0.0.0', port=8000)
        