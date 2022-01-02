import numpy as np  # linear algebra
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import cv2
from collections import Counter
from urllib.request import urlopen, Request
from PIL import Image
import requests
from matplotlib import cm


def RGB2HEX(color):
    return "#{:02x}{:02x}{:02x}".format(
        int(color[0]), int(color[1]), int(color[2]))



def trim_jpg_url(url):
    # return url
    return url.split('?')[0]



def get_image(url):
  """Returns the image as a matrix using the given url"""
  # trim the url
  url = trim_jpg_url(url)
  # request to read the file or something to avoid the 403 error
  req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
  resp = urlopen(req).read()
  # convert the image to a NumPy array
  image = np.asarray(bytearray(resp), dtype="uint8")
  # read the image into OpenCV format
  image = cv2.imdecode(image, cv2.IMREAD_COLOR)
  # convert GRB to RGB
  image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
  return image



def get_url_list(animes_df):
  url_list = []
  
  for poster_url in animes_df['attributes.posterImage.medium']:
    poster_url = trim_jpg_url(poster_url)
    url_list.append(poster_url)

  return url_list



def combine_images(img_list, name="combined"):
  """Combine multiple images into one big one"""
  images = []

  for url in img_list:
    images.append(Image.fromarray(np.uint8(get_image(url))))

  # make heights and widths all the same
  widths, heights = zip(*(i.size for i in images))
  total_width = sum(widths)
  max_height = max(heights)
  # new empty image
  new_im = Image.new('RGB', (total_width, max_height))
  # put the images together in new_im
  x_offset = 0
  for im in images:
      new_im.paste(im, (x_offset, 0))
      x_offset += im.size[0]

  name_str = 'combined_images/' + name + '.jpg'
  new_im.save(name_str)

  return new_im













def get_colors(image_url, number_of_colors):
  """
  Get color palette pie chart for a single image
    @param image_url = file path or url to the image
  """
  # resize image so computer doesn't take as long
  modified_image = cv2.resize(image_url, (600, 400), interpolation=cv2.INTER_AREA)
  modified_image = modified_image.reshape(modified_image.shape[0] * modified_image.shape[1], 3)

  clf = KMeans(n_clusters=number_of_colors)
  labels = clf.fit_predict(modified_image)

  counts = Counter(labels)
  # sort to ensure correct color percentage
  counts = dict(sorted(counts.items()))

  center_colors = clf.cluster_centers_
  # We get ordered colors by iterating through the keys
  ordered_colors = [center_colors[i] for i in counts.keys()]
  hex_colors = [RGB2HEX(ordered_colors[i]) for i in counts.keys()]
  rgb_colors = [ordered_colors[i] for i in counts.keys()]
  # print('got colors')

  plt.figure(figsize=(4, 3))
  plt.pie(counts.values(), colors=hex_colors)
  plt.savefig('test.png')

  # print('finished making pie chart')
  return rgb_colors




def get_colors_mult_img(img_list, number_of_colors, image_filename):
  """
  Get an overall color palette pie chart from multiple images
    @param img_list: list of the URLs of the images
  """
  # combine the images
  big_image = combine_images(img_list)

  # convert the Image object into an ndarray
  big_img_np = np.array(big_image)
  rs_big_img_np = big_img_np.reshape(big_img_np.shape[1], -1)

  # get 200 clusters so the colors don't turn out brown
  clf = KMeans(n_clusters = 75)
  labels = clf.fit_predict(rs_big_img_np)
  print(labels)

  counts = Counter(labels)
  # sort to ensure correct color percentage
  counts = dict(sorted(counts.items()))
  print(counts)

  center_colors = clf.cluster_centers_
  # We get ordered colors by iterating through the keys
  ordered_colors = [center_colors[i] for i in counts.keys()]
  hex_colors = [RGB2HEX(ordered_colors[i]) for i in counts.keys()]
  rgb_colors = [ordered_colors[i] for i in counts.keys()]
  
  # getting the first number_of_colors from the lists + dictionary
  counts = {k: counts[k] for k in list(counts)[:number_of_colors]}
  ordered_colors = ordered_colors[0:number_of_colors]
  hex_colors = hex_colors[0:number_of_colors]
  rgb_colors = rgb_colors[0:number_of_colors]

  plt.figure(figsize=(3, 3))
  plt.pie(counts.values(), colors=hex_colors)
  plt.savefig(image_filename + '.png')

  return rgb_colors
