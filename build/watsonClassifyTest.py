import json
from os.path import join, dirname
from watson_developer_cloud import VisualRecognitionV3

# authentication
visual_recognition = VisualRecognitionV3( \
    VisualRecognitionV3.latest_version, \
    api_key='07e9eaf4bbd732fe9a6d89d676f113620491d17e')

# cancer test cases
with open(join(dirname(__file__), 'images/extract-automatic/cancer-test.zip'), 'rb') as image_file:
 print(json.dumps(visual_recognition.classify( \
    images_file=image_file, \
    threshold=None, \
    classifier_ids=['Cancer_825696101']), indent=2))

# blood test cases
with open(join(dirname(__file__), 'images/extract-automatic/blood-test.zip'), 'rb') as image_file:
 print(json.dumps(visual_recognition.classify( \
    images_file=image_file, \
    threshold=None, \
    classifier_ids=['Cancer_825696101']), indent=2))

# other test cases
with open(join(dirname(__file__), 'images/extract-automatic/other-test.zip'), 'rb') as image_file:
 print(json.dumps(visual_recognition.classify( \
    images_file=image_file, \
    threshold=None, \
    classifier_ids=['Cancer_825696101']), indent=2))