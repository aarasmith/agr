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
    def get_scene_frames(cls, file_path, dest_path = None, sep_dir = True, save = True):
        
        basename = os.path.splitext(os.path.basename(file_path))[0]        
        dest_path = cls._set_dest_path(file_path, basename, dest_path, sep_dir)
        
        scene_list = detect(file_path, ContentDetector())
        frame_list = [i[0].get_frames() for i in scene_list]
        
        if save:
            cls._save_frames(file_path, dest_path, basename, frame_list)        
            return dest_path
        else:
            return frame_list
    
    @classmethod
    def get_i_frames(cls, file_path, dest_path = None, sep_dir = True):
        
        basename = os.path.splitext(os.path.basename(file_path))[0]
        dest_path = cls._set_dest_path(file_path, basename, dest_path, sep_dir)
        
        frame_types = cls._get_frame_types(file_path)
        
        frame_list = [x[0] for x in frame_types if x[1]=='I']
        if frame_list:
            cls._save_frames(file_path, dest_path, basename, frame_list)
        else:
            print ('No I-frames in '+ file_path)
        
    
    @classmethod
    def _get_frame_types(cls, file_path):
        command = 'ffprobe -v error -show_entries frame=pict_type -of default=noprint_wrappers=1'.split()
        out = subprocess.check_output(command + [file_path]).decode()
        frame_types = out.replace('pict_type=','').split()
        return zip(range(len(frame_types)), frame_types)
    
    @classmethod
    def _set_dest_path(cls, file_path, basename, dest_path, sep_dir):
        if dest_path is None:
            dest_path = os.path.join(os.path.dirname(file_path), basename)
        elif sep_dir is True:
            dest_path = os.path.join(dest_path, basename)
        if not os.path.isdir(dest_path):
            os.makedirs(dest_path)
        
        return dest_path
    
    @classmethod
    def _save_frames(cls, file_path, dest_path, basename, frame_list):
        cap = cv2.VideoCapture(file_path)
        for frame_no in frame_list:
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
            ret, frame = cap.read()
            destination = os.path.join(dest_path, basename + "_i_frame_" + str(frame_no) + ".jpg")
            cv2.imwrite(destination, frame)
            print ('Saved: ' + destination)
        cap.release()