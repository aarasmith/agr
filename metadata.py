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
    def write_metadata(cls, file_path, dest_path = None, keep_original = True):
        if dest_path is None:
            dest_path = os.path.dirname(file_path)
        
        vid_meta = MP4(file_path)
        basename = os.path.splitext(os.path.basename(file_path))[0]
        vid_meta['\xa9nam'] = basename
        name_en = basename
        
        translation = gt.translate(basename)        
        if translation.language != "en":
            vid_meta['\xa9cmt'] = translation.translation
            name_en = translation.translation
        
        vid_meta.save()
        
        unique_name = uuid.uuid4().hex
        destination = os.path.join(dest_path, unique_name + ".mp4")
        if keep_original:
            copy2(file_path, destination)
        else:
            os.rename(file_path, destination)
        
        return [destination, unique_name, basename, name_en]
