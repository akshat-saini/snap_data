import requests
from bs4 import BeautifulSoup
from connection import collection
from io import BytesIO
from PIL import Image
import re


# Profile URL
profile_url = "https://www.snapchat.com/add/raju_rastog9362?web_client_id=a0dfde06-5c36-441f-afff-671e6b1ebc77"

# Send an HTTP GET request to the profile URL
response = requests.get(profile_url)
soup = BeautifulSoup(response.content, 'html.parser')

script_tag = soup.find('script', {'type': 'application/ld+json'})
json_data = script_tag.string.strip()
    
# Convert JSON string to a Python dictionary
data_dict = eval(json_data)
profile_name = data_dict.get('alternateName')
name = data_dict.get('name')
description = data_dict.get('description')
address = data_dict.get('address')



meta_description = soup.find('meta', {'data-react-helmet': 'true', 'name': 'description'})
description_content = meta_description.get('content')

# Use regular expressions to extract the subscribers count
subscribers_match = re.search(r'(\d+(\.\d+)?)k Subscribers', description_content)
if subscribers_match:
    subscriber_count = subscribers_match.group(0)
else:
    subscriber_count = "No subscriber"

# Find the profile picture URL
if soup.find('img',{'alt': 'Profile Picture'}):
    profile_picture_url = soup.find('img', {'alt': 'Profile Picture'})['srcset']
    profile_picture_response = requests.get(profile_picture_url)
    profile_picture = Image.open(BytesIO(profile_picture_response.content))

    # Convert the image to bytes
    image_bytes = BytesIO()
    profile_picture.save(image_bytes, format="JPEG")
    profilePicture = image_bytes.getvalue()
else:
    profilePicture = "Profile picture not available of this user."


document = {
    "profilePicture":profilePicture,
    "userName":profile_name if profile_name else "Username not available",
    "name":name if name else "Name not available",
    "description":description if description else "No Description available",
    "address":address if address else "No address available",
    "subscriberCount":subscriber_count
}

collection.insert_one(document)
