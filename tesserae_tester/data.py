"""Data structures and functions for Tesserae comparisons"""


class TesseraeQuery(object):
    """Holder class for Tesserae query parameters"""

    def __init__(self, searchtype, source, target):
        self.searchtype = searchtype
        if searchtype == 'vanilla':
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


class TesseraeResultRecord(object):
    """Holder class for one Tesserae match"""

    def __init__(self, source_loc, target_loc, shared, score):
        """shared must be a sorted iterable"""
        self.source_loc = source_loc
        self.target_loc = target_loc
        self.shared = shared
        self.score = score

    def __eq__(self, other):
        if self.source_loc != other.source_loc or \
                self.target_loc != other.target_loc or \
                self.score != other.score or \
                len(self.shared) != len(other.shared):
            return False
        for this, that in zip(self.shared, other.shared):
            if this != that:
                return False
        return True

    def __str__(self):
        return '\t'.join([
            self.source_loc, self.target_loc, str(self.shared), self.score])
