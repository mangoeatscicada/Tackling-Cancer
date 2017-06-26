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

import json, watson, cellextractor, shutil
from os.path import join, dirname, exists
from os import environ, getenv, listdir, remove, makedirs
from watson_developer_cloud import VisualRecognitionV3  
from flask import Flask, render_template, request, send_from_directory, redirect, url_for, jsonify
from werkzeug import secure_filename

UPLOAD_FOLDER = 'temp'
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'zip'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

# parse json dump string into cleaner string
def jsonstrto(jsonstr):
    result = ''
    j = json.loads(jsonstr)
    images = j['images']
    for image in range(len(images)):
        result += "Cell: " + str(images[image]['image']) + '\n'
        classes = images[image]['classifiers'][0]['classes']
        for c in range(len(classes)):
            if classes[c]['class'] == 'blood':
                result += 'Blood: ' + str(classes[c]['score']) + '\n'
            if classes[c]['class'] == 'cancer':
                result += 'Cancer: ' + str(classes[c]['score']) + '\n'
            if classes[c]['class'] == 'other':
                result += 'Other: ' + str(classes[c]['score']) + '\n'
    return result + '\n'

# home
@app.route('/')
def Welcome():
    # delete any temp dir if it exists
    shutil.rmtree("./temp/", ignore_errors=True)
    shutil.rmtree("./tmp/", ignore_errors=True)

    return app.send_static_file('index.html')

@app.route('/results', methods = ['GET', 'POST'])
def upload():
    if request.method == 'POST':
        
        f = request.files['file']

        if allowed_file(f.filename):
            filename = secure_filename(f.filename)
            makedirs("temp")
            filepath = join(app.config['UPLOAD_FOLDER'], filename)
            f.save(filepath)
            
            # uploaded file is an image
            if filename.endswith(".jpg"):
                
                # classify image and clean result
                result = watson.classify([filepath])
                result = jsonstrto(result).split('\n')

            # uploaded file is a zip
            if filename.endswith(".zip"):
                result = watson.classify([filepath])

                jsonstrlist = ''

                result = result.split('$') 

                for item in range(len(result) - 1):
                    jsonstrlist += jsonstrto(result[item])

                jsonstrlist += 'Classifier_ID: Cancer_1509313240'

                result = jsonstrlist.split('\n')

            # delete temp dir
            shutil.rmtree("./temp/", ignore_errors=True)

            # return result rendered onto html page
            return render_template('results.html', result = result)

@app.route('/result', methods = ['GET', 'POST'])
def main_upload():
    if request.method == 'POST':
        f = request.files['file']

        if allowed_file(f.filename):
            filename = secure_filename(f.filename)
            makedirs("temp")
            filepath = join(app.config['UPLOAD_FOLDER'], filename)
            f.save(filepath)
            cellextractor.main([filepath])

            result = watson.classify(["temp.zip"])

            jsonstrlist = ''

            result = result.split('$') 

            for item in range(len(result) - 1):
                jsonstrlist += jsonstrto(result[item])

            jsonstrlist += 'Classifier_ID: Cancer_1509313240'

            # delete temp dir
            shutil.rmtree("./temp/", ignore_errors=True)
            remove("temp.zip")

            return render_template('results.html', result = jsonstrlist.split('\n'))

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.errorhandler(IOError)
def io_error(e):
    return render_template('io_error.html')

@app.errorhandler(NameError)
def name_error(e):
    return render_template('io_error.html')

@app.errorhandler(ValueError)
def value_error(e):
    return render_template('io_error.html')

@app.route('/testing')
def testing():
    return app.send_static_file('indexcopy.html')

port = getenv('PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port), debug=True)