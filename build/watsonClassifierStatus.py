import json
from os.path import join, dirname
from watson_developer_cloud import VisualRecognitionV3

# authentication
visual_recognition = VisualRecognitionV3( \
    VisualRecognitionV3.latest_version, \
    api_key='07e9eaf4bbd732fe9a6d89d676f113620491d17e')

# print classifier details
print(json.dumps(visual_recognition.get_classifier('Cancer_825696101'), indent=2))