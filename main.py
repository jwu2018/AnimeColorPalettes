import get_categories
import pandas as pd
import get_anime_posters
# import get_posters
# import test_poster
# import get_palette
import time

#================================================
#                Get Categories
#================================================
# cats = get_categories.get_cats_df()
# cats.to_csv('categories.csv')
cats = pd.read_csv('categories.csv')

#================================================
#                Get Anime Posters
#================================================
not_include = ['Tentacle','Loli','Super Deformed', 'Voyeurism', 'Ahegao', 'Netorare', 'Ecchi', 'Slavery', 'Dark Skinned Girl', 'Female Teacher', 'Female Student', 'Content Indicators', 'Dynamic', 'Elements', 'Setting', 'Themes', 'Yaoi', 'Target Demographics', 'Anime Influenced', 'Housewives']

# for i in range(len(cats)):
for i in range(85,len(cats)):
  cat = cats['category'][i]
  cat = "%20".join(cat.split())

  if not cats['category'][i] in not_include:
    print(i, cat)
    cat_animes = get_anime_posters.get_animes_df(cat, 1)
    cat_animes.dropna(subset=['attributes.canonicalTitle'], inplace=True)
    # combine the posters into a single image and save it
    get_anime_posters.combine_images(cat_animes, cat)
  else:
    print('bad category:', cat)
    
  # prevent rate limits
  if i % 10 == 0 and i != 0:
    print("waiting a bit so we aren't rate limited")
    time.sleep(60)

# adv_animes = pd.read_csv('adventure_animes.csv')

# urls = get_posters.get_image_urls(adv_animes)
# get_posters.get_colors_mult_img(urls, 8, True)

# url = get_posters.get_image('https://media.kitsu.io/anime/poster_images/16/original.jpg') 
# get_posters.get_colors(url, 8, True)

# url = test_poster.get_image('https://media.kitsu.io/anime/poster_images/24/original.jpg')
# NARUTOOOOOOO
# test_poster.get_colors(url, 10)