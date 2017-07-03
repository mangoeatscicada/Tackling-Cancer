import numpy as np
import json, sys, cv2, zipfile, os, shutil, pprint
from os.path import join, dirname
from watson_developer_cloud import VisualRecognitionV3
from PIL import Image

# authentication
visual_recognition = VisualRecognitionV3(VisualRecognitionV3.latest_version, \
    api_key = '1f99876aede140f190790ed9c86499e6fe9d525d')

# classify ID
classifier_id = 'Cancer_1009023861'

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

    imageList = []
    
    os.makedirs("tmp")

    zipFile = zipfile.ZipFile(zip_path)
    zipFile.extractall("tmp")
    zipFile.close()

    images = "tmp/"

    # read data to classify
    for tmpDir in  os.listdir(images):
        if tmpDir in zip_path:
            for image_file in os.listdir(images+tmpDir):
                if image_file.endswith(".jpg"):
                    p = classifyImage(join(images, tmpDir, image_file))
                    imageList.append(p)
    

    # delete tmp dir
    shutil.rmtree("./tmp/", ignore_errors=True)

    # return image list
    return imageList

def classify(argv):

    # read the file
    filename = argv[0]

    # check it's an image file
    if filename.endswith(".jpg"):
        return classifyImage(filename)

    # check it's a zip file
    elif filename.endswith(".zip"):
        return classifyZip(filename)

    else:
        sys.exit(filename + " could not be read as an image or zip file")

if __name__ == "__main__":
    classify(sys.argv[1:])