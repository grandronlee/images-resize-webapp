import os
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

from ImageObj import ImageObj

# Create an instance of the Flask class that is the WSGI application.
# The first argument is the name of the application module or package,
# typically __name__ when using a single module.
app = Flask(__name__)
app.config['SECRET_KEY'] = "asd123!@#"
app.config['UPLOAD_FOLDER'] = "static/uploads/"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')

@app.route('/images/resize', methods=['GET'])
def upload_form():
	return render_template('upload.html')

@app.route('/images/resize', methods=['POST'])
def imagesResize():
	data = request.form
	sizes = data.get('Sizes')
	sizeArray = sizes.split('x')
	width = sizeArray[0]
	height = sizeArray[1]
	
	if 'file' not in request.files:
		flash('No file part')
		return redirect(request.url)
	file = request.files['file']
	if file.filename == '':
		flash('No image selected for uploading')
		return redirect(request.url)
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		ImageObj.resize(os.path.join(app.config['UPLOAD_FOLDER'], filename),width,height)
		#print('upload_image filename: ' + filename)
		flash('Image successfully uploaded and displayed')
		return render_template('upload.html', filename=filename)
	else:
		flash('Allowed image types are -> png, jpg, jpeg, gif')
		return redirect(request.url)

@app.route('/display/<filename>')
def display_image(filename):
	print('display_image filename: ' + filename)
	return redirect(url_for('static',filename='uploads/' + filename), code=301)

if __name__ == '__main__':
    # Run the app server on localhost:4449
    app.run('localhost', 4449)
