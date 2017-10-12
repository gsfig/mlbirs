import sqlite3


def get_id(name_list):
    """
    returns all terms queried, with rid field '' if term isnt found.
    returns duplicate rid if term is pref_name AND synonym or obsolete AND snomed ... etc.
    :param name_list:
    :return:
    """
    db_name = 'radlex314.sqlite'
    list_id = dict()
    connection = sqlite3.connect(db_name)
    c = connection.cursor()

    # TODO: rid fica como lista. Se há pref_name e snomed, há 2x mesmo RID

    for name in name_list:
        # print("name: " + str(name))
        dict_new = dict()
        rid_list = list()
        dict_new['pref_name'] = ''
        dict_new['pref_name_obs'] = ''
        dict_new['snomed'] = ''
        dict_new['Synonym'] = ''
        dict_new['umls'] = ''

        ## Prefered name
        # TODO: SELECT UNIQUE ?
        res = c.execute("SELECT DISTINCT owlEntity.name, Preferred_name.name "
                        "FROM owlEntity "
                        "JOIN Preferred_name on owlEntity.id = Preferred_name.fkentity "
                        "WHERE Preferred_name.name = ?", (name,))

        for rid in res:
            if not dict_new['pref_name']: # no way of knowing if res is empty
                dict_new['pref_name'] = name
            rid_list.append(rid[0])

        ## Obsolete
        res = c.execute("SELECT DISTINCT owlEntity.name, Preferred_Name_for_Obsolete.name "
                        "FROM owlEntity "
                        "JOIN Preferred_Name_for_Obsolete on owlEntity.id = Preferred_Name_for_Obsolete.fkentity "
                        "WHERE Preferred_Name_for_Obsolete.name = ?", (name,))

        for rid in res:
            if not dict_new['pref_name_obs']:  # no way of knowing if res is empty
                dict_new['pref_name_obs'] = name
            rid_list.append(rid[0])

        ## SNOMED
        res = c.execute("SELECT DISTINCT owlEntity.name, SNOMED_Term.name "
                        "FROM owlEntity "
                        "JOIN SNOMED_Term on owlEntity.id = SNOMED_Term.fkentity "
                        "WHERE SNOMED_Term.name = ?", (name,))

        for rid in res:
            if not dict_new['snomed']:  # no way of knowing if res is empty
                dict_new['snomed'] = name
            rid_list.append(rid[0])

        ## Synonym
        res = c.execute("SELECT DISTINCT owlEntity.name, Synonym.name "
                        "FROM owlEntity "
                        "JOIN Synonym on owlEntity.id = Synonym.fkentity "
                        "WHERE Synonym.name = ?", (name,))

        for rid in res:
            if not dict_new['Synonym']:  # no way of knowing if res is empty
                dict_new['Synonym'] = name
            rid_list.append(rid[0])

        ## UMLS
        res = c.execute("SELECT DISTINCT owlEntity.name, UMLS_Term.name "
                        "FROM owlEntity "
                        "JOIN UMLS_Term on owlEntity.id = UMLS_Term.fkentity "
                        "WHERE UMLS_Term.name = ?", (name,))

        for rid in res:
            if not dict_new['umls']:  # no way of knowing if res is empty
                dict_new['umls'] = name
            rid_list.append(rid[0])

        dict_new['rid'] = rid_list
        list_id[name] = dict_new



    # print("database_search, print list_id")
    # print(list_id)
    connection.close()
    return list_id

