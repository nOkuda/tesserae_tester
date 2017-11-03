"""v4 Tesserae queries"""
import requests

import tesserae_tester as tess


QUERY_FORM = 'author:"{0}" AND title:"{1}" AND parse_type:"{2}"'


def get_query_results(v4path, query):
    """Executes query in V4 and return results

    Assumes that Solr is reachable on v4path
    """
    s_author, s_title = query.sourcetext.split('.')
    t_author, t_title = query.targettext.split('.')
    s_author = ' '.join([a.capitalize() for a in s_author.split()])
    t_author = ' '.join([a.capitalize() for a in t_author.split()])
    s_title = ' '.join([a.capitalize() for a in s_title.split('_')])
    t_title = ' '.join([a.capitalize() for a in t_title.split('_')])
    params = {
        'wt': 'python',
        'tess.sq': QUERY_FORM.format(s_author, s_title, query.unit),
        'tess.sf': 'text',
        'tess.sfl': 'text',
        'tess.tq': QUERY_FORM.format(t_author, t_title, query.unit),
        'tess.tf': 'text',
        'tess.tfl': 'text',
        'tess.sw': query.stop,
        'tess.cut': query.cutoff,
        'tess.md': query.dist,
        'start': '0',
        'rows': '999999'
    }
    response = requests.get(v4path+'latin/compare', params=params)
    response.raise_for_status()
    return _solr_to_results(eval(str(response.text)))


def _solr_to_results(solr_result):
    """Converts Solr result in TesseraeResults"""
    result = tess.data.TesseraeResults('v4', solr_result['stopList'])
    for match in solr_result['matches']:
        result.container[tess.data.TesseraeMatch(
            tess.data.clean_words(match['source']['fields']['text']),
            tess.data.clean_words(match['target']['fields']['text']))] = \
                tess.data.TesseraeData(
                    '; '.join(match['terms']), match['score'])
    return result
