# Returns parcel information and cost from Australia Post API

import requests, json

# Size and weight guidelines - http://auspost.com.au/parcels-mail/size-and-weight-guidelines.html

api_key = 'YOUR_API_HERE'
headers = {"AUTH-KEY": api_key}

# AUSPOST PARAMETERS
from_postcode = "4152"
to_postcode = "2800"
length = "10"
width = "10"
height = "10"
weight = "2"
service_code = "AUS_PARCEL_REGULAR" #The chosen product/service coordinates

url_prefix = "auspost.com.au"
parcelTypesUrl = "http://"+url_prefix+"/api/postage/parcel/domestic/calculate.json?from_postcode=%s&to_postcode=%s&length=%s&width=%s&height=%s&weight=%s&service_code=%s" % (from_postcode,to_postcode,length,width,height,weight,service_code)

try:
    # Assign api_key to AUTH-KEY in header
    parcel_types = requests.get(parcelTypesUrl,headers=headers)
    print(parcel_types.json())
except:
    parcel_types.raise_for_status()
