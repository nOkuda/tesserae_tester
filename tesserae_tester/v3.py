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
    return TesseraeResults(results_file)


class TesseraeResults(object):
    """Holder class for V3 Tesserae results"""

    def __init__(self, in_data):
        """in_data is the filepath to the V3 results"""
        self.results_path = in_data
        self.fh = None
        self.len = 0
        tmp = self._get_advanced_fptr()
        for line in tmp:
            self.len += 1

    def __len__(self):
        return self.len

    def __enter__(self):
        return self

    def __exit__(self):
        if self.fh:
            self.fh.close()

    def __iter__(self):
        self.fh = self._get_advanced_fptr()
        return self

    def __next__(self):
        return self._parse_line(next(self.fh))

    def _get_advanced_fptr(self):
        """Advances file pointer past non-results lines"""
        result = open(self.results_path)
        for line in result:
            if line.startswith("RESULT"):
                break
        return result

    def _parse_line(self, line):
        """Extracts match information of tab delimited V3 resuls"""
        entries = line.strip().split('\t')
        return tess.data.TesseraeResultRecord(
            entries[3], entries[1], self._parse_shared(entries[-2]),
            float(entries[-1]))

    def _parse_shared(shared):
        shared = shared.replace(';', ' ')
        return shared.strip.split()
