"""
Big Translator by Timothy Eden

This program takes a user input, a word or phrase, and translates it to as many available languages as possible at once.

The list of returned languages should be in alphabetical order, with the language on the left, and the translation on the
right.

As an idea for expanding this program, it could show a phonetic pronounciation when one is not obvious (i.e. when the word
is translated into a language with a different writing system).
"""

import google.cloud
import os
# auth login and auth application-default login from terminal window
# You will need to create your own Google Cloud account and set up your own authentication.
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/Users/timothyeden/.config/gcloud/application_default_credentials.json"
# loop through each available language
# try-except, translate if able, otherwise move on and put ?

# The code in translate_twm is publicly available code from Google Cloud. twm stands for Text With Model
from google.cloud import translate

def translate_twm(
    target_language="es",
    text="YOUR_TEXT_TO_TRANSLATE",
    project_id="bigtranslator101",
    model_id="general/nmt",
):
    """Translates a given text using Translation custom model."""

    client = translate.TranslationServiceClient()

    location = "us-central1"
    parent = f"projects/{project_id}/locations/{location}"
    model_path = f"{parent}/models/{model_id}"

    # Supported language codes: https://cloud.google.com/translate/docs/languages
    response = client.translate_text(
        request={
            "contents": [text],
            "target_language_code": target_language,
            "model": model_path,
            "source_language_code": "en",
            "parent": parent,
            "mime_type": "text/plain",  # mime types: text/plain, text/html
        }
    )
    # Display the translation for each input text provided
    for translation in response.translations:
        r = ("{}".format(translation.translated_text))
    return r


def list_languages_with_target(target):
    """Lists all available languages and localizes them to the target language.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """
    from google.cloud import translate_v2 as translate

    translate_client = translate.Client()

    # saves the results into a list of dictionaries, with keys "language" and "name"
    results = translate_client.get_languages(target_language=target)

    # gets the values saved in "language" (the 2 letter code)
    languages = []
    # gets the values saved in "name" (the actual name of the language)
    names = []

    for d in results:
        languages.append(d['language'])
        names.append(d['name'])
    return languages,names

# get user input, assign to variable
# pass in desired language and variable

languages,names = list_languages_with_target("en")


print("Enter text:")
user_input = input('>  ')
# This was test code using a short list of languages
#list_of_languages = ["es", "fr", "zh", "ja", "hi", "it", "de", "ko", "ru", "ar"]
#language_names = ["Spanish", "French", "Chinese", "Japanese", "Hindi", "Italian", "German", "Korean", "Russian", "Arabic"]

# iterates over languages and names in parallel to print the language and translation
language_zip = zip(languages,names)

for language,name in language_zip:
    try:
        translation = translate_twm(language,user_input)
        print(name + ': ' + translation)
    except:
        pass
