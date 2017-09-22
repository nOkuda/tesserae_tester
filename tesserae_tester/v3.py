"""v3 Tesserae queries

The functions in this file keep track of how to execute queries and parse
results on v3 Tesserae.
"""
import os
import subprocess
import uuid

import tesserae_tester as tess


SEARCH_BINS = {
    'vanilla': 'read_table.pl'
    }


def get_query_results(v3path, query):
    """Executes query in V3 and return results"""
    v3bin = os.path.join(v3path, 'cgi-bin')
    v3search = os.path.join(v3bin, SEARCH_BINS[query.searchtype])
    results_dir = '/tmp/'+'tess'+str(uuid.uuid4())
    subprocess.run([
        v3search,
        '--target', query.targettext,
        '--source', query.sourcetext,
        '--unit', query.unit,
        '--feature', query.feature,
        '--freq_basis', query.freq_basis,
        '--score', query.score,
        '--stop', query.stop,
        '--stbasis', query.stbasis,
        '--dist', query.dist,
        '--dibasis', query.dibasis,
        '--cutoff', query.cutoff,
        '--binary', results_dir], check=True)
    v3result = os.path.join(v3bin, 'read_bin.pl')
    results_file = '/tmp/'+'tess'+str(uuid.uuid4())
    with open(results_file, 'w') as ofh:
        subprocess.run([
            v3result,
            results_dir,
            '--export', 'tab'], stdout=ofh)
    # subprocess.run(['rm', '-rf', results_dir])
    result = tess.data.TesseraeResults('v3query')
    with open(results_file) as ifh:
        _advance_fh(ifh)
        for line in ifh:
            source_words, target_words, shared_words, score = _parse_line(line)
            result.container[(source_words, target_words)] = \
                (shared_words, score)
    return result


def _advance_fh(fh):
    """Advances file handle past non-results lines"""
    for line in fh:
        if line.startswith("RESULT"):
            break


def _parse_line(line):
    """Extracts match information of tab delimited V3 results

    return value :: (source words, target words, shared words, score)
    """
    entries = line.strip().split('\t')
    return (
        _clean_words(entries[4]),
        _clean_words(entries[2]),
        entries[-2],
        float(entries[-1]))


def _clean_words(words):
    return words.replace('*', '')
