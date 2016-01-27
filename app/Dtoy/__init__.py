from flask import Flask
# from flask_bootstrap import Bootstrap


app = Flask(__name__)
app.config.from_object('config')
app.secret_key = 'ASDKHEW^$&%$213'


from flask_socketio import SocketIO
import eventlet

eventlet.monkey_patch()
socketio = SocketIO(app, async_mode='eventlet')


# bootstrap = Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/Dtoy.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# app.config['SQLALCHEMY_NATIVE_UNICODE'] = 'utf8'	

from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy()

db.init_app(app)

import user.routes
import deploy.routes


if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('log/Dtoy.log', 'a', 1 * 1024 * 1024, 10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('Dtoy startup')









