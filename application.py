# -*- coding: utf-8 -*-
import os

from flask import Flask

from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy


class Application( Flask ):
    def __init__(self,import_name):
        super( Application,self ).__init__( import_name )
        self.config.from_pyfile( 'config/base_setting.py' )
        self.config.from_pyfile( 'config/auto_export_group_msgs_setting.py' )
        self.config.from_pyfile( 'config/auto_get_group_info_setting.py' )
        if "ops_config" in os.environ:
            self.config.from_pyfile( 'config/%s_setting.py'%os.environ['ops_config'] )

        db.init_app( self )

db = SQLAlchemy()
app = Application( __name__ )
manager = Manager( app )
