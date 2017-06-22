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
from os.path import join, dirname, exists
from os import environ, getenv, listdir, remove, makedirs
from watson_developer_cloud import VisualRecognitionV3  
from flask import Flask, render_template, request, send_from_directory, redirect, url_for, jsonify
from werkzeug import secure_filename
#import watsonClassify
import watsonClassifyZip

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'zip'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

visual_recognition = VisualRecognitionV3(VisualRecognitionV3.latest_version, api_key="3722ed0d4950e9c3c3c187a471043b264b2de23c")

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def Welcome():
    return app.send_static_file('upload.html')

@app.route('/upload')
def upload_file():
    return app.send_static_file('upload.html')

@app.route('/results')
def result_page():
    return render_template('results.html', result = 'Hello World!')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        f = request.files['file']

        f.save(secure_filename(f.filename))
        with open(join(dirname(__file__), f.filename), 'rb') as image_file:
            result = json.dumps(visual_recognition.classify(images_file = image_file, threshold=0, classifier_ids=['Cancer_1509313240']), indent = 2)
            #result = jsonify(visual_recognition.classify(images_file = image_file, threshold=0, classifier_ids=['Cancer_1509313240']), indent = 2)
        remove(f.filename)
        #newRes = json.loads(result)
        #return result
        #return redirect(url_for('test_results', result = result))
        #print result
        return render_template('results.html', result = result)
        return 'there was a problem sending the file'
        #watsonClassify.main(secure_filename(f.filename))

@app.route('/test')
def test_results(result):
    return result
    

@app.route('/zip_upload', methods = ['GET', 'POST'])
def upload_zip():
    if request.method == 'POST':
        f = request.files['file']
        if f.filename == '':
            flash('No selected file')
            return redirect(url_for(upload_file))
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
    #return jsonify(result)
    #nstring = '{"results": ['
    #for item in result[:len(result)-1]:
    #    nstring += item
    #    nstring += ','
    #nstring += result[len(result)-1]
    #nstring += ']}'
    #return nstring
    return str(result)

@app.route('/main_upload', methods = ['GET', 'POST'])
def main_upload():
    if request.method == 'POST':
        f = request.files['file']
        if f.filename == '':
            flash('No selected file')
            return redirect(url_for(upload_file))
        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            #if not exists('/holding'):
            #    makedirs('/holding')
            #app.config["UPLOAD_FOLDER"] = '/holding'
            f.save(join(app.config['UPLOAD_FOLDER'], filename))
            import cellextractor
            cellextractor.main([join(app.config['UPLOAD_FOLDER'], filename)])
            return redirect(url_for('uploaded_file', filename = 'temp.zip'))

port = getenv('PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port), debug=True)
