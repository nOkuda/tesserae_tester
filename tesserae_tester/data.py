"""Data structures and functions for Tesserae comparisons

Every Tesserae version must implement a get_query_results function that returns
an instance of TesseraeResults
"""


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
            self.freq_basis = 'text'
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

    def __init__(self, label):
        self.label = label
        self.container = {}


class TesseraeMatch(object):
    """Holder class for Tesserae matches"""

    def __init__(self, source_text, target_text):
        self.source_text = source_text
        self.target_text = target_text

    def __hash__(self):
        return hash((self.source_text, self.target_text))

    def __eq__(self, other):
        if self.source_text == other.source_text and \
                self.target_text == other.target_text:
            return True
        return False

    def __lt__(self, other):
        return (self.source_text, self.target_text) < \
            (other.source_text, other.target_text)

    def __str__(self):
        return '({0}, {1})'.format(self.source_text, self.target_text)

    def __repr__(self):
        return str(self)


class TesseraeData(object):
    """Holder class for Tesserae match data"""

    def __init__(self, match_terms, score):
        self.match_terms = match_terms
        self.score = score

    def __str__(self):
        return '({0}, {1})'.format(self.match_terms, self.score)

    def __repr__(self):
        return str(self)
