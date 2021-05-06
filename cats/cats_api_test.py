# imports installed from pypi.org:
import requests
import pandas as pd

# imports from python's standard library:
from collections import OrderedDict

url = 'https://query.wikidata.org/sparql'

# wdt:P31  <--> https://www.wikidata.org/wiki/Property:P31 <--> means: "INSTANCE OF"
# wd:Q146  <-->  https://www.wikidata.org/wiki/Q146        <--> means: "HOUSE CAT"

# This query is from https://www.wikidata.org/wiki/Wikidata:SPARQL_query_service/queries/examples#Cats
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

print("\n\nHere is our wikidata results in the form of JSON string. It contains the data we truly want along with a bunch of other junk:")
# show the JSON data.
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

# Very Optional...If we want to remove the 'ugly' numerical indexing (0,1,2,3, ..) and replace the index with the kitty_name, we could.
# df.set_index('kitty_name', inplace=True)

# Show a sampling of our cats from our dataframe.
print("\nSample of first few cats...")
df['kitty_lowercase'] = df['kitty_name'].str.lower()
print(df.loc[df['kitty_lowercase'].str.contains("sock"),['kitty_url','kitty_name']].head(5))

# Just showing how pandas syntax works for filtering rows and selecting columns.
print("\nCats with 'sock' in their name")
df['kitty_lowercase'] = df['kitty_name'].str.lower()
print(df.loc[df['kitty_lowercase'].str.contains("sock"),['kitty_url','kitty_name']].head(5))

# And, how many cat names do we have in our dataframe, in total?
print(f"\n\n...We have {len(df)} cats in our dataframe. Oh, yeah.")
