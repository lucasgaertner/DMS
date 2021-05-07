from flask import Flask, flash, request, redirect, render_template, send_from_directory, jsonify, make_response
import flask_sqlalchemy
#from .model import Document, db
#from . import config
from datetime import datetime, timedelta
from PIL import Image
import os, glob
import shutil
import base64
#import magic
import urllib.request
from werkzeug.utils import secure_filename
from skripte.converter import convert_pdf_to_tif
from skripte.data_processing import normalize
from skripte.pytesseract_ocr import get_text_from_tif, merge_files
from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer, CountVectorizer
import pickle
#db connection
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

DBUSER = 'postgres'
DBPASS = 'start.123'
DBHOST = 'postgres'
DBPORT = '5432'
DBNAME = 'documents'

db = SQLAlchemy()

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{db}'.format(user=DBUSER,passwd=DBPASS,host=DBHOST,port=DBPORT,db=DBNAME)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

class Document(db.Model):
	__tablename__ = 'document_informations'
	id = db.Column(db.Integer, primary_key=True)
	filename = db.Column(db.String(100))
	blob = db.Column(db.LargeBinary)
	extension = db.Column(db.String(100))
	content = db.Column(db.Text())
	timestamp = db.Column(db.TIMESTAMP()) # just add for sake of this error, dont add in db
	def __init__(self, filename, blob, extension, content, timestamp):
		self.filename = filename
		self.blob = blob
		self.extension = extension
		self.content = content
		self.timestamp = timestamp

STATIC  = 'static'
UPLOAD_FOLDER = 'uploads'
TIF = 'tif'
JOINED_TEXT_FOLDER = 'joined_text'
UPLOADED_FILES = 'uploaded_files'
NON_PDFS = 'non_pdfs'



app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['STATIC'] = STATIC
app.config['TIF'] = TIF
app.config['JOINED_TEXT_FOLDER'] = JOINED_TEXT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOADED_FILES'] = UPLOADED_FILES



ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def upload_form():
	return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_file():
	if request.method == 'POST':
		# check if the post request has the files part
		if 'files[]' not in request.files:
			flash('No file part')
			return redirect(request.url)
		files = request.files.getlist('files[]')

		for file in files:
			if file and allowed_file(file.filename):
				# Non PDF files
				filename = secure_filename(file.filename)
				# convert file to pdf
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
				if filename[-3:] != "pdf":
					tmp_file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
					tmp_image = Image.open(tmp_file)
					extension = tmp_file[:-3]
					tmp_filename = tmp_file[:-3] + "pdf"
					tmp_image.save(tmp_filename, "PDF" ,resolution=300.0, save_all=True)
					shutil.move(tmp_file, os.path.join(app.config['UPLOAD_FOLDER'], app.config['UPLOADED_FILES'], "non_pdfs", filename)) 
					filename = tmp_filename[8:]
					
				# PDF files 
				if filename[-3:] == "pdf":
					tmp_file = os.path.join(app.config['UPLOAD_FOLDER'], filename)
					# convert pdf to tif using pytesseract
					convert_pdf_to_tif(os.path.join(app.config['UPLOAD_FOLDER'], filename), os.path.join(app.config['UPLOAD_FOLDER'], app.config['TIF'], filename))
					# get text
					get_text_from_tif(app.config['UPLOAD_FOLDER'], filename)
					getText = merge_files(app.config['UPLOAD_FOLDER'], filename)
					# stemming, lemmatized finished!!!
					documents = normalize(os.path.join(app.config['UPLOAD_FOLDER'],app.config['JOINED_TEXT_FOLDER']), filename[:-4])

					# Vectorizing the document
					# cv = pickle.load(open(os.path.join("model", "vectorizer.p"),'rb'))
					# tfidf = cv.transform(documents)
					# mnb = pickle.load(open(os.path.join("model", "save.p"),'rb'))
					# pred = mnb.predict_proba(tfidf)

					with open(tmp_file, 'rb') as f:
						blob = base64.b64encode(f.read())
					text_file = open('test_blob.txt', "wb")
					
					# save into db
					extension = filename[-3:]
					uploadtime = datetime.now() + timedelta(hours=2)
					doc=Document(filename, blob, extension, getText, uploadtime)
					db.session.add(doc)
					db.session.commit()
					text_file.write(blob)
					text_file.close()
					#moving uploaded file
					shutil.move(tmp_file, os.path.join(app.config['UPLOAD_FOLDER'], app.config['UPLOADED_FILES'], filename)) 
				else:
					pass
		return redirect("/overview")


@app.route('/uploded')
def predicted():
	return render_template('prediction.html')

@app.route('/overview')
def overview():
	try:
		dir = os.path.join(app.config['STATIC'], "uploads")
		filelist = glob.glob(os.path.join(dir, "*"))
		for f in filelist:
			os.remove(f)
	except:
		pass
	docs = Document.query.order_by(Document.timestamp.asc()).all()
	results = [
	{
		"id": doc.id,
		"filename": doc.filename,
		"extension": doc.extension,
		"content": str(doc.content).lower(),
		"timestamp": doc.timestamp
	} for doc in docs]
	return render_template('overview.html', data=results)

@app.route('/overview/rev')
def reversed_overview():
	try:
		dir = os.path.join(app.config['STATIC'], "uploads")
		filelist = glob.glob(os.path.join(dir, "*"))
		for f in filelist:
			os.remove(f)
	except:
		pass
	docs = Document.query.order_by(Document.timestamp.desc()).all()
	results = [
	{
		"id": doc.id,
		"filename": doc.filename,
		"extension": doc.extension,
		"content": str(doc.content).lower(),
		"timestamp": doc.timestamp
	} for doc in docs]
	return render_template('overview.html', data=results)


@app.route("/view/<int:number>", methods= ['GET'])
def documentView(number=None):
	print(number)
	viewerDocument = Document.query.filter_by(id=number).first()
	FILENAME = viewerDocument.filename
	BLOB = viewerDocument.blob

	decodedDocument = base64.b64decode(BLOB)
	with open(os.path.expanduser(os.path.join(app.config['STATIC'],"uploads",FILENAME)), 'wb') as fout:
		fout.write(base64.decodestring(BLOB))
	results = {'filename': os.path.join("uploads",FILENAME) }
	return render_template('view.html', data=results)

@app.route("/appview/<int:number>", methods= ['GET'])
def documentAppView(number=None):
	print(number)
	viewerDocument = Document.query.filter_by(id=number).first()
	FILENAME = viewerDocument.filename
	BLOB = viewerDocument.blob

	decodedDocument = base64.b64decode(BLOB)
	with open(os.path.expanduser(os.path.join(app.config['STATIC'],"uploads",FILENAME)), 'wb') as fout:
		fout.write(base64.decodestring(BLOB))
	results = {'filename': os.path.join("uploads",FILENAME) }


    
	
	response = make_response(decodedDocument)
	response.headers['Content-Type'] = 'application/pdf'
	response.headers['Content-Disposition'] = \
		'inline; filename=%s.pdf' % FILENAME
	return response




@app.route("/jso/<path:path>", methods= ['GET'])
def getJson(path):
	return send_from_directory(app.config['STATIC'] , path, as_attachment=True)

@app.route("/json", methods= ['GET'])
def Json():
	docs = Document.query.order_by(Document.timestamp.desc()).all()
	results = [
	{
		"id": doc.id,
		"filename": doc.filename,
		"extension": doc.extension,
		"content": str(doc.content).lower(),
		"timestamp": doc.timestamp
	} for doc in docs]
	res = {"Documents": results}
	return jsonify(res)


if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0')
