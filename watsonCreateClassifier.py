import json
from os.path import join, dirname
from watson_developer_cloud import VisualRecognitionV3

# authentication
visual_recognition = VisualRecognitionV3( \
    VisualRecognitionV3.latest_version, \
    api_key='c8be440798e52325714997d9f7f3f0407e38d57d')

# delete existing classifier
#visual_recognition.delete_classifier('Cancer_939779875')

# train classifier
with open(join(dirname(__file__), "images/extract/cancer.zip"), 'rb') as trainingCancer, \
    open(join(dirname(__file__), "images/extract/blood.zip"), 'rb') as trainingBlood, \
    open(join(dirname(__file__), "images/extract-automatic/other.zip"), 'rb') as trainingOther :
 print "Uploading files..."
 print(json.dumps(visual_recognition.create_classifier( \
    'Cancer', \
    cancer_positive_examples=trainingCancer, \
    blood_positive_examples=trainingBlood, \
    other_positive_examples=trainingOther), indent=2))