from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = 'e25a30bfb3e19e769cf8b5c0c024056be5162002'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://u_19_mag:123@159.69.151.133:5056/db_19_mag'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
