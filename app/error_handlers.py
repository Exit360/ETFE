from app import app
from flask import render_template, Request

@app.errorhandler(404)
def not_found(e):
	return render_template('public/404.html')


@app.errorhandler(500)
def server_error(e):

	
	return render_template('public/500.html')

@app.errorhandler(409)
def int_error(e):

	
	return render_template('public/422.html')


