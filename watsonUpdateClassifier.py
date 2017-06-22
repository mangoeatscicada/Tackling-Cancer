import numpy as np
import json, sys, cv2
from os.path import join, dirname
from watson_developer_cloud import VisualRecognitionV3

def main(argv):

    # read the file
    filename = argv[0]
    classifier = argv[1]

    # authentication
    visual_recognition = VisualRecognitionV3( \
        VisualRecognitionV3.latest_version, \
        api_key='c8be440798e52325714997d9f7f3f0407e38d57d')

    # update cancer class
    if classifier == "cancer":
        with open(join(dirname(__file__), filename), 'rb') as trainer:
            return (json.dumps(visual_recognition.update_classifier( \
                'Cancer_939779875', \
                cancer_positive_examples=trainer, \
                blood_negative_examples=trainer), indent=2))

    # update blood class
    if classifier == "blood":
        with open(join(dirname(__file__), filename), 'rb') as trainer:
            return (json.dumps(visual_recognition.update_classifier( \
                'Cancer_939779875', \
                cancer_negative_examples=trainer, \
                blood_positive_examples=trainer), indent=2))

if __name__ == "__main__":
    main(sys.argv[1:])