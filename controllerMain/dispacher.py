from django.http import HttpResponse

from services.ner import Ner
from services.translateQuery import TranslationService


def translate(request):
    if request.method == 'GET':

        # 1. Translate
        transl = TranslationService()
        transl.toTranslate = request.GET.get('QueryField', '')
        print("toTranslate: " + transl.toTranslate)
        langfrom = "pt"
        langto = "en"
        transl.translatequery(langfrom, langto)
        translatedquery = transl.translated

        print(translatedquery)

            # 2. NER
        ner = Ner()
        ner.query = translatedquery
        response = ner.getner()

        # 3. similar



    return HttpResponse(response)


