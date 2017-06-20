import numpy as np
import json, sys, cv2
from os.path import join, dirname
from os import environ
from watson_developer_cloud import VisualRecognitionV3

def main(argv):

    # read the file
    filename = argv[0]
    classifier = argv[1]

    visual_recognition = VisualRecognitionV3(VisualRecognitionV3.latest_version, api_key='3722ed0d4950e9c3c3c187a471043b264b2de23c')

    if classifier == "cancer":
        with open(join(dirname(__file__), filename), 'rb') as trainer:
            return (json.dumps(visual_recognition.update_classifier('Cancer_1509313240', \
                cancer_positive_examples=trainer, \
                blood_negative_examples=trainer), indent=2))

    if classifier == "blood":
        with open(join(dirname(__file__), filename), 'rb') as trainer:
            return (json.dumps(visual_recognition.update_classifier('Cancer_1509313240', \
                cancer_negative_examples=trainer, \
                blood_positive_examples=trainer), indent=2))

if __name__ == "__main__":
    main(sys.argv[1:])