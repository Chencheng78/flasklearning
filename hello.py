from flask import Flask, request, make_response, redirect, render_template
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime

app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)


@app.route('/')
def index():
	'''
	response = make_response('<h1>This is a cookie!</h1>')
	response.set_cookie('answer','42')
	return response
	
	return redirect('http://www.baidu.com')
	'''
	#user_agent = request.headers.get('User-Agent')
	#return '<h1>Hello World!</h1><br><p>your browser is %s</p>' % user_agent
	return render_template('index.html', current_time=datetime.utcnow())

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
if __name__ == '__main__':
	manager.run()
