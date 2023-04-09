from app import app
import os
import pandas as pd
from flask import render_template, request, redirect, session, abort, url_for
from app import etfe_arch
from app import uvalue


users = pd.read_csv('app/templates/admin/db.csv')

@app.route('/')


def index():

# if you want to control forbiden request abort 403-means forbidden
	#abort(500)

	
	return render_template('public/index.html')



from flask import flash



		



@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():

	

	if request.method == "POST":

		req = request.form

		email = req.get("email")
		username = req.get("username")
		password = req.get("password")

		users = pd.read_csv("app/templates/admin/db.csv")
		for item in users:
			
			if item == email:

				flash("This email appears registered in our system, go to login and use this email credentials or retrive them if forgotten", 'warning')
				return redirect(request.url)


		if not username:

			flash("You must enter your name", "warning")
			return redirect(request.url)


		



		if not len(password) >= 5:
			flash("Password length must be at least 5 characters or numbers", "warning")
			return redirect(request.url)
		
		
		users[email] = {email:0, username:1, password:2}


		df = pd.DataFrame(users, columns=users.keys())
		
		df.to_csv('app/templates/admin/db.csv', index=False)
	

		
		import smtplib
		from email.mime.text import MIMEText
		from email.mime.multipart import MIMEMultipart
		email_user = 'marco.fabrix360@gmail.com'
		email_send = email
		subject = 'Do not reply-fabrix360 thank you'
		
		msg = MIMEMultipart()
		msg['from'] = email_user
		msg['To'] = email_send
		msg['Subject'] = subject
		body = 'Dear app user, Your activation code is: 1890'
		msg.attach(MIMEText(body, 'plain'))
		text = msg.as_string()
		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.starttls()
		server.login(email_user, 'fuvnhkxiqixqnezb')
		server.sendmail(email_user, email_send, text)
		server.quit()
			
			
					

				

		flash("Account created!, activation code has been sent to your e-mail, get your activation code then login from nav bar to use the app ", "success")
	
		return redirect(request.url)
	
	return render_template("public/sign_up.html")


"""
to work in session you need to create secure key or secret key
from folder app / type 'python'
>>> import secrets
>>> secrets.token_urlsafe(16)
'OCML3BRawWEUeaxcuKHLpw'
"""



app.config["SECRET_KEY"] = '3Fnd9t3a74A-dM1Nq8RhAw'


#users = pd.read_csv('app/templates/admin/db.csv')

@app.route("/sign-in", methods=["GET", "POST"])
def sign_in():

	users = pd.read_csv('app/templates/admin/db.csv')

	if request.method == 'POST':

		req = request.form

		email = req.get("email")
		password = req.get("password")
		activation_code = req.get("activation_code")

		if not email in users:
			flash("Session for this email has expired, or email not found. Sign up again to login", 'warning')
			return redirect(request.url)
		else:
			user = users[email]

		if not password == user[2]:
			flash("Incorrect password, re-enter correct password", 'warning')
			return redirect(request.url)

		if not float(activation_code) == 1890:
			flash("wrong activation code, re-enter correct activation code ", 'warning')
			return redirect(request.url)

		else:
			session["USERNAME"] = user[0]
			print('user added to session')
			return redirect(url_for("profile"))


			

			





	return render_template('public/sign_in.html')


@app.route("/profile")
def profile():

	if session.get("USERNAME") is not None:
		#email = session.get("USERNAME")
		#user = users[username]

		#return render_template("admin/profile.html", user=user)
		return etfe_arch()

		
	else:
		flash("You are not loged in!", "warning")
		return redirect(url_for("sign_in"))


@app.route("/sign-out")
def sign_out():

	session.pop("USERNAME", None)

	return redirect(url_for("sign_in"))

@app.route('/forgot-pw', methods=["POST", "GET"])
def forgot_pw():

	if request.method == 'POST':

		req = request.form

		email = req.get("email")

		if not email in users:
			flash("Sorry, we dont have records for this e-mail, sign up to create account", "warning")
			return redirect(request.url)
		else:
			user = users[email]
			your_password = user[2]

			import smtplib
			from email.mime.text import MIMEText
			from email.mime.multipart import MIMEMultipart
			email_user = 'marco.fabrix360@gmail.com'
			email_send = email
			subject = 'Do not reply-fabrix360 retrive your app password'
			
			msg = MIMEMultipart()
			msg['from'] = email_user
			msg['To'] = email_send
			msg['Subject'] = subject
			body = ('Dear app user, your password is: "{}"'.format(your_password)) + '\t(And, your activation code is: 1890)'
			msg.attach(MIMEText(body, 'plain'))
			text = msg.as_string()
			server = smtplib.SMTP('smtp.gmail.com', 587)
			server.starttls()
			server.login(email_user, 'fuvnhkxiqixqnezb')
			server.sendmail(email_user, email_send, text)
			server.quit()

			flash("your password and activation code were sent to your registered email", 'success')




			return render_template('public/forgot_pw.html')

	return render_template('public/forgot_pw.html')




