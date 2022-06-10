# -*- coding: utf-8 -*-
"""
Created on Sat May 28 13:51:19 2022

@author: andya
"""

from metadata import metadata as md
from scene_frames import scene_frames as sf
from translate import GoogleTranslate as gt
from tag_and_train import tag_and_train as tnt
from syno_fs import syno_fs as fs
import os
import pandas as pd


source_folder = "D:/Additional Videos/Reddit fix/"
destination = "D:/agr/test"

filepath = os.path.join(source_folder, os.listdir(source_folder)[0])
filepath = "D:/agr/test/_مشاهد من تحرير قرية الزارة النصيرية في ريف حمص الشمالي__.mp4"

entries = pd.DataFrame()

entry = md.write_metadata(filepath, destination)

entries = entries.append(pd.DataFrame.from_dict(entry))

sf.get_scene_frames(filepath, destination)


file_list = fs.list_files("/Main/Visual/Video projects/Conflict Videos/Syria/Syria Addendum/Doc War Syria Addendum")
file_path = file_list['data']['files'][0]['path']
file_path = fs.download_file(file_path, dest_path = "D:/agr/test")
entry = md.write_metadata(file_path, keep_original = False)
sf.get_scene_frames(os.path.join("D:/agr/test", entry['filename'][0] + ".mp4"))
tag_id = tnt.create_tag("mountain_hawks").id
tnt.tag_and_train(os.path.join("D:/agr/test", entry['filename'][0]), tag_id, tag_name = "mountain_hawks")
tag_id = tnt.create_tag("fatah_halab").id
tnt.tag_and_train(os.path.join("D:/agr/test", entry['filename'][0]), tag_id, tag_name = "fatah_halab")


#data structure filename - original_collection - original_title - title_en - \title_ar - year - date - group/s - adm1 - adm2 - adm3 - adm4 - place_name - training_data - is_indexed - vi_id - insights
