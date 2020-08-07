from flask import Flask, flash, request, redirect, render_template
import flask_sqlalchemy
from .model import Document, db
from . import config
from datetime import datetime

import os
#import magic
import urllib.request
from werkzeug.utils import secure_filename
from skripte.converter import convert_pdf_to_tif
from skripte.data_processing import normalize
from skripte.pytesseract_ocr import get_text_from_tif, merge_files
from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer, CountVectorizer
import pickle


UPLOAD_FOLDER = 'uploads'
TIF = 'tif'
JOINED_TEXT_FOLDER = 'joined_text'

app = Flask(__name__)

# Tutorial section
app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_CONNECTION_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.app_context().push()
db.init_app(app)
db.create_all()


app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['TIF'] = TIF
app.config['JOINED_TEXT_FOLDER'] = JOINED_TEXT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

val = 0


ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def upload_form():
	return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_file():
    print("bin im upload_file")
    if request.method == 'POST':
        val = 0
        print(val)
        print("testlauf")
        # check if the post request has the files part
        if 'files[]' not in request.files:
            flash('No file part')
            return redirect(request.url)
        files = request.files.getlist('files[]')

        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                if filename[-3:] == "pdf":
                    # convert pdf to tif using pytesseract
                    convert_pdf_to_tif(os.path.join(app.config['UPLOAD_FOLDER'], filename), os.path.join(app.config['UPLOAD_FOLDER'], app.config['TIF'], filename))
                    # get text
                    get_text_from_tif(app.config['UPLOAD_FOLDER'], filename)
                    merge_files(app.config['UPLOAD_FOLDER'], filename)
                    # stemming, lemmatized finished!!!
                    documents = normalize(os.path.join(app.config['UPLOAD_FOLDER'],app.config['JOINED_TEXT_FOLDER']), filename[:-4])

                    # Vectorizing the document
                    cv = pickle.load(open(os.path.join("model", "vectorizer.p"),'rb'))
                    print("yeeeeeeeeeeeee\n\n\n")
                    tfidf = cv.transform(documents)
                    print("Vectorized")

                    mnb = pickle.load(open(os.path.join("model", "save.p"),'rb'))

                    print("opend model")
                    pred = mnb.predict_proba(tfidf)
                    print(pred)
    # "pred = mnb.predict_proba(x_testcv)"
                    print("worked!")
                else:
                    print("ich bin im else")
                val += 1
        flash("Probability: " + str(pred))

        document = document(datetime=datetime.now())
        db.session.add(document)
        db.session.commit()

        return redirect('/uploded')


@app.route('/uploded')
def predicted():
	return render_template('prediction.html')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
