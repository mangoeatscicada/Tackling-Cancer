import json
from os.path import join, dirname
from os import environ
from watson_developer_cloud import VisualRecognitionV3

visual_recognition = VisualRecognitionV3(VisualRecognitionV3.latest_version, api_key='3722ed0d4950e9c3c3c187a471043b264b2de23c')

with open(join(dirname(__file__), "images/extract-automatic/cancer.zip"), 'rb') as trainingCancer, \
    open(join(dirname(__file__), "images/extract-automatic/blood.zip"), 'rb') as trainingBlood, \
    open(join(dirname(__file__), "images/extract-automatic/other.zip"), 'rb') as trainingOther :
 print "Uploading files..."
 print(json.dumps(visual_recognition.create_classifier('Cancer', \
    cancer_positive_examples=trainingCancer, \
    blood_positive_examples=trainingBlood, \
    other_positive_examples=trainingOther, \
    cancer_negative_examples=trainingBlood, \
    blood_negative_examples=trainingCancer), indent=2))