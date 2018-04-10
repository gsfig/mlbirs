import db_utilities
import DiShIn.semanticbase as dishin_base
import DiShIn.ssm as dishin_ssm
import main_db
import corpus_utilities as corpus


def get_similar(config, entities) -> dict:
    """
    :param config:
    :param entities: list of entity names
    :return:
    """

    dishin_db = config.get('DISHIN', 'dishin_file')
    query_owl_parents = main_db.get_parents(config, entities)  # dict: query_name : [parent_RID]
    query_owl_parents = [item for sublist in list(query_owl_parents.values()) for item in sublist]
    query_owl_parents = list(set(query_owl_parents))  # remove duplicates

    corpus_parents = get_corpus_parents(config)  # list: [parent_RIDs] without duplicates

    corpus_scores = evaluate_similarity(query_owl_parents, corpus_parents, dishin_db)  # dict{ corpus_owl : resnik dishin, resnik mica, lin mica }

    # print(corpus_scores)
    corpus_eval = rank_corpus(config, corpus_scores)  # dict { corpus_en_id : text, resnik dishin, resnik mica, lin mica }
    return corpus_eval


def rank_corpus(config, corpus_scores):

    corpus_dict = corpus.get_corpus_id_and_text(config)  # dict { corpus_en_id : text : corpus_en_text }

    for doc_id in corpus_dict:
        corpus_owl = corpus.get_owl_annotations_en(config, doc_id)
        corpus_owl = main_db.get_parents_owl(config, corpus_owl)  # dict {RID_annotation : [RIDs_parents]}
        corpus_owl = [item for sublist in list(corpus_owl.values()) for item in sublist]  # list with duplicates
        length = 0

        corpus_dict[doc_id].update({'resnik_dishin': 0, 'resnik_mica': 0, 'lin_mica': 0})

        for corpus_annotation in corpus_owl: # for each corpus owl
            if corpus_annotation in corpus_scores: # if corpus owl in scores, add scores
                corpus_dict[doc_id]['resnik_dishin'] += corpus_scores[corpus_annotation]['resnik_dishin']
                corpus_dict[doc_id]['resnik_mica'] += corpus_scores[corpus_annotation]['resnik_mica']
                corpus_dict[doc_id]['lin_mica'] += corpus_scores[corpus_annotation]['lin_mica']
                length +=1
                # print(str(corpus_scores[corpus_annotation]['resnik_dishin']) + "; " + str(corpus_scores[corpus_annotation]['resnik_mica']) + "; " + str(corpus_scores[corpus_annotation]['lin_mica']))

        # average
        corpus_dict[doc_id]['resnik_dishin'] = corpus_dict[doc_id]['resnik_dishin'] / length
        corpus_dict[doc_id]['resnik_mica'] = corpus_dict[doc_id]['resnik_mica'] / length
        corpus_dict[doc_id]['lin_mica'] = corpus_dict[doc_id]['lin_mica'] / length

    return corpus_dict
    # corpus1 : text, ave1, ave2, ave3 ;
    # corpus2 : text, ave1, ave2, ave3 ; ...


def evaluate_similarity(query_parents, corpus_parents, dishin_db):
    """
    return each corpus owl_id average score
    :param query_parents:
    :param corpus_parents:
    :param dishin_db:
    :return:
    """
    print('evaluating similarity: query list: ' + str(len(query_parents)) + ', corpus list: ' + str(len(corpus_parents)))

    dishin_ssm.semantic_base(dishin_db)

    # dict{ query : corpus : resnik dishin, resnik mica, lin mica }

    #similar = dict()
    scores = dict()

    for query_owl in query_parents:
        #corpus_dict = dict()

        for corpus_owl in corpus_parents:

            q = dishin_ssm.get_id(query_owl)
            c = dishin_ssm.get_id(corpus_owl)
            dishin_ssm.intrinsic = True
            dishin_ssm.mica = False
            resnik_dishin = float(dishin_ssm.ssm_resnik(q, c))
            dishin_ssm.mica = True
            resnik_mica = float(dishin_ssm.ssm_resnik(q, c))
            lin_mica = float(dishin_ssm.ssm_lin(q, c))

            if corpus_owl not in scores:
                scores[corpus_owl] = {'resnik_dishin': 0, 'resnik_mica' : 0, 'lin_mica' : 0}

            scores[corpus_owl]['resnik_dishin'] += resnik_dishin
            scores[corpus_owl]['resnik_mica'] += resnik_mica
            scores[corpus_owl]['lin_mica'] += lin_mica

            #corpus_dict[corpus_owl] = {'resnik_dishin': resnik_dishin, 'resnik_mica' : resnik_mica, 'lin_mica' : lin_mica}
            # print(str(query_owl) + " " + str(corpus_owl) + " resnik_dishin: " + str(resnik_dishin) + " resnik_mica: " + str(resnik_mica) + " lin_mica: " + str(lin_mica))

        #similar[query_owl] = corpus_dict

    length = len(query_parents) # for average
    for owl in scores:
        scores[owl]['resnik_dishin'] = scores[owl]['resnik_dishin'] / length
        scores[owl]['resnik_mica'] = scores[owl]['resnik_mica'] / length
        scores[owl]['lin_mica'] = scores[owl]['lin_mica'] / length

    return scores


def get_corpus_parents(config):
    """
    list of corpus owl parents without duplicates
    :param config:
    :return:
    """

    corpus_list = corpus.get_entities_owl(config)

    corpus_list = main_db.get_parents_owl(config, corpus_list)
    corpus_list = [item for sublist in list(corpus_list.values()) for item in sublist]
    return list(set(corpus_list))  # remove duplicates


def similarity_configuration(config):

    dishin_db = config.get('DISHIN', 'dishin_file')
    file = config.get('Files', 'rdf_file')
    relation = config.get('DISHIN', 'relation2')
    prefix = config.get('Predicates', 'subject_to_remove')

    if not db_utilities.check_db_file(dishin_db):
        dishin_base.create(file, dishin_db, prefix, relation, '')
    return db_utilities.connect_db(dishin_db)


