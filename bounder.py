#!/usr/bin/python

import sys
import time
import matplotlib.pyplot as plt
import numpy

__author__ = "Matan Lachmish and Asaf Rokach"
__copyright__ = "Copyright 2016, Bounding TSO"
__version__ = "1.2"
__status__ = "Development"

kNumberOfTests = 10000
kNumberOfWritesPerTests = 2 ** 10
MeasureMethod = 'fine'  # 'fine'/'coarse'


def main(argv):
    printWelcomePrompt()

    if MeasureMethod == 'fine':
        # Fine Grained
        print('Calculating TSO size (Fine Grained)...')
        fineGrainedIntervals = calculateTSOSizeFineGrained()

        saveResults(fineGrainedIntervals, 'fine')

        print('Plotting Fine Grained results')
        plt.plot(fineGrainedIntervals)
        plt.title('Fine Grained results')
        plt.ylabel('Process Time')
        plt.xlabel('# Bytes Written')
        plt.show()

    elif MeasureMethod == 'coarse':
        # Coarse Grained
        print('Calculating TSO size (CoarseGrained)...')
        sizeArray, meanTime = calculateTSOSizeCoarseGrained()
        linearPlot = numpy.poly1d(numpy.polyfit(sizeArray, meanTime, 1))(sizeArray)
        stepsPlot = [1 if x > linearPlot[i] else 0 for i, x in enumerate(meanTime)]

        saveResults(meanTime, 'coarse')

        print('Plotting Coarse Grained results')
        plt.plot(sizeArray, meanTime)
        plt.plot(sizeArray, linearPlot)
        plt.plot(sizeArray, stepsPlot)
        plt.title('Coarse Grained results')
        plt.ylabel('Process Time')
        plt.xlabel('# Bytes Written')
        plt.show()

    else:
        print('Unsupported MeasureMethod')


def floodTSO():
    meanWriteTime = 0.0
    for test in range(1, kNumberOfTests):
        storage = bytearray()  # New empty byte array
        for byteNumber in range(1, kNumberOfWritesPerTests):
            startTime = time.process_time()
            storage.extend(b"x")
            currentTime = time.process_time()
            currentWriteTime = currentTime - startTime
            if currentWriteTime >= meanWriteTime * 1.8 and byteNumber > 1:  # Check if current write time pass the threshold (1.8)
                print("Flooded at byte number: " + str(byteNumber))
                return True
            else:
                meanWriteTime = ((meanWriteTime * (byteNumber - 1)) + currentWriteTime) / byteNumber
    return False


def calculateTSOSizeCoarseGrained():
    sizeArray = list(range(1, kNumberOfWritesPerTests))
    meanTimeArray = []

    for size in sizeArray:

        # Flood TSO
        if not floodTSO():
            print("Flooding the TSO failed!")
            return

        startTime = time.process_time()
        for k in range(1, kNumberOfTests):
            storage = bytearray()  # New empty byte array
            for i in range(1, size):
                # x = b"x"  # Stub write
                storage.extend(b"x")
        stopTime = time.process_time()
        meanTimeArray.append((stopTime - startTime) / kNumberOfTests)

    return sizeArray, meanTimeArray


def calculateTSOSizeFineGrained():
    loggers = []

    for test in range(1, kNumberOfTests):
        storage = bytearray()  # New empty byte array

        # Flood TSO
        if not floodTSO():
            print("Flooding the TSO failed!")
            return

        timeLogger = [time.process_time()]
        for byteNumber in range(1, kNumberOfWritesPerTests):
            storage.extend(b"x")
            # x = b"x"  # Stub write
            timeLogger.append(time.process_time())
        loggers.append(timeLogger)

    intervals = []
    for logger in loggers:
        timeIntervals = []
        for counter in range(1, len(logger) - 1):
            timeIntervals.append(logger[counter + 1] - logger[counter])
        intervals.append(timeIntervals)

    avgIntervals = [float(sum(col)) / len(col) for col in zip(*intervals)]

    return avgIntervals


def saveResults(results, filename):
    with open(filename + "_results.csv", 'w') as myfile:
        for value in results:
            myfile.write(str(value)+',')


def printCurrentTime():
    currentTime = time.process_time()
    print('Current time is: ' + str(currentTime))


def printWelcomePrompt():
    print('')
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('         ~~~ Welcome to TSO Bounder ~~~')
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('')


if __name__ == "__main__":
    main(sys.argv)
