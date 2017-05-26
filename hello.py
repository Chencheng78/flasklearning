from flask import Flask, request, make_response, redirect, render_template
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import Form
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired


app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
app.config['SECRET_KEY'] = 'hard to guess string'


@app.route('/', methods=['GET', 'POST'])
def index():
	'''
	response = make_response('<h1>This is a cookie!</h1>')
	response.set_cookie('answer','42')
	return response
	
	return redirect('http://www.baidu.com')
	'''
	#user_agent = request.headers.get('User-Agent')
	#return '<h1>Hello World!</h1><br><p>your browser is %s</p>' % user_agent
	name = None
	form = NameFrom()
	if form.validate_on_submit():
		name = form.name.data
		form.name.data = ''
	return render_template('index.html', current_time=datetime.utcnow(), form=form, name=name)

@app.route('/user/<name>')
def user(name):
	#return '<h1>Hello %s!</h1>' % name
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
