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
from db import get_connection


source_folder = "D:/Additional Videos/Reddit fix/"
destination = "D:/agr/test"

filepath = os.path.join(source_folder, os.listdir(source_folder)[0])
filepath = "D:/agr/test/_مشاهد من تحرير قرية الزارة النصيرية في ريف حمص الشمالي__.mp4"

entries = pd.DataFrame()

entry = md.write_metadata(filepath, destination)

entries = entries.append(pd.DataFrame.from_dict(entry))

sf.get_scene_frames(filepath, destination)

entry = {"original_collection": "syria_doc_war"}
file_list = fs.list_files("/Main/Visual/Video projects/Conflict Videos/Syria/Syria Addendum/Doc War Syria Addendum")
file_path = file_list['data']['files'][0]['path']
file_path = fs.download_file(file_path, dest_path = "D:/agr/test")
entry.update(md.write_metadata(file_path, keep_original = False))
sf.get_scene_frames(os.path.join("D:/agr/test", entry['filename'][0] + ".mp4"))
tag_id = tnt.create_tag("mountain_hawks").id
tnt.tag_and_train(os.path.join("D:/agr/test", entry['filename'][0]), tag_id, tag_name = "mountain_hawks")
tag_id = tnt.create_tag("fatah_halab").id
tnt.tag_and_train(os.path.join("D:/agr/test", entry['filename'][0]), tag_id, tag_name = "fatah_halab")


#data structure file_name - original_collection - original_title - title_en - \title_ar - year - date - group/s - adm1 - adm2 - adm3 - adm4 - place_name - training_data - is_indexed - vi_id - insights

con = get_connection("agr_db.sqlite")
entries.set_index('file_name').to_sql("videos", con, if_exists="append")


pd.DataFrame([asdict(x)])




file_list = fs.list_files("/Main/Visual/Video projects/Conflict Videos/Syria/Syria Addendum/Doc War Syria Addendum")
file_path = file_list['data']['files'][0]['path']
file_path = fs.download_file(file_path, dest_path = "D:/agr/test")

vid = entry(file_path, original_collection = "syria_doc_war", armed_group = ["mountain_hawks", "fatah_halab"])
vid.write_metadata(keep_original = False)
vid.get_scene_frames()
vid.tag_and_train()

#dest_path = "D:/agr/test/training"