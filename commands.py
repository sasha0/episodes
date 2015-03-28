from app import app
from app.models import TVSeries
from pyes import *

@app.cli.command()
def index_data():
    # establishing connection to ElasticSearch server
    es_conn = ES('127.0.0.1:9200')

    settings = {
        'analysis': {
            'filter': {
                'ngram_filter': {
                    'type': 'nGram',
                    'min_gram': 2,
                    'max_gram': 12
                }
            },
            'analyzer': {
                'index_ngram_analyzer': {
                    'type': 'custom',
                    'tokenizer': 'standard',
                    'filter': ['lowercase', 'ngram_filter']
                },
                'search_ngram_analyzer': {
                    'type': 'custom',
                    'tokenizer': 'standard',
                    'filter': ['lowercase']
                }
            }
        }
    }

    if es_conn.indices.exists_index("tvseries"):
        es_conn.indices.delete_index("tvseries")
    es_conn.indices.create_index("tvseries", settings=settings)

    mapping = {
        'title': {
            'store': 'yes',
            'type': 'string',
            'index': 'analyzed',
            'index_analyzer': "index_ngram_analyzer",
            'search_analyzer': "search_ngram_analyzer"
        },
        'short_description': {
            'store': 'yes',
            'type': 'string',
            'index': 'analyzed'
        },
        'description': {
            'store': 'yes',
            'type': 'string',
            'index': 'analyzed'
        },
        'tvchannel': {
            'store': 'yes',
            'type': 'string'
        },
        'genres': {
            'store': 'yes',
            'type': 'string'
        },
        'cover_thumbnail': {
            'store': 'yes',
            'type': 'string'
        },
        'short_credits': {
            'store': 'yes',
            'type': 'string'
        },
        'id': {
            'store': 'yes',
            'type': 'integer'
        }


    }
    try:
        mapping_exists = es_conn.indices.get_mapping('tvseries-mapping')
    except:
        mapping_exists = False
    if mapping_exists:
        es_conn.indices.delete_mapping("tvseries", "tvseries-mapping")
    es_conn.indices.put_mapping("tvseries-mapping", {'properties': mapping}, ["tvseries"])
    for tvseries in TVSeries.query.all():
        doc = {'title': tvseries.title,
               'short_description': tvseries.short_description,
               'description': tvseries.description,
               'genres': [g.title for g in tvseries.genres],
               'tvchannel': tvseries.tvchannel.title,
               'cover_thumbnail': tvseries.cover_thumbnail,
               'short_credits': [a.full_name for a in tvseries.short_credits],
               'id': tvseries.id
               }
        es_conn.index(doc, 'tvseries', 'tvseries-mapping')
        print 'Indexed TV series %s' % tvseries.title