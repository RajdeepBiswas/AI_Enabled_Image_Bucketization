# -------------------------------------------------------------------------
# File: storage.py
# Name: Rajdeep Biswas
# Date: 06/06/2019
# Desc: This module will expose 'BlobOperations' class and it's methods
# Copyright (c) Rajdeep Biswas. All rights reserved.
# Licensed under the MIT License. See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

from PIL import Image,ExifTags
from PIL.ExifTags import TAGS, GPSTAGS
from io import BytesIO
import requests

# --------------------------------------------------------------------------
# Class: ImageData
# Desc: This class will expose various methods for operating on a Blob
#       object using sas token based authorization.
# Param 1: Type: String Name: account Desc: Azure Blob Storage Account Name
# Param 2: Type: String Name: key Desc: Azure Blob Storage Account Key
# --------------------------------------------------------------------------
class ImageData():
    def __init__(self, storage_account_name, container_name, blob_object, sas_date_expiry, sas_date_start, sas_token):
        self.storage_account_name = storage_account_name
        self.container_name = container_name
        self.blob_object = blob_object
        self.sas_date_expiry = sas_date_expiry        
        self.sas_date_start = sas_date_start
        self.sas_token = sas_token
        self.image_url="https://{}.blob.core.windows.net/{}/{}?sv=2018-03-28&ss=bfqt&srt=sco&sp=rwdlacup&se={}&st={}&spr=https,http&sig={}".format(self.storage_account_name, self.container_name, self.blob_object, self.sas_date_expiry, self.sas_date_start, self.sas_token)
        self.image = Image.open(BytesIO(requests.get(self.image_url).content))

    # --------------------------------------------------------------------------
    # Method: ImageData.get_image_metadata
    # Desc: This method return object metadata value
    # Param 1: Type: str Name: tag_name Desc: The metadata tag to fecth
    # --------------------------------------------------------------------------
    def get_image_metadata(self, tag_name):

        self.exif_data = {}
        self.tag_name = tag_name
        try:
            info = self.image._getexif()
            if info:
                for tag, value in info.items():
                    decoded = TAGS.get(tag, tag)
                    if decoded == "GPSInfo":
                        gps_data = {}
                        for gps_tag in value:
                            sub_decoded = GPSTAGS.get(gps_tag, gps_tag)
                            gps_data[sub_decoded] = value[gps_tag]

                        self.exif_data[decoded] = gps_data
                    else:
                        self.exif_data[decoded] = value

            return self.exif_data[self.tag_name]
        except Exception as e:
            return e
            
    # --------------------------------------------------------------------------
    # Method: ImageData._decimal_conversion
    # Desc: Helper function to convert the GPS coordinates to decimal
    # Param 1: Type: str Name: tag_name Desc: The metadata tag to fecth
    # --------------------------------------------------------------------------           
    def _decimal_conversion(self, value):
        deg_num, deg_denom = value[0]
        v_degrees = float(deg_num) / float(deg_denom)

        min_num, min_denom = value[1]
        v_minutes = float(min_num) / float(min_denom)

        sec_num, sec_denom = value[2]
        v_seconds = float(sec_num) / float(sec_denom)
        
        return v_degrees + (v_minutes / 60.0) + (v_seconds / 3600.0)

    # --------------------------------------------------------------------------
    # Method: ImageData.get_image_geo_data
    # Desc: This method return object metadata value
    # Param 1: Type: str Name: tag_name Desc: The metadata tag to fecth
    # --------------------------------------------------------------------------
    def get_image_geo_data(self, tag_name):
        self.extracted_location_data = {}
        self.location_data = self.get_image_metadata('GPSInfo')
        #print(self.location_data)
        self.latitude = None
        self.longitude = None
        self.tag_name = tag_name        
        self.gps_latitude = self.location_data.get("GPSLatitude")
        self.gps_latitude_ref = self.location_data.get('GPSLatitudeRef')
        self.gps_longitude = self.location_data.get('GPSLongitude')
        self.gps_longitude_ref = self.location_data.get('GPSLongitudeRef')

        if self.gps_latitude and self.gps_latitude_ref and self.gps_longitude and self.gps_longitude_ref:
            self.latitude = self._decimal_conversion(self.gps_latitude)
            if self.gps_latitude_ref != "N":                     
                self.latitude *= -1

            self.longitude = self._decimal_conversion(self.gps_longitude)
            if self.gps_longitude_ref != "E":
                self.longitude *= -1
        self.extracted_location_data['Latitude'] = self.latitude
        self.extracted_location_data['Longitude'] = self.longitude
        self.extracted_location_data['Coordinates'] = "{},{}".format(self.latitude,self.longitude)
        try:  
            return self.extracted_location_data[self.tag_name]
        except Exception as e:
            return e            

    def __del__(self):
        print('Object instance destructed!!!')
