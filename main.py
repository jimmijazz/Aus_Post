### TO DO ###
# How to get number of shipments in current order
# Make sure tracking works when out of test API

# Size and weight guidelines - http://auspost.com.au/parcels-mail/size-and-weight-guidelines.html
# parcelTypesUrl = "https://"+url_prefix+"/api/postage/parcel/domestic/calculate.json?from_postcode=%s&to_postcode=%s&length=%s&width=%s&height=%s&weight=%s&service_code=%s" % (from_postcode,to_postcode,length,width,height,weight,service_code)

import requests, base64, json
from requests.auth import HTTPBasicAuth

# Load shipment data
with open('shipment_data.json') as json_data:
    shipment_data = json.load(json_data)
json_data.close()

with open('label_data.json') as json_data:
    label_data = json.load(json_data)
json_data.close()

# Order Data
with open('order.json') as json_data:
    order_data = json.load(json_data)
json_data.close()



api_key = '3e031ded-9df2-4893-b899-718d7b482c80'
password = 'x4c51070a98dde071fe4'
account = '1001120582'

headers = {'Content-Type' : 'application/json',"Account-Number":"1001120582"}

# AUSPOST PARAMETERS
from_postcode = "4152"
to_postcode = "2800"
length = "10"
width = "10"
height = "10"
weight = "2"
service_code = "AUS_PARCEL_REGULAR" #The chosen product/service coordinates

url_prefix = "https://digitalapi.auspost.com.au/testbed/shipping/v1/"

def get_account_info(account_number):
    """ 2.1 Returns account info of given account number.

    get_account_info(str) -> dict
    """

    account_url = url_prefix + 'accounts/' + account_number
    parcel_types = requests.get(account_url, auth=(api_key, password))
    print(parcel_types.request.headers)
    # parcel_types.raise_for_status()
    print(parcel_types.json())

def create_shipments (shipments):
    """ 2.3 Creates an order including shipments.
    Post request returns information about the item such as pricing, status etc.

    create_order(dict) -> dict
    """
    parcel_url = url_prefix + 'shipments' # Create URL
    my_parcel = requests.post(parcel_url,headers=headers,auth=(api_key, password),json=shipments)
    print(my_parcel.json())

def get_shipment_by_id (shipment_id):
    """ 2.5 Retrieves the information associated with the shipment shipment_id.

    get_shipments(str) -> dict
    """

    url = url_prefix + 'shipments/' + shipment_id
    shipment = requests.get(url, auth=(api_key, password), headers= headers)
    shipment.raise_for_status()
    print(shipment.json())

def get_shipment_by_status (offset,number_of_shipments,status):
    """ 2.5.2 Retrieves all shipments with given status.

    Offset: Value of first record to be return starting at 0
    Number_of_shipments: Number of records to return in the result

    Acceptable statuses in section 3.2.1. Include:
    Created, Initiated, In Transit, Delivered, Awaiting Collection,
     Possible delay, Unsuccessful pickup, Cancelled, Cannot be delivered.

    get_shipments(str) -> dict
    """

    url = url_prefix + 'shipments?offset={0}&number_of_shipments={1}&status={2}'.format(offset,number_of_shipments,status)

    shipment = requests.get(url, auth=(api_key, password), headers=headers)

    # shipment.raise_for_status()
    print(shipment.json())

def track_item(tracking_number):
    """ Returns delivery events for consignments of articles.
    Can use article ID, consignment ID or barcode ID.

    Can provide multiple comma-seperated tracking numbers ie (123,456,123)

    track_item(str) -> dict
    """
    url = url_prefix + 'track?tracking_ids=' + tracking_number
    tracking = requests.get(url, auth=(api_key, password), headers= headers)
    tracking.raise_for_status()
    print(tracking.json())

def create_label(label_data):
    """ 2.15 Initiates the generation of labels for requested shipments that have
    previously been created.

    create_label(str) -> dict
    """
    url = url_prefix + 'labels'
    label = requests.post(url, auth=(api_key, password), data=json.dumps(label_data), headers= headers)
    print(label.json())

def create_order_from_shipments(shipment_data):
    """ 2.10 Creates an order for the referenced shipments that have previously been
    created using the create shipments service.

    create_order_from_shipments(str) -> dict
    """
    url = url_prefix + 'orders'
    order = requests.put(url,auth=(api_key, password), headers= headers,data=json.dumps(shipment_data))
    print(order.json())

def get_order_summary(order_id):
    """ 2.14 Returns the PDf order summary that contains a charges breakdown of
    the articles in the order.

    get_order_summary(str) -> dict
    """
    url = url_prefix + 'accounts/' + account + "/orders/{0}/summary".format(order_id)
    order_summary = requests.get(url, auth=(api_key, password), headers=headers)
    with open('order.pdf', 'wb') as f:
        f.write(order_summary.content)
# get_account_info(account) # Works
# create_shipments(shipment_data)
# get_shipment_by_id('e4a92bcf282e860624756790')
# create_label(label_data)
# get_shipment_by_status(0,100,'Created')
# create_order_from_shipments(order_data)
get_order_summary('869f6c9b41684fdf')
