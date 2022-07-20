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



def face_detect(image_url):

  #  display the image using html url
  image = io.imread(image_url)  
  image = cv.cvtColor(image, cv.COLOR_BGR2RGB)

  # get details about face detection of the given image and display it under the image
  response = requests.get(
      'https://api.imagga.com/v2/faces/detections?image_url=%s&return_face_attributes=1' % (image_url),
      auth=(api_key, api_secret))
  json_data = response.json()

  try:
    for i in range(len(['result'])):
      # get coordinates of face
        xmax = json_data['result']['faces'][i]['coordinates']['xmax']
        xmin = json_data['result']['faces'][i]['coordinates']['xmin']
        ymax = json_data['result']['faces'][i]['coordinates']['ymax']
        ymin = json_data['result']['faces'][i]['coordinates']['ymin']

        start_point = (xmin, ymin)
        end_point = (xmax, ymax)
        color = (0, 255, 0)
        thickness = 1

        # display image with green bounding box
        image =  cv.rectangle(image, start_point, end_point, color, thickness)
        cv2_imshow(image)
        
        if json_data['result']['faces'][i]['confidence'] > 50.0:
            print("\033[1;32;47m Face Detected!")

        # display detected person's age, gender and ethnicity
        for i in range(len(['result'])):
          age = (json_data['result']['faces'][i]['attributes'][i]['label'])
          gender = (json_data['result']['faces'][i]['attributes'][i+1]['label'])
          ethnicity = (json_data['result']['faces'][i]['attributes'][i+2]['label'])
          print(f"\n Age: {age[0:-1]}\n Gender: {gender}\n Ethnicity: {ethnicity}")

  
  # if no face detected display image without bounding box
  except IndexError:
    cv2_imshow(image)
    print("\033[1;31;47m No Face Detected.")
  

face_detect("https://i.ibb.co/7xcR7Dx/k-Z6axpb-Qs-M6bir-GOs-Tz-Evfbjs70-WM5x2flem-D1c-X.jpg")
print('\n')

face_detect("https://i.ibb.co/NZp2bXZ/xpn9-X3zc0qad-HSBy-Otg-N7-LFCKWAe-WBp-Xp9-Oxx-URA.jpg")
print('\n')

face_detect("https://i.ibb.co/dB1tK9C/ebe3f369e9df6c2dedfbb8ba58f5b591.jpg")
print('\n')

face_detect("https://i.ibb.co/YBDxxgZ/ee96150e6d4b0fdb7364ea258dd0e77b.jpg")
print('\n')




