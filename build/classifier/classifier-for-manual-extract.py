#!/usr/bin/python
from PIL import Image
import numpy as np
import os
from sklearn import linear_model

trainingCancerDir = "../images/extract-manual/cancer/"
trainingBloodDir = "../images/extract-manual/blood/"
testCancerDir = "../images/extract-manual/cancer-test/"
testBloodDir = "../images/extract-manual/blood-test/"

trainingImageList = []
testImageList = []

def getY(length, pos):
    '''Returns a numpy array of Y values'''
    posArray = np.ones(pos)
    negArray = np.zeros(length-pos)
    return np.concatenate((posArray,negArray))

def readImage(path):
    # look at the jpegs
    if path.endswith(".jpg"):
        
        # open each image then normalise  convert to greyscale and resize)
        #image = Image.open(path).convert("L").resize((20,20))
        image = Image.open(path).resize((18,18))
        
        # grab the pixel values into a 2d numpy array
        p = np.array(image)
        
        # reshape the 2d array into a 1d vector
        p = p.reshape(-1)

        return p
    
    return np.array([0,0])

def runTestData():
    testPosExamples = []
    testNegExamples = []
    
    for filename in os.listdir(testCancerDir):
        p = readImage(testCancerDir+filename)
        if p.size > 0:
            testPosExamples.append({"image":p,"filename":filename});

    for filename in os.listdir(testBloodDir):
        p = readImage(testBloodDir+filename)
        if p.size > 0:
            testNegExamples.append({"image":p,"filename":filename})
    
    print "Positive tests (should be 1.0):"
    for testPosExample in testPosExamples:
        print "  " + testPosExample["filename"] + " " + str(logreg.predict(testPosExample["image"])[0])
    
    print "Negative tests (should be 0.0):"
    for testNegExample in testNegExamples:
        print "  " + testNegExample["filename"] + " " + str(logreg.predict(testNegExample["image"])[0])

# read the training data
for dirname in (trainingCancerDir, trainingBloodDir):
    for filename in os.listdir(dirname):
        p = readImage(dirname+filename)
        if p.size > 0:
            # add the vector to our list of training data
            trainingImageList.append(p)
    
    # store the number of positive samples we've got ready for later
    if dirname == trainingCancerDir:
        numPosSamples = len(trainingImageList)


# convert training data into numpy array
X = np.array(trainingImageList)

# generate labels
y = getY(X.shape[0],numPosSamples)

print "X = " + str(X.shape[0]) + " x " + str(X.shape[1]) + " with " + str(len(y)) + " labels"

# train the model
logreg = linear_model.LogisticRegression()
logreg.fit(X, y)

print "Training complete"

runTestData()