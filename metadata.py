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
from shutil import copy2

@dataclass
class metadata:
    
    @classmethod
    def write_metadata(cls, filepath, destination = os.getcwd(), keep_original = True):
        vid_meta = MP4(filepath)
        basename = os.path.splitext(os.path.basename(filepath))[0]
        vid_meta['\xa9nam'] = basename
        translation = gt.translate(basename)
        name_en = basename
        if translation.language != "en":
            vid_meta['\xa9cmt'] = translation.translation
            name_en = translation.translation
        vid_meta.save()
        unique_name = uuid.uuid4().hex
        if keep_original:
            copy2(filepath, os.path.join(destination, unique_name + ".mp4"))
        else:
            os.rename(filepath, os.path.join(destination, unique_name + ".mp4"))
        
        return {"original_title": [basename], "filename": [unique_name], "title_en": [name_en]}
