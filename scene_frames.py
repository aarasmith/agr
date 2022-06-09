# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 07:13:22 2022

@author: andya
"""
import os
import cv2
from scenedetect import detect, ContentDetector
from dataclasses import dataclass
import subprocess

#get_i_frames requires ffmpeg


@dataclass
class scene_frames:
    
    @classmethod
    def get_scene_frames(cls, filepath, destination = None, sep_dir = True):
        
        basename = os.path.splitext(os.path.basename(filepath))[0]        
        destination = cls._set_destination(filepath, basename, destination, sep_dir)
        
        scene_list = detect(filepath, ContentDetector())
        frame_list = [i[0].get_frames() for i in scene_list]
        
        cls._save_frames(filepath, destination, basename, frame_list)
    
    @classmethod
    def get_i_frames(cls, filepath, destination = None, sep_dir = True):
        
        basename = os.path.splitext(os.path.basename(filepath))[0]
        destination = cls._set_destination(filepath, basename, destination, sep_dir)
        
        frame_types = cls._get_frame_types(filepath)
        
        frame_list = [x[0] for x in frame_types if x[1]=='I']
        if frame_list:
            cls._save_frames(filepath, destination, basename, frame_list)
        else:
            print ('No I-frames in '+ filepath)
        
    
    @classmethod
    def _get_frame_types(cls, filepath):
        command = 'ffprobe -v error -show_entries frame=pict_type -of default=noprint_wrappers=1'.split()
        out = subprocess.check_output(command + [filepath]).decode()
        frame_types = out.replace('pict_type=','').split()
        return zip(range(len(frame_types)), frame_types)
    
    @classmethod
    def _set_destination(cls, filepath, basename, destination, sep_dir):
        if destination is None:
            destination = os.path.join(filepath, basename)
        elif sep_dir is True:
            destination = os.path.join(destination, basename)
        if not os.path.isdir(destination):
            os.mkdir(destination)
        
        return destination
    
    @classmethod
    def _save_frames(cls, filepath, destination, basename, frame_list):
        cap = cv2.VideoCapture(filepath)
        for frame_no in frame_list:
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
            ret, frame = cap.read()
            outname = os.path.join(destination, basename + "_i_frame_" + str(frame_no) + ".jpg")
            cv2.imwrite(outname, frame)
            print ('Saved: ' + outname)
        cap.release()