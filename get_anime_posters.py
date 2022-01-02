import json
import pandas as pd
import requests
from PIL import Image
import requests
from io import BytesIO


def get_animes_df(category, num_pages=1):
  """Returns information for the top animes of a given category

  Args:
      category (string): the given category
      num_pages (int): pages of animes to return (each page has 10 animes)

  Returns:
      dataframe: information for the top animes of the category
  """
  
  basepath = 'https://kitsu.io/api/edge/anime'
  animes = pd.DataFrame()

  # get the animes for the category
  for page in range(num_pages):
    # each page in the api has only 10 animes
    url = basepath + '?page[limit]=10&page[offset]=' + str(page*10) + '&filter[categories]=' + category + "&sort=popularityRank"
    # print("URL = " + url)
    d = requests.get(url)
    # get the json content from the url, add to dataframe
    j = json.loads(d.content)
    df = pd.json_normalize(j, 'data')
    animes = animes.append(df)

  animes.reset_index(drop=True, inplace=True)
  
  # get the relevant columns only
  to_keep = ['attributes.updatedAt','attributes.canonicalTitle','attributes.startDate',
             'attributes.endDate','attributes.posterImage.large']
  return animes[to_keep]




def get_image(url):
  """Returns the image from the url as an Image object

  Args:
      url (string): the url that leads to the image

  Returns:
      Image: the image at the url
  """
  response = requests.get(url)
  img = Image.open(BytesIO(response.content))
  # img.show()
  return img



def combine_images(cat_animes, cat_name):
  """Combine multiple anime poster images for a given category

  Args:
      cat_animes (dataframe): information for the top animes of the category
      cat_name (string): the name of the given category

  Returns:
      Image: an image that combines the anime posters horizontally
  """

  images = []

  for url in cat_animes['attributes.posterImage.large'].to_numpy():
    images.append(get_image(url))
  print('got all images for', cat_name)
  # specify width and height for new image
  widths, heights = zip(*(i.size for i in images))
  total_width = sum(widths)
  max_height = max(heights)
  # new empty image
  combine_im = Image.new('RGB', (total_width, max_height))
  print('new empty image for', cat_name)
  # put the images together in combine_im
  x_offset = 0
  for im in images:
      combine_im.paste(im, (x_offset, 0))
      x_offset += im.size[0]
  print('combined image for', cat_name)
  
  # save the image and return it
  name_str = 'combined_images_2/' + cat_name + '.jpg'
  combine_im.save(name_str)
  return combine_im