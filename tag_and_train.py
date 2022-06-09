# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 14:01:25 2022

@author: andya
"""

from dataclasses import dataclass
import cv2
from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateBatch, ImageFileCreateEntry, Region
from msrest.authentication import ApiKeyCredentials
import os
from dotenv import load_dotenv

load_dotenv()

#filepath = "D:/agr/1193ca6bb36440a0a3000e581742a605/1193ca6bb36440a0a3000e581742a605_i_frame_127.jpg"
#folder_path = "D:/agr/1193ca6bb36440a0a3000e581742a605/"

@dataclass
class tag_and_train:
    
    _cv_endpoint: str = os.environ['CV_ENDPOINT']
    _training_key: str = os.environ['CV_TRAIN_KEY']
    _project_id: str = os.environ['CV_PROJECT_ID']
    
    @classmethod
    def _tag_image(cls, filepath):
        image = cv2.imread(filepath)
        tag_zone = cv2.selectROI(image)
        cv2.destroyAllWindows()
        
        im_height = image.shape[0]
        im_width = image.shape[1]
        
        left = tag_zone[0] / im_width
        top = tag_zone[1] / im_height
        width = tag_zone[2] / im_width
        height = tag_zone[3] / im_height
        
        if sum(tag_zone) == 0:
            return [0,0,0,0]
        
        return [left, top, width, height]
    
    @classmethod
    def tag_images(cls, folder_path):
        file_list = os.listdir(folder_path)
        region_dict = {}
        for file in file_list:
            basename = os.path.splitext(os.path.basename(file))[0]
            region_dict[basename] = cls._tag_image(os.path.join(folder_path, file))
        
        filtered_region_dict = {}
        for (key, value) in region_dict.items():
            if sum(value) > 0:
                filtered_region_dict[key] = value
        return filtered_region_dict
    
    @classmethod
    def load_tagged_images(cls, folder_path, tag_id):
        credentials = ApiKeyCredentials(in_headers={"Training-key": cls._training_key})
        trainer = CustomVisionTrainingClient(cls._cv_endpoint, credentials)
        
        image_regions = cls.tag_images(folder_path)
        
        tagged_images_with_regions = []
        for file_name in image_regions.keys():
            x,y,w,h = image_regions[file_name]
            regions = [Region(tag_id=tag_id, left=x, top=y, width=w, height=h)]
            
            with open(os.path.join(folder_path, file_name + ".jpg"), mode='rb') as image_contents:
                tagged_images_with_regions.append(ImageFileCreateEntry(name=file_name, contents=image_contents.read(), regions=regions))
        
        upload_result = trainer.create_images_from_files(cls._project_id, ImageFileCreateBatch(images=tagged_images_with_regions))
        if not upload_result.is_batch_successful:
            print("Image batch upload failed.")
        for image in upload_result.images:
            print("Image status: ", image.status)
        return
        


