#!/usr/bin/python -W ignore
from PIL import Image
import numpy as np
import os
from sklearn import linear_model

trainingCancerDir = "../images/extract-automatic/cancer/"
trainingBloodDir = "../images/extract-automatic/blood/"
trainingOtherDir = "../images/extract-automatic/other/"
testCancerDir = "../images/extract-automatic/cancer-test/"
testBloodDir = "../images/extract-automatic/blood-test/"
testOtherDir = "../images/extract-automatic/other-test/"

def getY(numCancerSamples, numBloodSamples, numOtherSamples):
    '''Returns a numpy array of Y values'''
    cancerArray = np.ones(numCancerSamples)
    bloodArray = np.zeros(numBloodSamples)
    otherArray = np.full(numOtherSamples, 2)
    return np.concatenate((cancerArray,bloodArray,otherArray))

def readImage(path):
    # look at the jpegs
    if path.endswith(".jpg"):
        
        # open each image (max size is known to be 30x30)
        image = Image.open(path)

        # grab the pixel values into a 2d numpy array
        pixels = np.array(image)
        
        # reshape the 2d array into a 1d vector of RGB values
        r = pixels[:,:,0].reshape(-1)
        g = pixels[:,:,1].reshape(-1)
        b = pixels[:,:,2].reshape(-1)
        
        if len(r) < 900:
            rgbfill = np.full(900-len(r), -1)
            r = np.append(r, rgbfill)
            g = np.append(g, rgbfill)
            b = np.append(b, rgbfill) 
        
        return np.concatenate((r,g,b))
    
    return np.array([0,0])

def getTrainingData():
    trainingImageList = []
    
    numCancerSamples = 0
    numBloodSamples = 0
    numOtherSamples = 0
    
    # read the training data
    for dirname in (trainingCancerDir, trainingBloodDir, trainingOtherDir):
        for filename in os.listdir(dirname):
            p = readImage(dirname+filename)
            if p.size > 0:
                # add the vector to our list of training data
                trainingImageList.append(p)
        
                # store the number of positive samples we've got ready for later
                if dirname == trainingCancerDir:
                    numCancerSamples += 1
                
                # store the number of positive samples we've got ready for later
                if dirname == trainingBloodDir:
                    numBloodSamples += 1
                    
                # store the number of positive samples we've got ready for later
                if dirname == trainingOtherDir:
                    numOtherSamples += 1
    
    
    # convert training data into numpy array
    X = np.array(trainingImageList)
    
    # generate labels
    y = getY(numCancerSamples,numBloodSamples,numOtherSamples)
    
    return (X, y)

def runTestData():
    testCancerExamples = []
    testBloodExamples = []
    testOtherExamples = []
    
    for filename in os.listdir(testCancerDir):
        p = readImage(testCancerDir+filename)
        if p.size > 0:
            testCancerExamples.append({"image":p,"filename":filename});

    for filename in os.listdir(testBloodDir):
        p = readImage(testBloodDir+filename)
        if p.size > 0:
            testBloodExamples.append({"image":p,"filename":filename})
    
    for filename in os.listdir(testOtherDir):
        p = readImage(testOtherDir+filename)
        if p.size > 0:
            testOtherExamples.append({"image":p,"filename":filename})
    
    print "Test cancer cells (should be 1.0):"
    correct = 0
    wrong = 0
    for testCancerExample in testCancerExamples:
        prediction = logreg.predict(testCancerExample["image"])[0]
        if prediction == 1.0:
            correct += 1
        else:
            wrong += 1
        print "  " + testCancerExample["filename"] + " " + str(prediction)
    print correct, "correct,", wrong, "wrong,", "Accuracy =", str(correct*100.0/(correct+wrong))
    
    print "Test blood cells (should be 0.0):"
    correct = 0
    wrong = 0
    for testBloodExample in testBloodExamples:
        prediction = logreg.predict(testBloodExample["image"])[0]
        if prediction == 0.0:
            correct += 1
        else:
            wrong += 1
        print "  " + testBloodExample["filename"] + " " + str(prediction)
    print correct, "correct,", wrong, "wrong,", "Accuracy =", str(correct*100.0/(correct+wrong))
    
    print "Test other cells (should be 2.0):"
    correct = 0
    wrong = 0
    for testOtherExample in testOtherExamples:
        prediction = logreg.predict(testOtherExample["image"])[0]
        if prediction == 2.0:
            correct += 1
        else:
            wrong += 1
        print "  " + testOtherExample["filename"] + " " + str(prediction)
    print correct, "correct,", wrong, "wrong,", "Accuracy =", str(correct*100.0/(correct+wrong))

if __name__ == "__main__":

    X, y = getTrainingData()
    
    print "X = " + str(X.shape[0]) + " x " + str(X.shape[1]) + " with " + str(len(y)) + " labels"
    
    # train the model
    logreg = linear_model.LogisticRegression()
    logreg.fit(X, y)
    
    print "Training complete"
    
    runTestData()