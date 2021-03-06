"""Run comparison tests against configured Tesserae versions"""
import argparse
import json
import os
import urllib.request as request

import tesserae_tester as tess


def _parse_args():
    """Parses arguments"""
    parser = argparse.ArgumentParser(
        description='Run Tesserae version comparison tests')
    parser.add_argument(
        'config',
        help='Configuration file for comparison tests')
    parser.add_argument(
        'outdir',
        help='Directory where output will be placed')
    return parser.parse_args()


def _report_setdiff(pairs, same_pairs, container, outdir, version, label):
    """If there are items in the set difference, notifies user and dumps"""
    diff = pairs.difference(same_pairs)
    if diff:
        print('****{0} has unshared matches'.format(version))
    with open(os.path.join(outdir, label+'.'+version+'.out'), 'w') as ofh:
        for item in diff:
            ofh.write(str(item))
            ofh.write('\n\t')
            ofh.write(str(container[item]))
            ofh.write('\n')


def compare(r1, r2, label, outdir):
    """Compares results

        * r1, r2 :: TesseraeResults

    The score returned is the sum of the differences of scores between the same
    match pair.
    """
    with open(os.path.join(outdir, label+'.results'), 'w') as ofh:
        r1_stop = {s for s in r1.stopwords}
        r2_stop = {s for s in r2.stopwords}
        same_stop = r1_stop.intersection(r2_stop)
        if len(same_stop) != len(r1_stop):
            ofh.write('****Stopword lists do not match (')
            ofh.write(str(len(r1.stopwords)) + ') (')
            ofh.write(str(len(r2.stopwords)) + ')\n')
            for r1s, r2s in zip(sorted(r1.stopwords), sorted(r2.stopwords)):
                ofh.write('\t'+r1s+'\t'+r2s+'\n')
        if len(r1.container) != len(r2.container):
            ofh.write('****Results do not have same number of matches\n')
            ofh.write(str(len(r1.container))+' '+str(len(r2.container))+'\n')
        r1_pairs = {k for k in r1.container}
        r2_pairs = {k for k in r2.container}
        same_pairs = r1_pairs.intersection(r2_pairs)
        ofh.write('####Number of matching matches '+str(len(same_pairs))+'\n')
        _report_setdiff(
            r1_pairs, same_pairs, r1.container, outdir, r1.version, label)
        _report_setdiff(
            r2_pairs, same_pairs, r2.container, outdir, r2.version, label)
    total_diff = 0.0
    mismatches = []
    for pair in same_pairs:
        diff = abs(r1.container[pair].score - r2.container[pair].score)
        if diff:
            mismatches.append((diff, pair, r1.container[pair],
                r2.container[pair]))
            total_diff += diff
    if mismatches:
        mismatches.sort()
        with open(os.path.join(outdir, label+'.mismatches.out'), 'w') as ofh:
            for mm in mismatches:
                ofh.write(str(mm))
                ofh.write('\n')
            ofh.write('####Total difference: '+str(total_diff)+'\n')
        print('####Total difference: ', total_diff)
    return total_diff


def _get_queries():
    """Gets queries to test"""
    result = {
        'freqbasis': tess.data.TesseraeQuery(
            'vanilla', 'ovid.ars_amatoria', 'martial.epigrams'),
        }
    result['freqbasis'].freq_basis = 'corpus'
    return result

def _get_all_queries():
    """Gets queries to test"""
    result = {
        'vanilla': tess.data.TesseraeQuery(
            'vanilla', 'ovid.ars_amatoria', 'martial.epigrams'),
        'phrase': tess.data.TesseraeQuery(
            'vanilla', 'ovid.ars_amatoria', 'martial.epigrams'),
        'stopsize': tess.data.TesseraeQuery(
            'vanilla', 'ovid.ars_amatoria', 'martial.epigrams'),
        'cutoff': tess.data.TesseraeQuery(
            'vanilla', 'ovid.ars_amatoria', 'martial.epigrams'),
        'dist': tess.data.TesseraeQuery(
            'vanilla', 'ovid.ars_amatoria', 'martial.epigrams'),
        'dibasis_span': tess.data.TesseraeQuery(
            'vanilla', 'ovid.ars_amatoria', 'martial.epigrams'),
        'dibasis_span_target': tess.data.TesseraeQuery(
            'vanilla', 'ovid.ars_amatoria', 'martial.epigrams'),
        'dibasis_span_source': tess.data.TesseraeQuery(
            'vanilla', 'ovid.ars_amatoria', 'martial.epigrams'),
        'dibasis_freq_target': tess.data.TesseraeQuery(
            'vanilla', 'ovid.ars_amatoria', 'martial.epigrams'),
        'dibasis_freq_source': tess.data.TesseraeQuery(
            'vanilla', 'ovid.ars_amatoria', 'martial.epigrams'),
        'stbasis_source': tess.data.TesseraeQuery(
            'vanilla', 'ovid.ars_amatoria', 'martial.epigrams'),
        'stbasis_target': tess.data.TesseraeQuery(
            'vanilla', 'ovid.ars_amatoria', 'martial.epigrams'),
        'stbasis_both': tess.data.TesseraeQuery(
            'vanilla', 'ovid.ars_amatoria', 'martial.epigrams'),
        'freqbasis': tess.data.TesseraeQuery(
            'vanilla', 'ovid.ars_amatoria', 'martial.epigrams'),
        }
    result['phrase'].unit = 'phrase'
    result['stopsize'].stop = '50'
    result['cutoff'].cutoff = '8.1'
    result['dist'].dist = '5'
    result['dibasis_span'].dibasis = 'span'
    result['dibasis_span_target'].dibasis = 'span_target'
    result['dibasis_span_source'].dibasis = 'span_source'
    result['dibasis_freq_target'].dibasis = 'freq_target'
    result['dibasis_freq_source'].dibasis = 'freq_source'
    result['stbasis_source'].stbasis = 'source'
    result['stbasis_target'].stbasis = 'target'
    result['stbasis_both'].stbasis = 'both'
    result['freqbasis'].freq_basis = 'corpus'
    return result


def _run(args):
    """Runs tests"""
    with open(args.config) as ifh:
        config = json.load(ifh)
    try:
        request.urlopen(config['v4path'])
    except:
        print('Cannot connect to v4')
        return
    queries = _get_queries()
    os.makedirs(args.outdir, exist_ok=True)
    for label, query in queries.items():
        v3results = tess.v3.get_query_results(config['v3path'], query)
        otherresults = tess.v4.get_query_results(config['v4path'], query)
        compare(v3results, otherresults, label, args.outdir)


if __name__ == '__main__':
    _run(_parse_args())
