import secrets_keys.config as config
from modules.storage import BlobOperations

file_handler = BlobOperations(config.STORAGE_ACCOUNT_NAME,config.STORAGE_ACCOUNT_KEY)
#file_handler = BlobOperations(config.STORAGE_ACCOUNT_NAME,'sasa')
file_handler.print_blob_file('tmp', 'ImpPythonsetupnotes.txt')
file_handler = 'destroy'