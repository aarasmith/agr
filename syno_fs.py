# -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 11:18:03 2022

@author: andya
"""

from synology_api import filestation
from dataclasses import dataclass, field
from dotenv import load_dotenv
import os

load_dotenv()
#folder_path = "/Main/Visual/Video projects/Conflict Videos/Syria/Syria Addendum/Doc War Syria Addendum"
@dataclass
class syno_fs:
    
    _syno_ip: str = field(default=os.environ['SYNO_IP'], init=False, repr=False)
    _syno_port: str = field(default=os.environ['SYNO_PORT'], init=False, repr=False)
    _syno_user: str = field(default=os.environ['SYNO_USER'], init=False, repr=False)
    _syno_pass: str = field(default=os.environ['SYNO_PASS'], init=False, repr=False)
    fs: object = field(init=False)        
    
    def __post_init__(self):
        self.fs = filestation.FileStation(self._syno_ip, self._syno_port, self._syno_user, self._syno_pass, secure=False, cert_verify=False, dsm_version=6, debug=True, otp_code=None)
        
    def list_files(self, folder_path):
        return self.fs.get_file_list(folder_path)
        
    def download_file(self, file_path, dest_path):
        self.fs.get_file(file_path, mode="download", dest_path = dest_path)
        return(os.path.join(dest_path, os.path.basename(file_path)))
    
    # fl = filestation.FileStation(syno_ip, syno_port, syno_user, syno_pass, secure=False, cert_verify=False, dsm_version=6, debug=True, otp_code=None)
    # dwn = downloadstation.DownloadStation(syno_ip, syno_port, syno_user, syno_pass, secure=False, cert_verify=False, dsm_version=6, debug=True, otp_code=None)
    # fl.get_file("/Main/File cabinet/R Scripts/aoc_locator.R", mode="download")