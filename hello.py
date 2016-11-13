from flask import Flask,request,make_response,redirect
from flask_script import Manager

app= Flask(__name__)
manager = Manager(app)


@app.route('/')
def index():
	'''
	response = make_response('<h1>This is a cookie!</h1>')
	response.set_cookie('answer','42')
	return response
	
	return redirect('http://www.baidu.com')
	'''
	user_agent = request.headers.get('User-Agent')
	return '<h1>Hello World!</h1><br><p>your browser is %s</p>' %user_agent

@app.route('/user/<name>')
def user(name):
	return '<h1>Hello %s!</h1>' %name

if __name__ == '__main__':
	manager.run()
