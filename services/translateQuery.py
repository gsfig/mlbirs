from services.implementations import bingTranslation


class TranslationService:
    toTranslate = ""
    translated = ""

    def translatequery(self, langfrom, langto):

        return bingTranslation.bingtranslation(self.toTranslate, langfrom, langto)









