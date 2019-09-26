import urllib
import json

# Get the dataset metadata by passing package_id to the package_search endpoint
# For example, to retrieve the metadata for this dataset:

url = "https://ckan0.cf.opendata.inter.prod-toronto.ca/api/3/action/package_show"
params = { "id": "f816b362-778a-4480-b9ed-9b240e0fe9c2"}
response = urllib.request.urlopen(url, data=bytes(json.dumps(params), encoding="utf-8"))
package = json.loads(response.read())
print(package)

# Get the data by passing the resource_id to the datastore_search endpoint
# See https://docs.ckan.org/en/latest/maintaining/datastore.html for detailed parameters options
# For example, to retrieve the data content for the first resource in the datastore:

for idx, resource in enumerate(package["result"]["resources"]):
    if resource["datastore_active"]:
        url = "https://ckan0.cf.opendata.inter.prod-toronto.ca/api/3/action/datastore_search"
        p = { "id": resource["id"] }
        r = urllib.request.urlopen(url, data=bytes(json.dumps(p), encoding="utf-8"))
        data = json.loads(r.read())
        print(data)
        break

# Step -2 Analyze it :) !! 

import pandas as pd
from collections import Counter

data=pd.read_csv("/Users/patel/Downloads/Highrise Inspections Data.csv")

data.head(5)
data.info()

description=data.iloc[:,7] # Fetching column : with description
description_processed=description.str.strip() # Remove spaces
description_processed.isnull().sum() # No of Nan values 
len(description_processed.unique().tolist()) # No of categories , unique values in violation desctiption

Counter = Counter(description_processed) 

# most_common() produces k frequently encountered 
# input values and their respective counts. 

n=10
most_occur = Counter.most_common(10) #[:-n-1:-1] uncomment this if you want to get least common items
print(most_occur) 

# Step 3: As we have latitude's and longitude we can plot on a toronto map to analyze the common areas where violations were found.
# You will need to get mapbox api token no and use that api. 

import plotly.express as px
import plotly.graph_objects as go

mapbox_access_token = "pk.eyJ1IjoiYWF5dXNocGF0ZWwwMDciLCJhIjoiY2swaXh0NWF0MDR3bzNpcW9tbW9rc2hlYyJ9.iwnJqHGlDbm14f0ecqJUEQ"

fig = go.Figure(go.Scattermapbox(

        lat=data.iloc[:,3].values.tolist(),
      #  lat=['43.651070'],
       # lon=['-79.347015'],
        lon=data.iloc[:,4].values.tolist(),
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=10
        ),
        text=data.iloc[:,5]+"  "+ data.iloc[:,7]
        #text=['Toronto']
    ))

fig.update_layout(
    autosize=True,

    hovermode='closest',
    mapbox=go.layout.Mapbox(
        accesstoken=mapbox_access_token,
        bearing=0,
        center=go.layout.mapbox.Center(
            lat=43.6532, # Toronto Coordinates
            lon=-79.3832
        ),
        pitch=0,
        zoom=11
    ),
)

fig.show() # This will open a browser and display a map ! Enjoy !! :)

