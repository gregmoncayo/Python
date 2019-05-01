import random
import csv
import math

def loadCSV(filename):
    lines = csv.reader(open(filename,"rb"))
    dataset = list(lines)
    for i in range(len(dataset)):
        dataset[i] = [float(x) for x in dataset[i]]
    return dataset

def splitDataset(dataset, splitratio):
    training = int(len(dataset)*splitratio)
    train = []
    copy = list(dataset)
    while len(train) < training:
        index = random.randrange(len(copy))
        train.append(copy.pop(index))

    return [train,copy]

def separateByClass(dataset):
    separated = {}
    for i in range(len(dataset)):
        vector = dataset[i]
        if(vector[0] not in separated):
            separated[vector[0]]=[]
        separated[vector[0]].append(vector)

    return separated

def mean(numbers):
    return sum(numbers)/float(len(numbers))

def stddev(numbers):
    avg = mean(numbers)
    variance = sum([pow(x-avg,2) for x in numbers])/float(len(numbers))
    if (variance == 0):
	variance = 1
    return math.sqrt(variance)

def calculateProbability(x,mean,stddev):
    exponent = math.exp(-(math.pow(x-mean,2)/(2*math.pow(stddev,2))))
    return (1/(math.sqrt(2*math.pi)*stddev))*exponent


def summarize(dataset):
    summaries = [(mean(attribute),stddev(attribute)) for attribute in zip(*dataset)]
    return summaries

def summarizeByClass(dataset):
    separated = separateByClass(dataset)
    summaries = {}
    for classVal, instance in separated.iteritems():
        summaries[classVal] = summarize(instance)

    return summaries

def calculateClassProbability(summaries,inputVector):
    probabilities = {}
    for classVal, classSum in summaries.iteritems():
        probabilities[classVal] = 1
        for i in range(len(classSum)):
            mean, stddev = classSum[i]
            x = inputVector[i]
	    if (stddev == 0):
		stddev = 1
            probabilities[classVal]*=calculateProbability(x,mean,stddev)

    return probabilities

def predict(summaries, inputVector):
    probabilities = calculateClassProbability(summaries,inputVector)
    bestLabel, bestProb = None,-1
    for classVal, probability in probabilities.iteritems():
        if bestLabel is None or probability > bestProb:
            bestProb = probability
            bestLabel = classVal
    return bestLabel


def getPredictions(summaries, testSet):
    predictions = []
    for i in range(len(testSet)):
        result = predict(summaries,testSet[i])
        predictions.append(result)

    return predictions

def getAccuracy(testSet,predictions):
    correct = 0
    for i in range(len(testSet)):
        if testSet[i][0] == predictions[i]:
            correct+=1

    return (correct/float(len(testSet)))*100.0

def main():
    filename = 'wine.csv'
    splitRatio = 0.7
    dataset=loadCSV(filename)
    trainingSet, testSet = splitDataset(dataset, splitRatio)

    summaries = summarizeByClass(trainingSet)

    predictions = getPredictions(summaries,testSet)
    accuracy = getAccuracy(testSet,predictions)

    print(accuracy)

main()

