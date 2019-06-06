import secrets_keys.config as config
from modules.storage import BlobOperations
from modules.image import ImageData

import matplotlib.pyplot as plt
from PIL import Image,ExifTags
from io import BytesIO
import requests

from pygeocoder import Geocoder

import json

#file_handler = BlobOperations(config.STORAGE_ACCOUNT_NAME,config.STORAGE_ACCOUNT_KEY)
#file_handler = BlobOperations(config.STORAGE_ACCOUNT_NAME,'sasa')
#file_handler.print_blob_file('tmp', 'ImpPythonsetupnotes.txt')
#image_data=file_handler.get_blob_bytes('staging', 'test_images/20180114_153529.jpg')


#image_url='https://blob9cognitive.blob.core.windows.net/staging/test_images/20180114_153529.jpg?sv=2018-03-28&ss=bfqt&srt=sco&sp=rwdlacup&se=2021-02-07T02:42:57Z&st=2019-06-06T17:42:57Z&spr=https,http&sig=tlrNJ%2FL8lDJgmMNGSI2iFNsrIOLg6IrdzvS0pscJuU0%3D'
#image_data = open(image_path, "rb").read()
container_name='staging'
blob_object='test_images/20180114_153529.jpg'
sas_token='tlrNJ%2FL8lDJgmMNGSI2iFNsrIOLg6IrdzvS0pscJuU0%3D'
sas_date_start='2019-06-06T17:42:57Z'
sas_date_expiry='2021-02-07T02:42:57Z'
image_url="https://blob9cognitive.blob.core.windows.net/{}/{}?sv=2018-03-28&ss=bfqt&srt=sco&sp=rwdlacup&se={}&st={}&spr=https,http&sig={}".format(container_name, blob_object, sas_date_expiry, sas_date_start, sas_token)

#image1=requests.get(image_url)
#image2 = Image.open(BytesIO(requests.get(image_url).content))
#exif = { ExifTags.TAGS[k]: v for k, v in image2._getexif().items() if k in ExifTags.TAGS }    
#print(exif['GPSInfo'])
#print(exif['ExifImageWidth'])
#print(exif['ExifImageHeight'])
#print(exif['ExifImageHeight'])
#dimension="Dimension - {} x {} pixels".format(exif['ExifImageWidth'],exif['ExifImageHeight'])
#print(dimension)
#print(dir(image1))
#print("\n---------\n")
#print(exif)

#image = Image.open(BytesIO(requests.get(image_url).content))

#image = Image.open(BytesIO(image_data))
#plt.imshow(image)
#plt.axis("off")
#image=Image.open(image_data)
#exif = { ExifTags.TAGS[k]: v for k, v in image._getexif().items() if k in ExifTags.TAGS }    
#print(exif['GPSInfo'])
#plt.show()
#file_handler = 'destroy'


my_image=ImageData(config.STORAGE_ACCOUNT_NAME, config.CONTAINER_NAME, config.BLOB_OBJECT, config.SAS_DATE_EXPIRY, config.SAS_DATE_START, config.SAS_TOKEN)
#print(my_image.get_image_metadata('Dimension'))
#print("\n---------\n")
#dict=my_image.get_image_metadata('GPSInfo')
#print("Latitude")   
#print(dict[2][2][0])
#latitude=(dict[2][2][0])/(dict[2][2][1])
#print(latitude) 
#print("Longitude")   
#print(dict[4][2][0])
#Longitude=(dict[4][2][0])/(dict[2][2][1])
print(my_image.get_image_metadata('GPSInfo'))
print("\n---------\n")    
print(my_image.get_image_geo_data('Coordinates'))
print("\n---------\n")

coordinates=my_image.get_image_geo_data('Coordinates')
map_key=config.MAP_DEV_KEY

image_url='http://dev.virtualearth.net/REST/v1/Locations/{}?key={}'.format(coordinates,map_key)

image_data = requests.get(image_url)
analysis = image_data.json()
print(analysis)
#print(dir(analysis))
#print(analysis.get('resourceSets')[resources])

json.dumps(analysis)
print("\nFull address\n")
print(analysis['resourceSets'][0]['resources'][0]['name'])
print("\nLocation\n")
print(analysis['resourceSets'][0]['resources'][0]['address']['locality'])
#json_dict=json.loads(analysis['resourceSets'][0])

#print(json_dict)
#lat=my_image.get_image_geo_data('Latitude')
#longi=my_image.get_image_geo_data('Longitude')

# Convert longitude and latitude to a location
#results = Geocoder.reverse_geocode(lat, longi)    
#print(results.city)

#results = Geocoder.reverse_geocode(31.3372728, -109.5609559)   
#print(results.city)
#image_url='http://dev.virtualearth.net/REST/v1/Locations/31.3372728,-109.5609559?key=AmnFsl3pcx22YoSJi2mMpUb9ZRcrcNsrK2pLA5rI71RIZG24zO7cFQaCJh-pJCyp'
#image_data = Image.open((requests.get(image_url).content))
#image_data.json
#image_url='http://dev.virtualearth.net/REST/v1/Locations/27.5986,33.6891?key=AkMeAQ_es_tPb-6I3llHpQ7HkjA1pLInPg3SYa-MRBawspA0ci7tZUQAb3Gl3taF'

#response = requests.get(image_url)
#response.raise_for_status()
#print(response)
#print("\n---------\n")
# The 'analysis' object contains various fields that describe the image. The most
# relevant caption for the image is obtained from the 'description' property.
#analysis = response.json()
#print(analysis)

#image_caption = analysis["description"]["captions"][0]["text"].capitalize()


