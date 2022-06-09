# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 12:03:25 2022

@author: andya
"""
import os
from google.cloud import translate
from dotenv import load_dotenv
from dataclasses import dataclass, field
import html.parser as htmlparser

load_dotenv()

# trans_text = "_مشاهد من تحرير قرية الزارة النصيرية في ريف حمص الشمالي__.mp4"
# trans_text = "Сирия. Джобар. Тяжелый день для танкистов. Часть 2  [filatov andrey]"
# trans_text = "Que tal"


@dataclass
class GoogleTranslate:
    translation: str
    language: str
    _project_id: str = field(default=os.environ['GOOGLE_PROJECT_ID'], init=False, repr=False)
    target_language_code: str = "en"
    #parent: str = f"projects/{_project_id}"
    _client: object = field(default=translate.TranslationServiceClient(), init=False, repr=False)
    
    
    @classmethod
    def translate(cls, text):
        parent = f"projects/{cls._project_id}"
        response = cls._client.translate_text(
            contents=[text],
            target_language_code=cls.target_language_code,
            parent=parent,
            )
        #return {"translation": cls._translate_text(response), "language": cls._detect_language(response)}
        return GoogleTranslate(cls._translate_text(response), cls._detect_language(response))
    @classmethod
    def _translate_text(cls, response):
        parser = htmlparser.HTMLParser()
        return parser.unescape(response.translations[0].translated_text)
    
    @classmethod
    def _detect_language(cls, response):
        return response.translations[0].detected_language_code