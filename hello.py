from flask import Flask, request, make_response, redirect, render_template, session, url_for, flash
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm as Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import os
from flask_sqlalchemy import SQLAlchemy


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] =\
	'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Role(db.Model):
	__tablename__ = 'roles'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), unique=True, index=True)
	users = db.relationship('User', backref='role', lazy='dynamic')

	def __repr__(self):
		return 'Role %r' % self.name


class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), unique=True, index=True)
	role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

	def __repr__(self):
		return '<User %r>' % self.username


@app.route('/', methods=['GET', 'POST'])
def index():
	'''
	response = make_response('<h1>This is a cookie!</h1>')
	response.set_cookie('answer','42')
	return response
	
	return redirect('http://www.baidu.com')
	'''
	user_agent = request.headers.get('User-Agent')
	# return '<h1>Hello World!</h1><br><p>your browser is %s</p>' % user_agent
	# name = None
	form = NameFrom()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.name.data).first()
		if user is None:
			user = User(username=form.name.data)
			db.session.add(user)
			session['known'] = False
		else:
			session['known'] = True
		session['name'] = form.name.data
		# form.name.data = ''
		return redirect(url_for('index'))
	return render_template('index.html', current_time=datetime.utcnow(),
							form=form, name=session.get('name'), known=session.get('known', False), user_agent=user_agent)


@app.route('/user/<name>')
def user(name):
	# return '<h1>Hello %s!</h1>' % name
	return render_template('user.html', name=name)


@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
	return render_template('500.html'), 500


class NameFrom(Form):
	name = StringField('what\'s your name?', validators=[DataRequired()])
	submit = SubmitField('Submit')


if __name__ == '__main__':
	manager.run()
