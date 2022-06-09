# Armed Group Recognition
Module for cleaning archive of video of the Syrian Conflict
Intended to recognize armed group emblems in videos and classify accordingly

###### Completed features:
- Translates filenames into english
- Writes original name and translation into metadata
- Renames or moves and renames filenames as unique 32 char strings
- Extracts scenes-transition frames or I-frames from videos
- Presents frames in GUI for tagging
- Uploads tagged images into Azure Custom Vision project for training

###### Unfinished features:
- Feed videos into Azure VideoIndexer
- Extract VI insights
- Feed VI keyframes to Custom Vision prediction endpoint

###### Planned features:
- Feed local frames to prediction endpoint
- Load file info into sqlite db
- Load VI insights into db
- Load prediction results into db
- Location and date extraction from names where possible
