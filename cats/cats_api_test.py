import requests

import pandas as pd
from collections import OrderedDict


url = 'https://query.wikidata.org/sparql'

# wdt:P31  <--> https://www.wikidata.org/wiki/Property:P31 <--> means: "INSTANCE OF"
# wd:Q146  <-->  https://www.wikidata.org/wiki/Q146        <--> means: "HOUSE CAT"

query = """
SELECT ?item ?itemLabel 
WHERE 
{
  ?item wdt:P31 wd:Q146.
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}
"""


r = requests.get(url, params = {'format': 'json', 'query': query})
data = r.json()

print("\n\nHere is our wikidata results in the form of JSON string. It contains the data we want with a bunch of other junk:")
print(data)
print("\n")

cats = []  #start it as an empty list.

# Extract out the stuff we want from the junk by treating the JSON as a python dictionary
# and then surgically pulling what we care about.  We load this stuff into a Python.
for this_item in data['results']['bindings']:
    cats.append(OrderedDict({
        'kitty_url': this_item['item']['value'],
        'kitty_name': this_item['itemLabel']['value']
    }))

# Convert our python list into a Pandas dataframe named 'df':
df = pd.DataFrame(cats)

# Very Optional...If we want to remove the ugly index numbering (0,1,2,3, ..) and replace the index with the kitty_name, we can.
# df.set_index('kitty_name', inplace=True)

#show a sampling of our cats from our dataframe.
print(df.head(5))

# How many cats do we have in our dataframe
print(f"\n\n...We have {len(df)} cats in our dataframe. Oh, yeah.")
