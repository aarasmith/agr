# -*- coding: utf-8 -*-
"""
Created on Sun May 29 08:50:07 2022

@author: andya
"""
from dataclasses import dataclass, field
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials
import time
import io
import os
from video_indexer import VideoIndexer
from dotenv import load_dotenv

load_dotenv()

@dataclass
class CustomVision:
    
    _cv_endpoint: str = field(default=os.environ['CV_ENDPOINT'], init=False, repr=False)
    _training_key: str = field(default=os.environ['CV_TRAIN_KEY'], init=False, repr=False)
    _project_id: str = field(default=os.environ['CV_PROJECT_ID'], init=False, repr=False)
    _predictor_endpoint: str = field(default=os.environ['CV_PRED_ENDPOINT'], init=False, repr=False)
    _predictor_key: str = field(default=os.environ['CV_PRED_KEY'], init=False, repr=False)
    _published_name: str = field(default=os.environ['CV_PUBLISHED_NAME'], init=False, repr=False)
    _subscription_key: str = field(default=os.environ['CV_SUBSCRIPTION_KEY'], init=False, repr=False)
    _location: str = field(default=os.environ['CV_LOCATION'], init=False, repr=False)
    _account_id: str = field(default=os.environ['CV_ACCOUNT_ID'], init=False, repr=False)

    @classmethod
    def _init_vi(cls):
        vi = VideoIndexer(vi_subscription_key=cls._subscription_key,
                  vi_location=cls._location,
                  vi_account_id=cls._account_id)
        return vi
    
    @classmethod
    def upload_to_vi(cls, filepath, video_name, video_language = 'ar-SY'):
        vi = cls._init_vi()
        video_id = vi.upload_to_video_indexer(input_filename = filepath,
                                      video_name = video_name,
                                      video_language= video_language)
        return video_id
    
    @classmethod
    def get_vi_insights(cls, video_id, video_language = 'English'):
        vi = cls._init_vi()
        info = vi.get_video_info(video_id, video_language= video_language)
        return info
    
    @classmethod
    def _keyframes_from_insights(cls, video_id, video_language = 'English'):
        info = cls.get_vi_insights(video_id, video_language)
        keyframes = []
        for shot in info["videos"][0]["insights"]["shots"]:
            for keyframe in shot["keyFrames"]:
                keyframes.append(keyframe["instances"][0]['thumbnailId'])
        
        return keyframes
    
    @classmethod
    def preds_from_insights(cls, video_id, video_language = 'English'):
        vi = cls._init_vi()
        prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": cls._predictor_key})
        predictor = CustomVisionPredictionClient(cls._predictor_endpoint, prediction_credentials)
        
        prediction_threshold = .8
        timeout_interval, timeout_time = 5, 10.0
        
        keyframes = cls._keyframes_from_insights(video_id, video_language)
        
        for index, keyframe in enumerate(keyframes):
            if index % timeout_interval == 0:
               print("Trying to prevent exceeding request limit waiting {} seconds".format(timeout_time))
               time.sleep(timeout_time)
        
            # Get KeyFrame Image Byte String From Video Indexer
            img_str = vi.get_thumbnail_from_video_indexer(video_id, keyframe)
        
            # Convert Byte Stream to Image Stream
            img_stream = io.BytesIO(img_str)
        
            # Analyze with Azure Computer Vision
            cv_results = predictor.detect_image(cls._project_id, cls._published_name, img_stream)
            predictions = [pred for pred in cv_results.predictions if pred.probability > prediction_threshold]
            print("Detecting brands in keyframe {}: ".format(keyframe))
        
            if len(predictions) == 0:
               print("No custom brands detected.")
            else:
               for brand in predictions:
                   print("'{}' brand detected with confidence {:.1f}% at location {}, {}, {}, {}".format( brand.tag_name, brand.probability * 100, brand.bounding_box.left, brand.bounding_box.top, brand.bounding_box.width, brand.bounding_box.height))


#computervision_client = ComputerVisionClient(cv_endpoint, CognitiveServicesCredentials(subscription_key))
#trainer.create_images_from_data(project_id, img_stream)
