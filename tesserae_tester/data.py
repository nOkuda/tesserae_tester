"""Data structures and functions for Tesserae comparisons

Every Tesserae version must implement a get_query_results function that returns
an instance of TesseraeResults
"""
import collections
import re


class TesseraeQuery(object):
    """Holder class for Tesserae query parameters"""

    def __init__(self, searchtype, source, target):
        self.searchtype = searchtype
        if searchtype == 'vanilla':
            # simple text to text query
            self.targettext = target
            self.sourcetext = source
            # defaults for v3 according to read_table.pl
            self.unit = 'line'
            self.feature = 'stem'
            self.freq_basis = 'texts'
            self.score = 'feature'
            self.stop = '10'
            self.stbasis = 'corpus'
            self.dist = '999'
            self.dibasis = 'freq'
            self.cutoff = '0'
        else:
            raise NotImplementedError(
                'No query implementation for '+searchtype)


class TesseraeResults(object):
    """Holder class for Tesserae results

    self.container :: {(source words, target words): ((shared words), score)}
    """

    def __init__(self, version, stopwords):
        self.version = version
        self.stopwords = stopwords
        self.container = {}


TesseraeMatch = collections.namedtuple(
        'TesseraeMatch', 'source_text target_text')
TesseraeData = collections.namedtuple('TesseraeData', 'match_terms score')


NON_ALPHA = re.compile('\W+', re.UNICODE)


def clean_words(words):
    """Normalize text across versions

    There seemed to be discrepancies in the way v3 and v4 handled punctuation,
    so we're going to ignore punctuation formatting differences.
    """
    return ' '.join(NON_ALPHA.sub(' ', words).strip().split())
