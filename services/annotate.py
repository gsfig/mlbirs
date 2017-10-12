from services.implementations import mer


class Annotate:
    query = ""
    ner_response = ''
    entity_and_frequencies = ""

    def ner(self):
        self.ner_response = mer.mer(self.query)
        self.get_entities_and_frequencies()
        return self.get_entities()

    def get_entities(self):
        """

        :return: list of entities
        """
        if self.entity_and_frequencies:
            return list(self.entity_and_frequencies.keys())
        else:
            raise ValueError('ner response not set')

    def get_entities_and_frequencies(self):
        """

        :return: dict of entity : frequency
        """
        if self.ner_response:
            self.entity_and_frequencies = mer.get_entities_and_frequencies(self.ner_response)
            return self.entity_and_frequencies
        else:
            raise ValueError('ner response not set')


