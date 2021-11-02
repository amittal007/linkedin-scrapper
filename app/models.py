from app import db,login_manager
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



class User(db.Model,UserMixin):
	id = db.Column(db.Integer, primary_key = True)
	usertype = db.Column(db.String(30),default=1, nullable = True)
	first_name = db.Column(db.String(30), nullable = False)
	last_name = db.Column(db.String(30), nullable = False)
	email = db.Column(db.String(120),unique = True, nullable = False)
	# contact = db.Column(db.Integer,unique = True, nullable = False)
	#image_file = db.Column(db.String(20), nullable = False, default = 'default.jpg')
	password = db.Column(db.String(60), nullable = False)
	added_date = db.Column(db.DateTime,nullable = False,default = datetime.utcnow)
	is_active = db.Column(db.Boolean(), default=0, nullable=True)
	
	def __repr__(self):
		return self.first_name




db.create_all()
# from app import db
# db.create_all()


