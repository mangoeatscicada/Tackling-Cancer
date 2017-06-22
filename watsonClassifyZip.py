import numpy as np
import json, sys, cv2, zipfile, os, shutil
from os.path import join, dirname
from watson_developer_cloud import VisualRecognitionV3
from PIL import Image

def classifyImage(path, authentication):
    # look at jpegs
    if path.endswith(".jpg"):
        
        # open each image (max size known to be 30x30)
        image = Image.open(path)

        # classify image file
        with open(join(dirname(__file__), path), 'rb') as image_file:
            result = json.dumps(authentication.classify( \
                images_file=image_file, \
                threshold=0, \
                classifier_ids=['Cancer_1509313240']), indent=2)
            return result

def main(argv):
    imageList = []

    zipFile = zipfile.ZipFile(argv)

    zipFile.extractall("tmp")

    zipFile.close()

    images = "tmp/"

    # authentication
    visual_recognition = VisualRecognitionV3( \
        VisualRecognitionV3.latest_version, \
        api_key='3722ed0d4950e9c3c3c187a471043b264b2de23c')

    # read data to classify
    for tmpDir in  os.listdir(images):
        if tmpDir in argv:
            for image_file in os.listdir(images+tmpDir):
                p = classifyImage(images+tmpDir+"/"+image_file, visual_recognition)
                imageList.append(p)
    
    # delete tmp dir
    shutil.rmtree("./tmp/", ignore_errors=True)

    # return image list
    for i in imageList:
        print i
    return imageList

if __name__ == "__main__":
    main(sys.argv[1])