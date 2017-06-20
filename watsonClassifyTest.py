import json
from os.path import join, dirname
from os import environ
from watson_developer_cloud import VisualRecognitionV3

visual_recognition = VisualRecognitionV3(VisualRecognitionV3.latest_version, api_key='3722ed0d4950e9c3c3c187a471043b264b2de23c')

with open(join(dirname(__file__), 'images/extract-automatic/cancer-test.zip'), 'rb') as image_file:
 print(json.dumps(visual_recognition.classify(images_file=image_file, threshold=0, classifier_ids=['Cancer_756185088']), indent=2))

with open(join(dirname(__file__), 'images/extract-automatic/blood-test.zip'), 'rb') as image_file:
 print(json.dumps(visual_recognition.classify(images_file=image_file, threshold=0, classifier_ids=['Cancer_756185088']), indent=2))

with open(join(dirname(__file__), 'images/extract-automatic/other-test.zip'), 'rb') as image_file:
 print(json.dumps(visual_recognition.classify(images_file=image_file, threshold=0, classifier_ids=['Cancer_756185088']), indent=2))