# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 14:51:50 2022

@author: andya
"""
from mutagen.mp4 import MP4
import uuid
import os
from dataclasses import dataclass
from translate import GoogleTranslate as gt

@dataclass
class metadata:
    
    @classmethod
    def write_metadata(cls, filename, filepath = os.getcwd() + "/", destination = os.getcwd() + "/"):
        vid_meta = MP4(filepath + filename)
        basename = os.path.splitext(os.path.basename(filename))[0]
        vid_meta['\xa9nam'] = basename
        translation = gt.translate(basename)
        name_en = basename
        if translation.language != "en":
            vid_meta['xa9cmt'] = translation.translation
            name_en = translation.translation
        vid_meta.save()
        unique_name = uuid.uuid4().hex
        os.rename(filepath + filename, destination + unique_name + ".mp4")
        
        return {"original_title": basename, "filename": unique_name, "title_en": name_en}
