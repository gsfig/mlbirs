import subprocess

from django.http import HttpResponse

from services.ner.ner import Ner
from services.translateService.translateQuery import TranslationService


def translate(request):
    if request.method == 'GET':

        # 1. Translate
        transl = TranslationService()
        transl.toTranslate = request.GET.get('QueryField', '')
        translatedquery = transl.translatequery()


        # 2. NER
        ner = Ner()
        ner.query = translatedquery
        response = ner.getner()


    return HttpResponse(response)


