"""Run comparison tests against configured Tesserae versions"""
import argparse
import json
import urllib.request as request

import tesserae_tester as tess


def _parse_args():
    """Parses arguments"""
    parser = argparse.ArgumentParser(
        description='Run Tesserae version comparison tests')
    parser.add_argument(
        'config',
        help='Configuration file for comparison tests')
    return parser.parse_args()


def _report_setdiff(pairs, same_pairs, label):
    """If there are items in the set difference, notifies user and dumps"""
    diff = pairs.difference(same_pairs)
    if diff:
        print('****{0} has extra stuff'.format(label))
        with open(label+'.txt', 'w') as ofh:
            for item in diff:
                ofh.write(str(item))
                ofh.write('\n')


def compare(r1, r2):
    """Compares results

        * r1, r2 :: TesseraeResults

    The score returned is the sum of the differences of scores between the same
    match pair.
    """
    if len(r1.container) != len(r2.container):
        print('****Results do not have same number of matches')
        print(len(r1.container), len(r2.container))
    r1_pairs = {k for k in r1.container}
    r2_pairs = {k for k in r2.container}
    same_pairs = r1_pairs.intersection(r2_pairs)
    _report_setdiff(r1_pairs, same_pairs, r1.label)
    _report_setdiff(r2_pairs, same_pairs, r2.label)
    total_diff = 0.0
    mismatches = []
    for pair in same_pairs:
        diff = abs(r1.container[pair][1] - r2.container[pair][1])
        if diff:
            mismatches.append((diff, pair))
            total_diff += diff
    if mismatches:
        mismatches.sort()
        print('####Mismatches found')
        for mm in mismatches:
            print(mm)
    print('####Total difference: ', total_diff)


def _run(args):
    """Runs tests"""
    with open(args.config) as ifh:
        config = json.load(ifh)
    try:
        check = request.urlopen(config['v4path'])
        print(check.getcode())
    except:
        print('Cannot connect to v4')
        return
    query = tess.data.TesseraeQuery(
        'vanilla', 'ovid.ars_amatoria', 'martial.epigrams')
    v3results = tess.v3.get_query_results(config['v3path'], query)
    otherresults = tess.v4.get_query_results(config['v4path'], query)
    compare(v3results, otherresults)


if __name__ == '__main__':
    _run(_parse_args())
