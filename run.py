"""Run comparison tests against configured Tesserae versions"""
import argparse
import json

import tesserae_tester as tess


def _parse_args():
    """Parses arguments"""
    parser = argparse.ArgumentParser(
        description='Run Tesserae version comparison tests')
    parser.add_argument(
        'config',
        help='Configuration file for comparison tests')
    return parser.parse_args()


def compare(r1, r2):
    """Compares results"""
    if len(r1) != len(r2):
        print('****Results do not have same number of matches')
        return
    mismatches = []
    for m1, m2 in zip(r1, r2):
        if m1 != m2:
            mismatches.append((m1, m2))
    if mismatches:
        print('####Mismatches found')
        for mm in mismatches:
            print(mm[0])
            print(mm[1])


def _run(args):
    """Runs tests"""
    with open(args.config) as ifh:
        config = json.load(ifh)
    query = tess.data.TesseraeQuery(
        'vanilla', 'ovid.ars_amatoria', 'martial.epigrams')
    v3results = tess.v3.get_query_results(config['v3path'], query)
    otherresults = tess.v3.get_query_results(config['v3path'], query)
    compare(v3results, otherresults)


if __name__ == '__main__':
    _run(_parse_args())
