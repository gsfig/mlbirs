import json
from os import remove
from os.path import isfile
import configparser
from configuration import Configuration
from translation_model import TranslationService
from ner_model import Ner
import similarity_model
from math import floor


def dispatcher(query):
    print("dispatcher")
    print("query: " + str(query))

    # 0. configurations, database and files creation
    config = configparser.ConfigParser()
    config.read('config.ini')

    development(config)

    c = Configuration(config)

    # tests(c)


    # 1. Translate query
    translation = TranslationService()
    translated = translation.translate_query(query, "pt", "en")
    print(translated)
    # 2. query NER (Name Entity Recognition)
    ner = Ner(config)
    entities = ner.mer_get_entities(translated)

    # 3. find similar
    similar_dict = similarity_model.get_similar(config, entities) # dict { corpus_en_id : text, resnik dishin, resnik mica, lin mica }
    # print(similar_dict)

    # 4. organize response
    response = organize_response(similar_dict)

    return json.dumps(response)


def organize_response(full_dict):
    """

    :param full_dict:
    :return:
    """
    doc_and_ave = dict()
    for doc in full_dict:
        temp = dict()
        temp['doc_id'] = doc
        temp['doc_text'] = full_dict[doc]['text']
        temp['average_score'] = floored_percentage(full_dict[doc]['resnik_dishin'], 3)
        doc_and_ave[doc] = temp
    return doc_and_ave


def floored_percentage(val, digits):
    val *= 10 ** (digits + 2)
    return '{1:.{0}f}'.format(digits, floor(val) / 10 ** digits)


def development(config):
    """
    for development
    :param config:
    :return:
    """

    # mer data files
    lexicon_file = config.get('NER', 'lexicon_file')
    path = 'MER/data/'

    # if isfile(lexicon_file):  # if delete db_file => delete corpus_db
    #     remove(lexicon_file)
    #
    # if isfile(path + lexicon_file):
    #     remove(path + lexicon_file)
    #     remove(path + 'lexicon_radlex_word1.txt')
    #     remove(path + 'lexicon_radlex_word2.txt')
    #     remove(path + 'lexicon_radlex_word2.txt')
    #     remove(path + 'lexicon_radlex_words2.txt')

    # corpus
    # corpus_db_name = config.get("Corpus", "corpus_file")
    # if isfile(corpus_db_name):
    #     remove(corpus_db_name)

    # main DB
    # main_db_name = config.get("MainDB", "db_file")
    # if isfile(main_db_name):
    #     remove(main_db_name)


def tests(configuration):

    main_db_connection = configuration.main_db_connection
    dishin_db = configuration.similarity_connection

    # 1. main_db owl_ids exist but not pref_name or synonym or obsolete.

    entity_ids = set(main_db_connection.execute('SELECT id FROM entity ').fetchall())
    synonym_fk = set(main_db_connection.execute('SELECT fkentity FROM Synonym ').fetchall())
    pref_name_fk = set(main_db_connection.execute('SELECT fkentity FROM Preferred_name ').fetchall())
    pref_name_obs_fk = set(main_db_connection.execute('SELECT fkentity FROM Preferred_Name_for_Obsolete ').fetchall())

    id_set = synonym_fk | pref_name_fk
    id_set2 = id_set | pref_name_obs_fk

    print(len(entity_ids))
    print(len(id_set2))

    diff = list(entity_ids - id_set2)
    print(len(diff))
    diff_owls = dict()
    for d in diff:
        rows = main_db_connection.execute('SELECT owl_id FROM entity WHERE id = ?', (d,)).fetchall()
        diff_owls[d] = rows

    print(diff_owls)

    exit()

