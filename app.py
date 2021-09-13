from flask import Flask, render_template, make_response, url_for, request, redirect, json
from flask_cors import CORS, cross_origin
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
CORS(app, support_credentials=True)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['Access-Control-Allow-Origin'] = '*'
app.config['Access-Control-Allow-Credentials'] = 'true'

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://nicholas@localhost:9000/aws_bank_user"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class UserModel(db.Model):
	__tablename__ = 'users'

	user_id			= db.Column(db.Integer, primary_key=True)
	user_name		= db.Column(db.String(200), nullable=False)
	user_birth		= db.Column(db.DateTime, default=datetime.utcnow)
	user_balance	= db.Column(db.Float, default=0)

	def __init__(self,user_name,user_birth,user_balance):
		self.user_name		= user_name
		self.user_birth		= user_birth
		self.user_balance	= user_balance

	def __repr__(self):
		return '<User %r>' % self.user_id


@app.route('/users', methods=['GET','POST'])
# @cross_origin(headers=['Access-Control-Allow-Credentials','Authorization','Content-Type'])
def handle_users():

	if request.method == 'POST':
		print('\n', request.get_json(force=True), '\n')

		try:
			data = request.get_json(force=True)
			new_user = UserModel(
				user_name		= data['user_name']		,
				user_birth		= data['user_birth']	,
				user_balance	= data['user_balance']	,
			)

			db.session.add(new_user)
			db.session.commit()

			return f'success: {new_user.user_name} register has been finished'

		except:
			return 'error: request payload is in a wrong format'

	elif request.method == 'GET':
		users = UserModel.query.all()
		data = [
			{
				"user_id"		: user.user_id		,
				"user_name"		: user.user_name	,
				"user_birth"	: user.user_birth	,
				"user_balance"	: user.user_balance	,
			}
			for user in users
		]

		response = make_response( { "type": f"{type(data)}", "count": len(data), "users": data } )
		
		response.headers['Allow-Control-Allow-Origin'] = '*'
		response.headers['Allow-Control-Allow-Credentials'] = 'true'

		return response


if __name__ == "__main__":
	app.run( debug = True )