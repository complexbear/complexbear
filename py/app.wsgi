import os, sys
location = os.path.dirname(os.path.realpath(__file__))
sys.path.append(location)

import app
application = app.application()