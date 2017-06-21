# Copyright 2015 IBM Corp. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
from os.path import join, dirname
from os import environ, getenv, listdir, remove
from watson_developer_cloud import VisualRecognitionV3  
from flask import Flask, render_template, request, send_from_directory, redirect, url_for
from werkzeug import secure_filename
#import watsonClassify
import watsonClassifyZip

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'zip'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

visual_recognition = VisualRecognitionV3(VisualRecognitionV3.latest_version, api_key="c8be440798e52325714997d9f7f3f0407e38d57d")

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def Welcome():
    return app.send_static_file('index.html')

@app.route('/upload')
def upload_file():
    return app.send_static_file('upload.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        f = request.files['file']

        f.save(secure_filename(f.filename))
        with open(join(dirname(__file__), f.filename), 'rb') as image_file:
            result = json.dumps(visual_recognition.classify(images_file = image_file, threshold=0, classifier_ids=['Cancer_1509313240']), indent = 2)
        remove(f.filename)
        newRes = json.loads(result)
        return str(newRes)
        #return redirect(url_for('test_results', result = result))
        return 'there was a problem sending the file'
        #watsonClassify.main(secure_filename(f.filename))

@app.route('/test')
def test_results(result):
    return 'Redirect Complete' + result
    

@app.route('/zip_upload', methods = ['GET', 'POST'])
def upload_zip():
    if request.method == 'POST':
        f = request.files['file']
        if f.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if f and allowed_file(f.filename) :
            print 'Made it to here'
            filename = secure_filename(f.filename)
            f.save(join(app.config['UPLOAD_FOLDER'], filename))
            print 'And here'
            return redirect(url_for('uploaded_file', filename = filename))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    #return 'Hello World! Thanks for giving me ' + filename
    print 'Check 1'
    result = watsonClassifyZip.main('uploads/' + filename)
    print 'Check 2'
    return str(result)

port = getenv('PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port))
