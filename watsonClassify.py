import numpy as np
import json, sys, cv2
from os.path import join, dirname
from watson_developer_cloud import VisualRecognitionV3

def main(argv):

    # read the file
    filename = argv[0]
    src = cv2.imread(filename, cv2.IMREAD_COLOR)

    # check it's an image file
    if src is None:
        sys.exit(filename + " could not be read as an image file")

    # authentication
    visual_recognition = VisualRecognitionV3( \
        VisualRecognitionV3.latest_version, \
        api_key='c8be440798e52325714997d9f7f3f0407e38d57d')

    # classify image file
    with open(join(dirname(__file__), filename), 'rb') as image_file:
        result = json.dumps(visual_recognition.classify( \
            images_file=image_file, \
            threshold=0, \
            classifier_ids=['Cancer_939779875']), indent=2)
        print result
        return result

if __name__ == "__main__":
    main(sys.argv[1:])