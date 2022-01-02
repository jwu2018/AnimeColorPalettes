import json
import pandas as pd
import requests

"""
Gets all anime categories from the Kitsu
API, returns it, and saves it as a csv file.
"""
def get_cats_df():
  categories = pd.DataFrame()
  # first page
  basepath = 'https://kitsu.io/api/edge/categories?fields[categories]=title&page[limit]=10'
  url = basepath

  # get all of the categories from the kitsu api (218 categories)
  for page in range(22):
    # each page in the api has only 10 categories
    if page > 0:
      url = basepath + '&page[offset]=' + str(page*10)
    # get the json from the page, add to dataframe
    d = requests.get(url)
    j = json.loads(d.content)
    df = pd.json_normalize(j, 'data')
    categories = categories.append(df)
    
  # drop all categories except category name
  categories = categories.drop(columns=['links.self','type','id'])
  categories.rename(columns={'attributes.title':'category'}, inplace=True)
  # reset indices
  categories.reset_index(inplace = True, drop = True)
  # save as csv
  categories.to_csv('categories.csv', index = False)
  
  return categories