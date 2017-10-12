from django.http import HttpResponse
from services.annotate import Annotate
from services.translateQuery import TranslationService
from services.similar import Similar
from services.corpus_db import CorpusDB


def translate(request):
    # 0. setup corpus database
    corpus_db = CorpusDB()
    corpus_db.setup_db()

    if request.method == 'POST':
    # if request.method == 'GET':





        # 1. Translate
        transl = TranslationService()
        transl.toTranslate = request.GET.get('QueryField', '')
        print("toTranslate: " + transl.toTranslate)
        langfrom = "pt"
        langto = "en"
        transl.translatequery(langfrom, langto)
        translatedquery = transl.translated

        # print("translated: " + translatedquery)

        # 2. NER
        ner = Annotate()
        ner.query = translatedquery
        ner_response = ner.ner() # keys
        # print("NER RESPONSE")
        # print(ner_response)
        print("ner_response length: " + str(len(ner_response)))
        # print(ner_response)

        # ner.get_entities_and_frequencies()


        # 3. similar (DShin)
        similar = Similar()
        similar.query_list = ner_response
        # similar.query_list.append('infarction')
        # similar.query_list.append('hernia modifier')
        # similar.query_list.append('hypothalamospinal tract')
        # similar.query_list.append('brodmann')

        # print(similar.query_list)
        similar_list = similar.getSimilar()
        print("SIMILAR DSHIN")
        print(similar_list)


        # 4. organize response


    return HttpResponse(similar_list)


