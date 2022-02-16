import requests
import cv2 as cv 
from google.colab.patches import cv2_imshow
from skimage import io
from PIL import Image 
import matplotlib.pyplot as plt
from wordcloud import WordCloud


api_key = 'acc_da959b82113a057'
api_secret = '3d765a2b3769019d51897fdd864b3acf'

def get_tags(image_url):

  #  display the image using html url
  image = io.imread(image_url)
  image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
  cv2_imshow(image)

  #  connect to api and get first 12 generated tags, displat under the image
  try:
    response = requests.get(
        'https://api.imagga.com/v2/tags?image_url=%s' % image_url,
        auth=(api_key, api_secret))
    json_data = response.json()
    count = 0
    for i in range(len(['result'])+1):
        while count <12:
            tag = (json_data['result']['tags'][i+count]['tag']['en'])
            count += 1
            print(f"\033[1;37;40m {tag} \033[0;37;40m", end=" | ")

  #  generated word cloud from first 20 generated tags
    dictionary = {}
    count = 0
    for i in range(len(['result'])+1):
            while count <20:
                tag = (json_data['result']['tags'][i+count]['tag']['en'])
                confidence = (json_data['result']['tags'][i+count]['confidence'])
                dictionary[tag]=confidence
                count += 1
                if len(dictionary)==20:
                  wc = WordCloud(background_color="white",width=4000,height=2000, max_words=20,relative_scaling=0.5,normalize_plurals=False).generate_from_frequencies(dictionary)
                  plt.imshow(wc)

  except:
    print("Could not generate tag")

  

get_tags("https://i.ibb.co/hXQTm5f/XOHr-Gxlq-RDC1-PRVA4nbh-OKSf-As-Oo-W5-Bii1-CGep-Jr.jpg")
print('\n')

get_tags("https://i.ibb.co/K9V0QVZ/david-suarez-Noy-V5ciwwmg-unsplash-1.jpg")
print('\n')

get_tags("https://i.ibb.co/J5bW9PT/succulents-flowers-plant-110695-3840x2400.jpg")
print('\n')



