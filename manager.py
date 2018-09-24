# -*- coding: utf-8 -*-

import www
from application import app, manager
from flask_script import Server
from jobs.launcher import runJob
from test.launcher import runTest

# run web server
manager.add_command( "runserver", Server( host='0.0.0.0',port=app.config['SERVER_PORT'],use_debugger = True ,use_reloader = True) )

# run job task
manager.add_command('runjob', runJob() )

# run test case
manager.add_command( 'runtest', runTest() )

def main():
    manager.run( )

if __name__ == '__main__':
    try:
        import sys
        sys.exit( main() )
    except Exception as e:
        import traceback
        traceback.print_exc()
