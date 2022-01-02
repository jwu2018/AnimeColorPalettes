import numpy as np  # linear algebra
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import cv2
from collections import Counter
import urllib
from urllib.request import urlopen, Request

# import urllib.request
# url = 'http://google.com'
# html = urllib.request.urlopen(url).read()
# print(html)


def RGB2HEX(color):
    return "#{:02x}{:02x}{:02x}".format(
        int(color[0]), int(color[1]), int(color[2]))


# def get_image(url):
#   """ Getting the image from a single url"""
#   # download the image, convert it to a NumPy array, and then read
#   # it into OpenCV format
#   # resp = requests.get(url)
#   # image = Image.open(urlopen(url))# np.asarray(bytearray(resp.read()), dtype="uint8")
#   # image = cv2.imdecode(image, cv2.IMREAD_COLOR)
#   url = trim_jpg_url(url)

#   image = cv2.imread(url)
#   image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

#   # resp = requests.get(url, stream=True).raw
#   # image = np.asarray(bytearray(resp.read()), dtype="uint8")
#   # image = cv2.imdecode(image, cv2.IMREAD_COLOR)
#   response = requests.get(url)
#   img = Image.open(BytesIO(response.content))
#   return img

# def og_get_image(image_path):
#     image = cv2.imread(image_path)
#     image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#     return image


# def get_image(url, readFlag=cv2.IMREAD_COLOR):
#   """Getting the image from a single url using cv2 and urllib"""
#   req = requests.get(trim_jpg_url(url))
#   print("got the http response: ", req)
#   print(bytearray(req.read()))
#   print(dtype=np.uint8)
#   arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
#   print("array: ", arr)
#   img = cv2.imdecode(arr, -1)  # 'Load it as it is'

#   print('returning type:', type(img))

#   # return the image
#   # cv2.imshow('awexranweornxauwex', img)
#   return img



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








def trim_jpg_url(url):
    # return url
    return url.split('?')[0]


def get_colors(image_url, number_of_colors):
  """
  Get color palette pie chart for a single image
    @param image_url = file path or url to the image
  """
  # resize image so computer doesn't take as long
  modified_image = cv2.resize(image_url, (600, 400), interpolation=cv2.INTER_AREA)
  modified_image = modified_image.reshape(modified_image.shape[0] * modified_image.shape[1], 3)
  # print('modified image')

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

  print('finished making pie chart')
  return rgb_colors
