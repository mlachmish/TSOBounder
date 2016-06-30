#!/usr/bin/python

import sys
import time
import matplotlib.pyplot as plt

__author__ = "Matan Lachmish and Asaf Rokach"
__copyright__ = "Copyright 2016, Bounding TSO"
__version__ = "1.2"
__status__ = "Development"

kNumberOfTests = 100000
kNumberOfWritesPerTests = 2 ** 10
MeasureMethod = 'coarse'  # 'fine'/'coarse'


def main(argv):
    printWelcomePrompt()

    if MeasureMethod == 'fine':
        # Fine Grained
        print('Calculating TSO size (Fine Grained)...')
        fineGrainedIntervals = calculateTSOSizeFineGrained()

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

        print('Plotting Coarse Grained results')
        plt.plot(sizeArray, meanTime)
        plt.title('Coarse Grained results')
        plt.ylabel('Process Time')
        plt.xlabel('# Bytes Written')
        plt.show()

    else:
        print('Unsupported MeasureMethod')


def calculateTSOSizeCoarseGrained():
    sizeArray = list(range(1,kNumberOfWritesPerTests))
    meanTimeArray = []

    for size in sizeArray:
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

    for test in range(1,kNumberOfTests):
        storage = bytearray()  # New empty byte array
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
