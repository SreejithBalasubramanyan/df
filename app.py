import os
#import magic
import urllib3.request
import pandas as pd
#from app import app
from flask import Flask, flash, request, redirect, render_template
UPLOAD_FOLDER = './'

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


from werkzeug.utils import secure_filename








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
        if 'file' not in request.files and 'youtube_link' not in request.form:
            flash('No file part or url')
            return redirect(request.url)
        elif 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                flash('No file selected for uploading')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join('./static', filename))
                from code import predict_model
                flash('File successfully uploaded')
                predict_model("%s" % (filename))
                r=filename.split(".")
                temp="static/"+r[0]+"1.mp4"
                t="static/"+r[0]+"1.avi"
                import ffmpy
                ff = ffmpy.FFmpeg(
                inputs={'%s'%(t): None},
                outputs={'%s'%(temp): None})
                ff.run()
                df=pd.read_csv('static/%s.csv' %(r[0]),index_col = 0)
                temp2="static/"+r[0]+"1.ogg"
                temp3="static/"+r[0]+".png"
                #df=pd.read_csv('static/ %s.csv' %(r[0]),index_col = 0)
                return render_template('hello.html',tables=[df.to_html(classes='data')], titles=df.columns.values,fname=temp,oname=temp2,iname=temp3)
            else:
                flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
                return redirect(request.url)

        elif 'youtube_link' in request.form:
            youtube_url = request.form['youtube_link']
            from pytube import YouTube
            from pytube import extract
            yt = YouTube(youtube_url)
            file=yt.streams.filter(progressive=True,mime_type="video/mp4").first()
            filename2=(file.title).split(" ")
            r=filename2[0]
            file.download("./static",r)
            from code import predict_model
            flash('File successfully uploaded')
            filename=r+".mp4"
            predict_model("%s" % (filename))
            temp="/static/"+r+"1.avi"
            temp2="/static/"+r+"1.ogg"
            temp3="static/"+r+".png"
            df=pd.read_csv('static/%s.csv' %(r),index_col = 0)
            return render_template('hello.html',tables=[df.to_html(classes='data')], titles=df.columns.values,fname=temp,oname=temp2,iname=temp3)
            #file.title

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=5000) 
