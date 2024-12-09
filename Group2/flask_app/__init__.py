# ===================
# BPでエラーがでてます
# ===================

import sys
# __pycashe__を作らなくする
sys.dont_write_bytecode = True

from flask import Flask
from flask_app.models import *
from flask_migrate import Migrate
from flask_login import LoginManager

# appの設定
app = Flask(__name__,instance_relative_config=True)
app.config.from_pyfile('config.py')
app.config['UPLOAD_FOLDER'] = 'static/images/movieimages'  # 画像を保存するフォルダー
# app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}  # 許可するファイル拡張子

# DBの設定
db.init_app(app)
Migrate(app, db)

#LoginManager
login_manager = LoginManager(app)
login_manager.login_view = 'signin' 

#Blueprintの登録
from flask_app.views.auth import auth_bp
from flask_app.views.views import views_bp

app.register_blueprint(auth_bp)
app.register_blueprint(views_bp, name=views_bp)