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
from flask import Flask, render_template, request
from werkzeug import secure_filename
import watsonClassify

app = Flask(__name__)

visual_recognition = VisualRecognitionV3(VisualRecognitionV3.latest_version, api_key="3722ed0d4950e9c3c3c187a471043b264b2de23c")

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
            result = json.dumps(visual_recognition.classify(images_file = image_file, threshold=0, classifier_ids=['Cancer_756185088']), indent = 2)
        remove(f.filename)
        return result
        return 'there was a problem sending the file'
        #watsonClassify.main(secure_filename(f.filename))

@app.route('/myapp')
def WelcomeToMyapp():
    return 'Welcome again to my app running on Bluemix!'

@app.route('/api/people')
def GetPeople():
    list = [
        {'name': 'John', 'age': 28},
        {'name': 'Bill', 'val': 26}
    ]
    return jsonify(results=list)

@app.route('/api/people/<name>')
def SayHello(name):
    message = {
        'message': 'Hello ' + name
    }
    return jsonify(results=message)

port = getenv('PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port))
