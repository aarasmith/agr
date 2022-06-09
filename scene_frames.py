# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 07:13:22 2022

@author: andya
"""
import os
import cv2
from scenedetect import detect, ContentDetector
from dataclasses import dataclass


@dataclass
class scene_frames:
    
    @classmethod
    def get_scene_frames(cls, filename, destination = None, sep_dir = True):
        
        basename = os.path.splitext(os.path.basename(filename))[0]
        
        if destination is None:
            destination = os.getcwd() + f"/{basename}/"
        elif sep_dir is True:
            destination = destination + f"/{basename}/"
        if not os.path.isdir(destination):
            os.mkdir(destination)
        
        scene_list = detect(filename, ContentDetector())
        frame_list = [i[0].get_frames() for i in scene_list]
        
        cap = cv2.VideoCapture(filename)
        for frame_no in frame_list:
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
            ret, frame = cap.read()
            outname = destination + basename+'_i_frame_'+str(frame_no)+'.jpg'
            cv2.imwrite(outname, frame)
            print ('Saved: ' + outname)
        cap.release()

