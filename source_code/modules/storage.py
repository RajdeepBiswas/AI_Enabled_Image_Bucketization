# -------------------------------------------------------------------------
# File: storage.py
# Name: Rajdeep Biswas
# Date: 06/05/2019
# Desc: This module will expose 'BlobOperations' class and it's methods
# Copyright (c) Rajdeep Biswas. All rights reserved.
# Licensed under the MIT License. See LICENSE.txt in the project root for
# license information.
# --------------------------------------------------------------------------

from azure.storage.blob import BlockBlobService
import azure.common

# --------------------------------------------------------------------------
# Class: BlobOperations
# Desc: This class will expose various methods for operating on a Blob 
#       Storage account. This can include listing, printing contents,
#       uploading objects, deleting objects etc.
# Param 1: Type: String Name: account Desc: Azure Blob Storage Account Name
# Param 2: Type: String Name: key Desc: Azure Blob Storage Account Key
# --------------------------------------------------------------------------
class BlobOperations():
    def __init__(self, account,key):
        self.account = account
        self.key = key

    # --------------------------------------------------------------------------
    # Method: BlobOperations.print_blob_file
    # Desc: This method will print the content of a non-binary Blob file 
    # Param 1: Type: str Name: container_name Desc: Blob Container Name
    # Param 2: Type: str Name: blob_name Desc: Blob File Name
    # --------------------------------------------------------------------------        
    def print_blob_file(self,container_name,blob_name):
        self.container_name = container_name
        self.blob_name = blob_name
        try:
            block_blob_service = BlockBlobService(account_name=self.account, account_key=self.key)
            #Get the file handler
            file = block_blob_service.get_blob_to_text(self.container_name,self.blob_name)
            content = file.content
            print(content) 
        except azure.common.AzureHttpError:
            print("\n__ERROR__: The specified account name or the associated key is not correct.\n")            
        except azure.common.AzureMissingResourceHttpError:
            print("\n__ERROR__: The specified conatiner or the blob file does not exists.\n")

    def __del__(self):
        print('Object instance destructed!!!')
