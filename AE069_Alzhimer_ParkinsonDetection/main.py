# import the necessary packages
from flask import Flask, render_template, redirect, url_for, request,session,Response
from werkzeug import secure_filename
import sqlite3
import pandas as pd
from datetime import datetime
import os
from utils import *
from autils import *
#from voiceTest import *
import cnn_svm

name = ''
pred = ''
suggest = ''
voicePred = ''

app = Flask(__name__)

app.secret_key = '1234'
app.config["CACHE_TYPE"] = "null"
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/', methods=['GET', 'POST'])
def landing():
	return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	global name
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		con = sqlite3.connect('mydatabase.db')
		cursorObj = con.cursor()
		cursorObj.execute(f"SELECT Name from Users WHERE Email='{email}' AND password = '{password}';")
		try:
			name = cursorObj.fetchone()[0]
			return redirect(url_for('home'))
		except:
			error = "Invalid Credentials Please try again..!!!"
			return render_template('login.html',error=error)
	return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
	error = None
	if request.method == 'POST':
		if request.form['sub']=='Submit':
			name = request.form['name']
			email = request.form['email']
			password = request.form['password']
			rpassword = request.form['rpassword']
			pet = request.form['pet']
			if(password != rpassword):
				error='Password dose not match..!!!'
				return render_template('register.html',error=error)
			try:
				con = sqlite3.connect('mydatabase.db')
				cursorObj = con.cursor()
				cursorObj.execute(f"SELECT Name from Users WHERE Email='{email}' AND password = '{password}';")
			
				if(cursorObj.fetchone()):
					error = "User already Registered...!!!"
					return render_template('register.html',error=error)
			except:
				pass
			now = datetime.now()
			dt_string = now.strftime("%d/%m/%Y %H:%M:%S")			
			con = sqlite3.connect('mydatabase.db')
			cursorObj = con.cursor()
			cursorObj.execute("CREATE TABLE IF NOT EXISTS Users (Date text,Name text,Email text,password text,pet text)")
			cursorObj.execute("INSERT INTO Users VALUES(?,?,?,?,?)",(dt_string,name,email,password,pet))
			con.commit()

			return redirect(url_for('login'))

	return render_template('register.html')

@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
	error = None
	global name
	if request.method == 'POST':
		email = request.form['email']
		pet = request.form['pet']
		con = sqlite3.connect('mydatabase.db')
		cursorObj = con.cursor()
		cursorObj.execute(f"SELECT password from Users WHERE Email='{email}' AND pet = '{pet}';")
		
		try:
			password = cursorObj.fetchone()
			#print(password)
			error = "Your password : "+password[0]
		except:
			error = "Invalid information Please try again..!!!"
		return render_template('forgot-password.html',error=error)
	return render_template('forgot-password.html')

@app.route('/home', methods=['GET', 'POST'])
def home():
	global name
	return render_template('home.html',name=name)

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
	return render_template('dashboard.html',name=name)



@app.route('/image', methods=['GET', 'POST'])
def image():
	if request.method=='POST':
		savepath = r'static/img/'
		f = request.files['doc']
		f.save(os.path.join(savepath,(secure_filename('test.jpg'))))
		return redirect(url_for('image_test'))
	return render_template('image.html',name=name)

@app.route('/image_test', methods=['GET', 'POST'])
def image_test():
	global pred,suggest
	pred,result,suggest = predictImg()
	return render_template('image_test.html',name=name,result=result,suggestion=suggest)

@app.route('/aimage', methods=['GET', 'POST'])
def aimage():
	if request.method=='POST':
		savepath = r'static/img/'
		f = request.files['doc']
		f.save(os.path.join(savepath,(secure_filename('atest.jpg'))))
		return redirect(url_for('aimage_test'))
	return render_template('aimage.html',name=name)

@app.route('/aimage_test', methods=['GET', 'POST'])
def aimage_test():
	global pred,suggest
	pred,result,suggest = predictAlzhimer()
	return render_template('aimage_test.html',name=name,result=result,suggestion=suggest)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
	global voicePred
	if request.method=='POST':
		if request.form['uploadbutton'] == 'Upload':
			savepath = r'upload/'
			f = request.files['doc']
			f.save(os.path.join(savepath,(secure_filename('test.wav'))))
			return render_template('upload.html',name=name,file=f.filename,mgs='File uploaded..!!')
		elif request.form['uploadbutton'] == 'Detect PD':
			voicePred,result = testVoice()
			return render_template('upload.html',name=name,mgs=result)
	return render_template('upload.html',name=name)

@app.route('/record', methods=['GET','POST'])
def record():
	global pred,voicePred,name
	if(pred == 'Parkinson' and voicePred == 'Parkinson'):
		final = 'Parkinson'
	elif(pred == 'Healthy' and voicePred == 'Healthy'):
		final = 'Healthy'
	else:
		final = 'Further Diagnosis is Required'
	now = datetime.now()
	dt_string = now.strftime("%d/%m/%Y %H:%M:%S")			
	con = sqlite3.connect('mydatabase.db')
	cursorObj = con.cursor()
	cursorObj.execute("CREATE TABLE IF NOT EXISTS FinalPred (Date text,Name text,DrawingPrediction text, VoicePrediction text, FinalPrediction text)")
	cursorObj.execute("INSERT INTO FinalPred VALUES(?,?,?,?,?)",(dt_string,name,pred,voicePred,final))
	con.commit()

	conn = sqlite3.connect('mydatabase.db', isolation_level=None,
						detect_types=sqlite3.PARSE_COLNAMES)
	df = pd.read_sql_query(f"SELECT * from FinalPred WHERE Name='{name}';", conn)
	
	return render_template('record.html',name=name,tables=[df.to_html(classes='table-responsive table table-bordered table-hover')], titles=df.columns.values)


# No caching at all for API endpoints.
@app.after_request
def add_header(response):
	# response.cache_control.no_store = True
	response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
	response.headers['Pragma'] = 'no-cache'
	response.headers['Expires'] = '-1'
	return response


if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True, threaded=True)
