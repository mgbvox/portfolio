'''
This script will download the TCIA Lymphoma dataset to the same directly it is run in. NOTE: this will take a while.
'''


import pandas as pd
import pandas
from tciaclient import TCIAClient
import zipfile

KEY = '65547902-6d69-4f5b-9857-fb1e724d3b90' 
client = TCIAClient(apiKey = KEY, baseUrl="https://services.cancerimagingarchive.net/services/v3",resource = "TCIA")

def getResponseString(response):
    try:
        return response.read()
    except:
        pass
    
def download_series(uid, download_dir, zip_name):
    response = client.get_image(uid, download_dir, zip_name)
    strResponseImage = getResponseString(response)
    
    
    
response = client.get_collection_values()
strRespCollections = getResponseString(response)
collections = pandas.io.json.read_json(strRespCollections)

lymph_series_name = collections['Collection'].loc[50]


#Grab the series for CT Lymph Nodes
response = client.get_series(modality="CT", collection=lymph_series_name)
strRespSeries = getResponseString(response)
pdfSeries = pandas.io.json.read_json(strRespSeries)

#Filter so each Series in the collection has >300 images.
#We can filter other things too later if we want.
res = pdfSeries[pdfSeries['ImageCount']>300]


'''
Let's download the data!
'''
import os
if not os.path.isdir(f'./data/{lymph_series_name}'):
    os.mkdir(f'./data/{lymph_series_name}')
    

uids = res.SeriesInstanceUID
download_dir = f'./data/{lymph_series_name}'
for uid in uids:
    print(f'Downloading {uid}...')
    zip_name = uid+'.zip'
    download_series(uid, download_dir, zip_name)
    print(f'Unzipping {uid}...')
    z_path = os.path.join(download_dir,zip_name)
    z = zipfile.ZipFile(z_path)
    out_path = os.path.join(download_dir,uid)
    os.mkdir(out_path)
    z.extractall(out_path)
    z.close()
    print('Next!')
print('Done!')