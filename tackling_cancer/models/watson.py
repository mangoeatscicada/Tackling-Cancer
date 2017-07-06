import numpy as np
import json, sys, cv2, zipfile, os, shutil, pprint
from os.path import join, dirname
from watson_developer_cloud import VisualRecognitionV3
from PIL import Image
from pathlib import Path

# authentication
visual_recognition = VisualRecognitionV3(VisualRecognitionV3.latest_version, \
    api_key = '07e9eaf4bbd732fe9a6d89d676f113620491d17e')

# classify ID
classifier_id = 'Cancer_524812823'

def classifyImage(image_path):

    i = []

    # open each image (max size known to be 30x30)
    image = Image.open(image_path)
    
    # classify image file
    with open(image_path, 'rb') as image_file:
        result = json.dumps(visual_recognition.classify( \
            images_file=image_file, \
            threshold=0, \
            classifier_ids=[classifier_id]), indent=2)
        i.append(result)
    print i[0]
    return i[0]

def classifyZip(zip_path):
    
    # create temp directory and unzip images into it
    os.makedirs("tmp")
    zipFile = zipfile.ZipFile(zip_path)
    zipFile.extractall("tmp")
    zipFile.close()
    images = "tmp/"

    # read data to classify
    imageList = []
    for tmpDir in  os.listdir(images):
        if tmpDir in zip_path:
            for image_file in os.listdir(images+tmpDir):
                if image_file.endswith(".jpg"):
                    p = classifyImage(join(images, tmpDir, image_file))
                    imageList.append(p)
    

    # delete tmp dir
    shutil.rmtree("./tmp/", ignore_errors=True)

    # with open("017_biopsy.txt", 'wb') as archive:
    #     archive.write(json.dumps(imageList))

    # return image list
    return imageList

def archive(text_file):

    # return saved data for image previously classified
    with open(text_file, 'rb') as tf:
        source = tf.read()
        data = json.loads(source)
        return data

def classify(argv):

    # read the file
    filename = argv[0]

    # check if file already has saved data
    txtf = Path(filename[:-4] + ".txt")
    if txtf.is_file():
        return archive(str(txtf))

    # check it's an image file
    elif filename.endswith(".jpg"):
        return classifyImage(filename)

    # check it's a zip file
    elif filename.endswith(".zip"):
        return classifyZip(filename)

    # file could not be read as an image or zip file
    else:
        sys.exit(filename + " could not be read as an image or zip file")

if __name__ == "__main__":
    classify(sys.argv[1:])