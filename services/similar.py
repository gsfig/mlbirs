from services.implementations import similar_DiShin
from services.implementations import database_search


class Similar:
    query_list = list()
    db_list = ''
    id_list = list()

    def getSimilar(self):
        self.get_id_from_name()
        self.make_id_list()
        return similar_DiShin.getSimilar(self.id_list)

    def get_id_from_name(self):
        self.db_list = database_search.get_id(self.query_list)

    def make_id_list(self):

        for entry in self.db_list:
            self.id_list.append(self.db_list[entry]['rid'])

        flat_list = [item for sublist in self.id_list for item in sublist]
        self.id_list = list(set(flat_list)) # set removes duplicates
        self.id_list.sort()



