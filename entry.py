# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 10:59:02 2022

@author: andya
"""
#data structure filename - original_collection - original_title - title_en - \title_ar - year - date - group/s - adm1 - adm2 - adm3 - adm4 - place_name - training_data - is_indexed - vi_id - insights
import metadata as md
from scene_frames import scene_frames as sf
from translate import GoogleTranslate as gt
from tag_and_train import tag_and_train as tnt
from syno_fs import syno_fs as fs
import os
import pandas as pd
from db import get_connection
from dataclasses import dataclass, field, asdict
from CustomVision import CustomVision as cv
import json

@dataclass
class entry:
    file_path: str
    train_path: str = None
    file_name: str = None
    original_collection: str = None
    original_title: str = None
    title_en: str = None
    year: int = None
    date: str = None
    armed_groups: list = field(default_factory=lambda: [None])
    adm1: str = None
    adm2: str = None
    adm3: str = None
    adm4: str = None
    place_name: str = None
    is_training: bool = False
    is_indexed: bool = False
    vi_id: str = None
    insights: str = None
    pred_results: dict = field(default_factory=lambda: {})
    
    
    
    def write_metadata(self, dest_path = None, keep_original = True):
        self.file_path, self.file_name, self.original_title, self.title_en = md.write_metadata(self.file_path, dest_path, keep_original)
    
    def get_scene_frames(self, dest_path = None, sep_dir = True):
        self.train_path = sf.get_scene_frames(self.file_path, dest_path, sep_dir)
        
    def tag_and_train(self, save_json = True):
        tags = tnt.get_tags()
        for ag in self.armed_groups:
            print(ag)
            if ag not in tags.keys():
                tag_id = tnt.create_tag(ag).id
            else:
                tag_id = tags[ag]
            tnt.tag_and_train(self.train_path, tag_id, tag_name = ag)
        self.is_training = True

    def preds_from_local(self):
        self.armed_groups, self.pred_results = cv.preds_from_local(self.file_path)
        
    def finish(self):
        df = pd.DataFrame([asdict(self)]).set_index('file_name')
        df['pred_results'] = str(json.dumps(df['pred_results'].iloc[0]))
        df['armed_groups'] = str(json.dumps(df['armed_groups'].iloc[0]))
        with get_connection("agr_db.sqlite") as con:
            df.to_sql("videos", con, if_exists="append")
