from OutServices.DiShIn import semanticbase

# TODO: seperate in functions: 1. semanticbase.create; 2. Corpus database; 3. get_similar
def getSimilar(id_list):


    owl_file = "OutServices/DiShIn/Radlex3.14.owl"
    db_file = 'radlex.db'
    name_prefix = 'http://www.radlex.org/RID/#'
    relation = 'http://www.w3.org/2000/01/rdf-schema#subClassOf'
    annotation_file = ''

    # prepare DB
    # semanticbase.create(owl_file, db_file, name_prefix, relation, annotation_file)
    # TODO: here, find way to: with pref_name, get RID to continue

    return "ended get Similar"
