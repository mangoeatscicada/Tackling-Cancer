import json
from os.path import join, dirname
from watson_developer_cloud import VisualRecognitionV3

# authentication
visual_recognition = VisualRecognitionV3( \
    VisualRecognitionV3.latest_version, \
    api_key='1f99876aede140f190790ed9c86499e6fe9d525d')

# print classifier details
print(json.dumps(visual_recognition.get_classifier('Cancer_1009023861'), indent=2))