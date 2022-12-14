import os
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS



basedir = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(basedir + '/excelFiles')


app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'secret-key'
#app.config['SQLALCHEMY_DATABASE_URI'] =\
#       'sqlite:///' + os.path.join(basedir, 'database.db')

#Localhost uri
#app.config['SQLALCHEMY_DATABASE_URI'] ='mysql+pymysql://juanseAdmin:52fa33f66@localhost:3307/dianProject'

app.config['SQLALCHEMY_DATABASE_URI'] =  'postgresql://root:j5AwLAk8n6lZPmluq7EMkGP0o18PZvCw@dpg-cdpurq82i3mjaloc3u5g-a:5432/dianproject'
#online Uri
#app.config['SQLALCHEMY_DATABASE_URI'] ='mysql+pymysql://root:4Nnc5YHjofY18CBNN2or@containers-us-west-112.railway.app:6147/railway'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['TEMPLATES_AUTO_RELOAD'] = True

db = SQLAlchemy(app)



login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

from models import User

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))

from auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)


from main import main as main_blueprint
app.register_blueprint(main_blueprint)
  
       
 


