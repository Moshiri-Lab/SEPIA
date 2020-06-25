#!/usr/bin/env python3
"""
File implements a script where the user can calculate the Kendall Tau B correlation coefficient
between their ordering and most optimal ordering, assuming that the counts of individuals in
inputted file sorted is the most optimal.
"""

import scipy.stats as stats 
import math


def calculateTauB(userOrder, outfile, reverse: bool) -> None:
        """
        Calculates the Kendall Tau B correlation coefficient between user ordering
        and most optimal ordering, assuming that the an ascending count starting
        from 0 is the most optimal.
        (ex: for an ordering containing 3 people, the optimal ordering would be [0,1,2])

        Outputs coefficient and pvalue in the following format: "<tau> <pvalue>".
        Returns void.

        Parameters
        ----------
        userOrder- an ordering of infectors and their counts
                   - generated by the user's algorithm
        outfile - the file the tau and pvalue are outputted
        reverse - bool, true if user's ordering is compared to an order sorted descending,
                                        false if comparing to an order sorted ascending
        """

        optimalOrder = []

        if not reverse:
            optimalOrder = list(range(len(userOrder), 0, -1))
        else:
            optimalOrder = list(range(len(userOrder)))

        tau, pvalue = stats.kendalltau(optimalOrder, userOrder)

        outfile.write("%s\t%s\n" % (tau, pvalue))


if __name__ == "__main__":
    # parse user arguments [-h] [-i INPUT] [-o OUTPUT] [-r]
    import argparse
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', required=False, type=str, default='stdin', help="Input File - User's Ordering")
    parser.add_argument('-o', '--output', required=False, type=str, default='stdout', help="Output File")
    parser.add_argument('-r', '--reverse', action='store_true', help='Sort in Ascending Order')

    args = parser.parse_args()

    # handle input and and output, save into infile and outfile vars
    if args.input == 'stdin':
        from sys import stdin; efficacy = [[v.strip() for v in l.strip().split('\t')] for l in stdin.read().strip().splitlines()]
    elif args.input.lower().endswith('.gz'):
        from gzip import open as gopen; efficacy = [[v.strip() for v in l.strip().split('\t')] for l in gopen(args.input).read().decode().strip().splitlines()]
    else:
        efficacy = [[v.strip() for v in l.strip().split('\t')] for l in open(args.input).read().strip().splitlines()]
    if args.output == 'stdout':
        from sys import stdout; outfile = stdout
    else:
        outfile = open(args.output,'w')

    # Iterate over all the lines for efficacy
    for i in range(len(efficacy)):
        if len(efficacy[i]) != 2:
            raise ValueError("Input must be efficacy file as generated by ./compute_efficacy (TSV with 2 columns: PERSON<TAB>EFFICACY", efficacy)
        efficacy[i] = float(efficacy[i][1])

    ascendingSort = False
    # user wants to compare their ordering theirs sorted in ascending order
    if args.reverse:
        ascendingSort = True

    calculateTauB(efficacy, outfile, ascendingSort)
    outfile.close()
