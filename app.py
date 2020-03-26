import os
#import magic
import urllib3.request
#import torch

#from app import app
from flask import Flask, flash, request, redirect, render_template
UPLOAD_FOLDER = './'

app = Flask(__name__, template_folder='templates')
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


from werkzeug.utils import secure_filename



#model_path = './xception/full_raw.p'
#model = torch.load(model_path, map_location=torch.device('cpu'))




ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','mp4','avi'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
@app.route('/')
def hello():
    return render_template('index.html')
@app.route('/upload')
def upload_form():
	return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_file():
	if request.method == 'POST':
        # check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		if file.filename == '':
			flash('No file selected for uploading')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join('./static', filename))
			from code import predict_model
			flash('File successfully uploaded')
			predict_model("./static/%s" % (filename))
			return render_template('hello.html')
		else:
			flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
			return redirect(request.url)

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=5000)		 

# 	app.run(host='0.0.0.0', port=80)
