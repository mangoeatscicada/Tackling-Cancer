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

import tackling_cancer.models.watson as watson
import tackling_cancer.models.cellextractor as cellextractor
import json, shutil, matplotlib, time, StringIO
from os.path import join, dirname, exists, splitext, basename
from os import environ, getenv, listdir, remove, makedirs
from watson_developer_cloud import VisualRecognitionV3  
from flask import Flask, render_template, request, send_from_directory, redirect, url_for, jsonify, send_file
from werkzeug import secure_filename
from PIL import Image
from pathlib import Path

# import app
from tackling_cancer import app

# remove python rocket from dock (mac)
matplotlib.use("Agg")
import matplotlib.pyplot as plt, mpld3

UPLOAD_FOLDER = 'temp'
ALLOWED_EXTENSIONS = set(['jpg', 'zip'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

# parse json dump string into cleaner string
def jsonstrto(jsonstr, counter):
    result = []
    j = json.loads(jsonstr)
    images = j['images']
    for image in range(len(images)):
        result.append('Cell #' + str(counter))
        classes = images[image]['classifiers'][0]['classes']
        for c in range(len(classes)):
            if classes[c]['class'] == 'blood':
                result.append(classes[c]['score'])
            if classes[c]['class'] == 'cancer':
                result.append(classes[c]['score'])
            if classes[c]['class'] == 'other':
                result.append(classes[c]['score'])

    print result
    return result

# parse json object, return type 
def jsonType(jsonstr):
    j = json.loads(jsonstr)
    images = j['images']
    for image in range(len(images)):
        classes = images[image]['classifiers'][0]['classes']
        topscore = 0
        topclass = ''
        for c in range(len(classes)):
            if float(classes[c]['score']) > topscore:
                topscore = float(classes[c]['score'])
                topclass = classes[c]['class']
        return topclass

# homepage
@app.route('/')
def Welcome():
    # delete any temp dir if it exists on refresh
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
            fileextension = splitext(filename)[1]            
            filepath = join(app.config['UPLOAD_FOLDER'], filename)
            print(filepath)
            f.save(filepath)
            
            # uploaded file is an image
            if filename.endswith(".jpg"):
                
                # classify image and clean result
                result = watson.classify([filepath])
                resStats = result
                result = [jsonstrto(result, 1)]

                # handling the stats
                if jsonType(resStats) == 'blood':
                    cellStats = (100.0,0.0,0.0)
                elif jsonType(resStats) == 'cancer':
                    cellStats = (0.0, 100.0, 0.0)
                else: cellStats = (0.0, 0.0, 100.0)
                print cellStats
                typeStats = [int(cellStats[0]),int(cellStats[1]),int(cellStats[2])]

            # uploaded file is a zip
            if filename.endswith(".zip"):
                result = watson.classify([filepath])
                print result

                jsonstrlist = []

                # result = result.split('$') 

                numBlood = 0
                numCancer = 0
                numOther = 0

                counter = 1

                for item in result:
                    jsonstrlist.append(jsonstrto(item, counter))
                    counter += 1
                    # handling the stats
                    # res = result[item]
                    if jsonType(item) == 'blood':
                        numBlood += 1
                    if jsonType(item) == 'cancer':
                        numCancer += 1
                    if jsonType(item) == 'other':
                        numOther += 1
                totalCells = numBlood + numCancer + numOther
                percentB = numBlood/float(totalCells) * 100
                percentC = numCancer/float(totalCells) * 100
                percentO = numOther/float(totalCells) * 100
                cellStats = (percentB, percentC, percentO)

                typeStats = [int(cellStats[0]),int(cellStats[1]),int(cellStats[2])]

                print cellStats

                result = jsonstrlist
                print result

            # delete temp dir
            shutil.rmtree("./temp/", ignore_errors=True)

            # return result rendered onto html page
            return render_template('results/results.html', result = result, image=filepath, typeStats = typeStats)

@app.route('/result', methods = ['GET', 'POST'])
def main_upload():
    if request.method == 'POST':
        f = request.files['file']

        if allowed_file(f.filename):
            filename = secure_filename(f.filename)
            txtf = Path(filename[:-4] + ".txt")
            w = "temp.zip"
            if txtf.is_file():
                w = filename

            makedirs("temp")
            filepath = join(app.config['UPLOAD_FOLDER'], filename)
            print filepath
            f.save(filepath)
            cellextractor.main([filepath])
            originalImagePath = 'static/images/fullpic' + str(hash(filepath)) + '.jpg' 


            result = watson.classify([w])

            jsonstrlist = []

            numBlood = 0
            numCancer = 0
            numOther = 0

            counter = 1
            for item in result:
                jsonstrlist.append(jsonstrto(item, counter))
                counter += 1
                # handling the stats
                # res = result[item]
                if jsonType(item) == 'blood':
                    numBlood += 1
                if jsonType(item) == 'cancer': 
                    numCancer += 1
                if jsonType(item) == 'other':
                    numOther += 1
            totalCells = numBlood + numCancer + numOther
            percentB = numBlood/float(totalCells) * 100
            percentC = numCancer/float(totalCells) * 100
            percentO = numOther/float(totalCells) * 100
            cellStats = (percentB, percentC, percentO)

            typeStats = [int(cellStats[0]),int(cellStats[1]),int(cellStats[2])]

            # delete temp dir
            shutil.rmtree("./temp/", ignore_errors=True)
            if exists("temp.zip"):
                remove("temp.zip")

            # return result rendered onto html page
            return render_template('results/results.html', result = jsonstrlist, typeStats = typeStats, filePath = originalImagePath)

@app.route('/demobiopsy', methods = ['GET', 'POST'])
def demo():
    if request.method == 'POST':

        w = "temp.zip"

        val = request.form["demo"]

        # if demo image has previously been classified, change filename from temp.zip to (demo_img_name).zip
        txtf = Path(basename(val)[:-4] + ".txt")
        if txtf.is_file():
            w = basename(val)[:-4] + ".zip"
        
        else:
            cellextractor.main([val])

        result = watson.classify([w])

        jsonstrlist = []

        originalImagePath = 'static/images/' + basename(val) 
            
        numBlood = 0
        numCancer = 0
        numOther = 0
        counter = 1
        for item in result:
            jsonstrlist.append(jsonstrto(item, counter))
            counter += 1
            # handling the stats
            # res = result[item]
            if jsonType(item) == 'blood':
                numBlood += 1
            if jsonType(item) == 'cancer': 
                numCancer += 1
            if jsonType(item) == 'other':
                numOther += 1
        totalCells = numBlood + numCancer + numOther
        percentB = numBlood/float(totalCells) * 100
        percentC = numCancer/float(totalCells) * 100
        percentO = numOther/float(totalCells) * 100
        cellStats = (percentB, percentC, percentO)

        typeStats = [int(cellStats[0]),int(cellStats[1]),int(cellStats[2])]
        
        # delete temp dir
        shutil.rmtree("./temp/", ignore_errors=True)
        if exists("temp.zip"):
            remove("temp.zip")

        # return result rendered onto html page
        return render_template('results/results.html', result = jsonstrlist, typeStats = typeStats, filePath = originalImagePath)

# error handlers
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error/500.html'), 500

@app.errorhandler(IOError)
def io_error(e):
    return render_template('error/io_error.html')

@app.errorhandler(NameError)
def name_error(e):
    return render_template('error/io_error.html')

@app.errorhandler(ValueError)
def value_error(e):
    return render_template('error/io_error.html')

# test and loading page
@app.route('/testing')
def testing():
    return app.send_static_file('resTester.html')

@app.route('/loading')
def loading():
    return app.send_static_file('loading.html')

port = getenv('PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port), debug=True)
