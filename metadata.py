# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 14:51:50 2022

@author: andya
"""
from mutagen.mp4 import MP4
import uuid
import os
from translate import GoogleTranslate as gt
from shutil import copy2


def write_metadata(file_path, dest_path = None, keep_original = False):
    """
    Function for taking messy filenames and standardizing them
    
    Takes the original filename of an MP4 and any translation of it and writes these
    to the video's metadata under "Title" and "Comments" respectively
    
    Renames the file to a 32 char string generated with uuid and writes the file
    either in the same directory or wherever dest_path points to

    Parameters
    ----------
    file_path : STR
        The file path of the targeted MP4.
    dest_path : STR, optional
        Path to the destination folder.
        If None, the dest_path is set to the same folder as file_path.
        The default is None.
    keep_original : BOOL, optional
        If True, the file is copied to the destination under the new name
        If False, the file is renamed and moved to the destination. 
        The default is False.

    Returns
    -------
    list
        [new file path, new name, original name, original name translated to english].

    """    
    video_metadata = MP4(file_path)
    basename = os.path.splitext(os.path.basename(file_path))[0]
    video_metadata['\xa9nam'] = basename
    
    name_en = gt.translate(basename).translation
    if basename != name_en:
        video_metadata['\xa9cmt'] = name_en
    
    video_metadata.save()
    
    unique_name, destination = _rename(file_path, dest_path, keep_original)
    
    return [destination, unique_name, basename, name_en]

def _rename(file_path, dest_path, keep_original):
    
    unique_name = uuid.uuid4().hex
    if dest_path is None:
        dest_path = os.path.dirname(file_path)
    elif not os.path.isdir(dest_path):
        os.makedirs(dest_path)
        
    destination = os.path.join(dest_path, unique_name + ".mp4")
    
    if keep_original:
        copy2(file_path, destination)
    else:
        os.rename(file_path, destination)
    
    return unique_name, destination
