import json
from os.path import join, dirname
from watson_developer_cloud import VisualRecognitionV3

# authentication
visual_recognition = VisualRecognitionV3( \
    VisualRecognitionV3.latest_version, \
    api_key='3722ed0d4950e9c3c3c187a471043b264b2de23c')

# print classifier details
print(json.dumps(visual_recognition.get_classifier('Cancer_1509313240'), indent=2))