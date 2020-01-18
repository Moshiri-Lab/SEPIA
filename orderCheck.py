#!/usr/bin/env python3
"""
File implements several methods used in compute_efficiency.py and compute_taub.py
"""
from gzip import open as gopen
from sys import stderr
import scipy
import scipy.stats as stats # run 'pip install scipy' in your terminal


def pairCounts(transmissionHist, lowerBound: int, upperBound: int, metric: int) -> dict:
        """
        Pairs each individual with a count value, where a higher count value indicates
        that an individual has a higher priority. Count values are calculated based
        on the corresponding chosen metric.

        There are currently four metrics to choose from:
        Metric 1 - 
        Metric 2 - 
        Metric 3 -
        Metric 4 -
        Metric 5 -

        Returns a dictionary where each key is an individual and their value
        is their corresponding count.

        Parameters
        ----------
        tranmissionHist - the file object with data on tranmissions used to build the
                                          dictionary
        lowerBound - lower bound of years range
        upperBound - upper bound of years range
        metric - int, specifies the chosen metric
        """

        # call the function corresponding to the chosen metric
        if (metric == 1):
            return directTransmissions(transmissionHist, lowerBound, upperBound)
        elif (metric == 2):
            return bestfitGraph(transmissionHist, lowerBound, upperBound)
        elif (metric == 3):
            return indirectTransmissions(transmissionHist, lowerBound, upperBound)
        elif (metric == 4):
            return totalTransmissions(transmissionHist, lowerBound, upperBound)
        elif (metric == 5):
            return numContacts(transmissionHist, lowerBound, upperBound)


def directTransmissions(transmissionHist, lowerBound: int, upperBound: int) -> dict:
        """
        Counts the number of times each individual infected someone else in a file.

        Returns a dictionary where each key is an individual and their value
        is their corresponding infection count.

        Parameters
        ----------
        tranmissionHist - the file object with data on tranmissions used to build the
                                          dictionary
        lowerBound - lower bound of years range
        upperBound - upper bound of years range
        """

        infectedPersons= []
        people = []
        numInfected = dict()
        if isinstance(transmissionHist,str):
            if transmissionHist.lower().endswith('.gz'):
                lines = [l.strip() for l in gopen(transmissionHist,'rb').read().decode().strip().splitlines()]
            else:
                lines = [l.strip() for l in open(transmissionHist).read().strip().splitlines()]
        else:
            lines = [l.strip() for l in transmissionHist.read().strip().splitlines()]

        # Loop over each line in the file.
        for line in lines:
            u,v,t = line.split('\t')
            u = u.strip()
            v = v.strip()

            # Only considers infections within a given range of years
            if (lowerBound > float(t)) | (float(t) > upperBound):
                continue

            if u == 'None':
                continue

            if u not in numInfected:
                numInfected[u] = 0

            numInfected[u] += 1

        """
        # Print the output of all individuals, unsorted
        for u in numInfected:
                print("%s\t%d" % (u, numInfected[u]))
        """

        return numInfected


def bestfitGraph(transmissionHist, lowerBound: int, upperBound: int) -> dict:
        """
        TODO metric 2 - Titan

        Returns a dictionary where each key is an individual and their value
        is their corresponding indirect infection count.

        Parameters
        ----------
        tranmissionHist - the file object with data on tranmissions used to build the
                                          dictionary
        lowerBound - lower bound of years range
        upperBound - upper bound of years range
        """

        infectedPersons= []
        people = []
        numInfected = dict()
        if isinstance(transmissionHist,str):
            if transmissionHist.lower().endswith('.gz'):
                lines = [l.strip() for l in gopen(transmissionHist,'rb').read().decode().strip().splitlines()]
            else:
                lines = [l.strip() for l in open(transmissionHist).read().strip().splitlines()]
        else:
            lines = [l.strip() for l in transmissionHist.read().strip().splitlines()]

        # Loop over each line in the file.
        for line in lines:
            u,v,t = line.split('\t')
            u = u.strip()
            v = v.strip()

            # Only considers infections within a given range of years
            if (lowerBound > float(t)) | (float(t) > upperBound):
                continue

            if u == 'None':
                continue

            if u not in numInfected:
                numInfected[u] = 0

            numInfected[u] += 1

        return numInfected


def indirectTransmissions(transmissionHist, lowerBound: int, upperBound: int) -> dict:
        """
        Returns a dictionary where each key is an individual and their value
        is their corresponding indirect infection count.

        Parameters
        ----------
        tranmissionHist - the file object with data on tranmissions used to build the
                                          dictionary
        lowerBound - lower bound of years range
        upperBound - upper bound of years range
        """

        infectedPersons= []
        people = []
        numInfected = dict()
        if isinstance(transmissionHist,str):
            if transmissionHist.lower().endswith('.gz'):
                lines = [l.strip() for l in gopen(transmissionHist,'rb').read().decode().strip().splitlines()]
            else:
                lines = [l.strip() for l in open(transmissionHist).read().strip().splitlines()]
        else:
            lines = [l.strip() for l in transmissionHist.read().strip().splitlines()]

        # Loop over each line in the file.
        for line in lines:
            u,v,t = line.split('\t')
            u = u.strip()
            v = v.strip()

            # Only considers infections within a given range of years
            if (lowerBound > float(t)) | (float(t) > upperBound):
                continue

            if u == 'None':
                continue

            if u not in numInfected:
                numInfected[u] = 0

            numInfected[u] += 1

        numIndirect = dict()
        for line in lines:
            u,v,t = line.split('\t')
            u = u.strip()
            v = v.strip()

            # Only considers infections within a given range of years
            if (lowerBound > float(t)) | (float(t) > upperBound):
                continue

            if u == 'None':
                continue

            if u not in numIndirect:
                numIndirect[u] = 0

            # should get the number of people that were indirected impacted
            if v in numInfected:
                numIndirect[u] += numInfected.get(v)

        return numIndirect


def totalTransmissions(transmissionHist, lowerBound: int, upperBound: int) -> dict:
        """
        Returns a dictionary where each key is an individual and their value
        is their corresponding indirect infection count.

        Parameters
        ----------
        tranmissionHist - the file object with data on tranmissions used to build the
                                          dictionary
        lowerBound - lower bound of years range
        upperBound - upper bound of years range
        """

        infectedPersons= []
        people = []
        numInfected = dict()
        if isinstance(transmissionHist,str):
            if transmissionHist.lower().endswith('.gz'):
                lines = [l.strip() for l in gopen(transmissionHist,'rb').read().decode().strip().splitlines()]
            else:
                lines = [l.strip() for l in open(transmissionHist).read().strip().splitlines()]
        else:
            lines = [l.strip() for l in transmissionHist.read().strip().splitlines()]

        # Loop over each line in the file.
        for line in lines:
            u,v,t = line.split('\t')
            u = u.strip()
            v = v.strip()

            # Only considers infections within a given range of years
            if (lowerBound > float(t)) | (float(t) > upperBound):
                continue

            if u == 'None':
                continue

            if u not in numInfected:
                numInfected[u] = 0

            numInfected[u] += 1


        numIndirect = dict()
        for line in lines:
            u,v,t = line.split('\t')
            u = u.strip()
            v = v.strip()

            # Only considers infections within a given range of years
            if (lowerBound > float(t)) | (float(t) > upperBound):
                continue

            if u == 'None':
                continue

            if u not in numIndirect:
                numIndirect[u] = 0

            # should get the number of people that were indirected impacted
            if v in numInfected:
                numIndirect[u] += numInfected.get(v)

        numTotal = dict()

        # go through loop
        for person in numInfected:

            if person not in numTotal:
                numTotal[person] = 0

            if person in numInfected:
                numTotal[person] += numInfected[person]
            if person in numIndirect:
                numIndirect[person]

        return numTotal

def numContacts(transmissionHist, lowerBound: int, upperBound: int) -> dict: 
        """
        Counts the number of connections an individual has.

        Returns a dictionary where each key is an individual and their value
        is their corresponding number of contacts in the file.

        Parameters
        ----------
        transmissionHist - the file object with data on transmissions used to
        build the dictionary.
        lowerBound - Ignored for contact networks
        upperBound - Ignored for contact networks
        """

        infectedPersons= []
        people = []
        numberContacts = dict()
        if isinstance(transmissionHist,str):
            if transmissionHist.lower().endswith('.gz'):
                lines = [l.strip() for l in gopen(transmissionHist,'rb').read().decode().strip().splitlines()]
            else:
                lines = [l.strip() for l in open(transmissionHist).read().strip().splitlines()]
        else:
            lines = [l.strip() for l in transmissionHist.read().strip().splitlines()]

        # Loop over each line in the file.
        for line in lines:
            # Skip over lines listing the nodes
            if(line[0:4] == 'NODE'):
                    continue

            u,v,t,w,x = line.split('\t')
            u = u.strip()
            v = v.strip()
            
            if u == 'None':
                continue
            
            if v not in numberContacts:
                numberContacts[v] = 0

            numberContacts[v] += 1
        
        return numberContacts

def matchInfectorCounts(infectionsDict: dict, inputOrder, outfile) -> None:
        """
        Matches the infectors in a user inputted file to their corresponding
        infection count. Returns void.

        Outputs lines with the format: "<individual> <count>",
        maintaing the original order of individuals in input.

        Parameters
        ----------
        infectionsDict - a dict with keys as infectors and values as
                                         their infection counts
        infile - a file with the user's ordering of individuals
        outfile - a file where each line of output is written
        """

        for line in inputOrder:

                p = line.strip()

                if p not in infectionsDict.keys():
                        outfile.write("%s\t0\n" % p)

                else:
                        outfile.write("%s\t%d\n" % (p, infectionsDict[p]))


def calculateTauB(userOrder, outfile, reverse: bool) -> None:
        """
        Calculates the Kendall Tau B correlation coefficient between user ordering
        and most optimal ordering, assuming that the counts of individuals in
        infile sorted is the most optimal.
        Outputs coefficient and pvalue in the following format: "<tau> <pvalue>".
        Returns void.

        Parameters
        ----------
        userOrder- an ordering of infectors and their counts 
                   - generated by the user's algorithm
        outfile - the file the tau and pvalue are outputted
        reverse - bool, true if user's ordering is compared to order sorted descending,
                                        false if comparing to order sorted ascending
        """
        optimalOrder = []
        for i in range(len(userOrder)):
            optimalOrder.append(i)

        tau, pvalue = stats.kendalltau([e[0] for e in optimalOrder], [e[0] for e in userOrder])

        outfile.write("%s\t%s\n" % (tau, pvalue))

