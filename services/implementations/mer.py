from subprocess import Popen, PIPE


def mer(query):
    """

    :param query:
    :return: text: first column corresponds to the start-index, the second to the end-index and the third to the annotated term
    """

    # TODO: mer function to create lexicon (commandProduceDataFiles)
    command1 = "bash"
    directory = "OutServices/MER"
    commandGetEntities = "get_entities.sh"
    commandProduceDataFiles = "produce_data_files.sh"
    text = str(query)
    lexicon = "lexiconRadlex"
    lexicon_path = directory + "/data/" + lexicon + ".txt"

    #produceDataFiles(command1, commandProduceDataFiles, lexicon_path)

    return get_entities_mer(command1, commandGetEntities, text, lexicon)


def get_entities_mer(command1, commandGetEntities, text, lexicon):
    sreturn = ''
    with Popen([command1, commandGetEntities, text, lexicon], cwd='OutServices/MER', stdout=PIPE, bufsize=1,
               universal_newlines=True) as process:
        for line in process.stdout:  # b'\n', b'\r\n', b'\r' are recognized as newline
            sreturn += line
    return sreturn


def produceDataFiles(command1, commandProduceDataFiles, lexicon):
    sreturn = ''
    with Popen([command1, commandProduceDataFiles, lexicon], cwd='OutServices/MER', stdout=PIPE, bufsize=1,
               universal_newlines=True) as process:
        for line in process.stdout:  # b'\n', b'\r\n', b'\r' are recognized as newline
            sreturn += line
    print("produce data")
    print(sreturn)


def get_entities_and_frequencies(mer_response):
    """

    :param ner_response: first column corresponds to the start-index, the second to the end-index and the third to the annotated term
    :return:
    """

    entities = dict()

    split1 = mer_response.split('\n') # each line

    for s in split1:
        s2 = s.split('\t') # index \t index \t term
        if len(s2) > 1:
            entity = s2[2]
            entity.lower() # lower case
            if entity in entities:
                entities[entity] += 1
            else:
                entities[entity] = 1
    return entities
