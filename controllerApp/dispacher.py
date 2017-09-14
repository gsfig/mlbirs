from django.http import HttpResponse

from services.ner import Ner
from services.translateQuery import TranslationService


def translate(request):
    if request.method == 'GET':

        # 1. Translate
        transl = TranslationService()
        transl.toTranslate = request.GET.get('QueryField', '')
        langfrom = "pt"
        langto = "en"
        translatedquery = transl.translatequery(langfrom, langto)


        # 2. NER
        ner = Ner()
        ner.query = translatedquery
        response = ner.getner()

        # 3. similar



    return HttpResponse(response)


