# -*- coding: utf-8 -*-
from application import app
from web.controllers.index import route_index
from web.controllers.messages.Message import route_message

app.register_blueprint( route_index,url_prefix = "/" )
app.register_blueprint( route_message,url_prefix = "/message" )
