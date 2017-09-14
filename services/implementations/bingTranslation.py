from xml.etree import ElementTree
import requests
from services.implementations.AzureAuthClient import AzureAuthClient
from services.implementations.azureClientSecret import getsecret


def GetTextAndTranslate(textToTranslate, finalToken, langfrom, langto):
    # Call to Microsoft Translator Service
    headers = {"Authorization ": finalToken}
    translateUrl = "http://api.microsofttranslator.com/v2/Http.svc/Translate?text={}&to={}".format(textToTranslate,
                                                                                                   langto)

    translationData = requests.get(translateUrl, headers=headers)
    # parse xml return values
    translation = ElementTree.fromstring(translationData.text.encode('utf-8'))
    # display translation
    print ("The translation is---> ", translation.text)

    print(" ")


def bingtranslation(query, langfrom, langto):

    # adapted from github.com/MicrosoftTranslator/PythonConsole

    client_secret = getsecret() # not present in VCS
    auth_client = AzureAuthClient(client_secret)
    bearer_token = 'Bearer ' + auth_client.get_access_token()
    GetTextAndTranslate(query, bearer_token, langfrom, langto)
    return query