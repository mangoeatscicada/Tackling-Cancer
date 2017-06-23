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

import json, watson
from os.path import join, dirname, exists
from os import environ, getenv, listdir, remove, makedirs
from watson_developer_cloud import VisualRecognitionV3  
from flask import Flask, render_template, request, send_from_directory, redirect, url_for, jsonify
from werkzeug import secure_filename

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'zip'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

visual_recognition = VisualRecognitionV3(VisualRecognitionV3.latest_version, api_key="1f99876aede140f190790ed9c86499e6fe9d525d")

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

def jsonstrto(jsnstr):
    result = ''
    num = 1
    j = json.loads(jsnstr)
    images = j['images']
    classifier_id = 'Cancer_1009023861'
    for image in range(len(images)):
        result += "Cell " + str(num) + "\nImage: " + str(images[image]['image']) + '\n'
        num += 1
        classes = images[image]['classifiers'][0]['classes']
        for c in range(len(classes)):
            if classes[c]['class'] == 'blood':
                result += 'Blood: ' + str(classes[c]['score']) + '\n'
            if classes[c]['class'] == 'cancer':
                result += 'Cancer: ' + str(classes[c]['score']) + '\n'
            if classes[c]['class'] == 'Other':
                result += 'Other: ' + str(classes[c]['score']) + '\n'
    return result + "Classifier ID: " + classifier_id

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
        
        result = watson.classifyImage(f.filename)

        result = jsonstrto(result).split('\n')

        remove(f.filename)
        #newRes = json.loads(result)
        #return result
        #return redirect(url_for('test_results', result = result))
        #print 
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
    result = watson.classify(['uploads/' + filename])
    print 'Check 2'
    #return jsonify(result)
    #nstring = '{"results": ['
    #for item in result[:len(result)-1]:
    #    nstring += item
    #    nstring += ','
    #nstring += result[len(result)-1]
    #nstring += ']}'
    #return nstring
    print result
    return render_template('results.html', result = jsonstrto(result).split('\n'))

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

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

port = getenv('PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port), debug=True)
