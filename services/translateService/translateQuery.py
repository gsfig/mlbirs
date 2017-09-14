from services.translateService import bingTranslation


class TranslationService:
    toTranslate = ""
    translated = ""

    def translatequery(self):

        return bingTranslation.bingtranslation(self.toTranslate)









