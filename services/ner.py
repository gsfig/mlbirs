from services.implementations import mer


class Ner:
    query = ""
    entities = ""

    def getner(self):
        return mer.mer(self.query)


