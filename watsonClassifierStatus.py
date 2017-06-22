import json
from os.path import join, dirname
from watson_developer_cloud import VisualRecognitionV3

# authentication
visual_recognition = VisualRecognitionV3( \
    VisualRecognitionV3.latest_version, \
    api_key='c8be440798e52325714997d9f7f3f0407e38d57d')

# print classifier details
print(json.dumps(visual_recognition.get_classifier('Cancer_939779875'), indent=2))