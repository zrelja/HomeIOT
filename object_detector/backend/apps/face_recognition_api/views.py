import numpy as np
import os
import sys
import tarfile
import zipfile
import time
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from io import BytesIO
from PIL import Image
import requests
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.decorators import parser_classes
try:
    from django.utils import simplejson as json
except ImportError:
    import json


import face_recognition
import urllib.request
from django.conf import settings as djangoSettings
import base64
import time





@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
@parser_classes((JSONParser,))
def face_recognition_api(request):
    start = time.time()

    print("Request for detection, let's detect!")
    data = {}

    load_jsona = time.time()
    with open('backend/static/known_people/known_people.json') as data_file:    
      known_persons = json.load(data_file)
    print("Load json filea {}", (time.time() - load_jsona))
  
   # all_known_persons_encodings = np.array([])
    first_element = False
    encodings = ""  

  # all_known_persons_encodings = np.empty(())
    i=0
    encoding = []
   # all_known_persons_encodings = []
    ucitavanje_encodinga = time.time()
    for person in known_persons['data']:
         encoding_array = np.fromstring((person["face_encoding"].replace("[","")).replace("]",""), dtype=float, sep=', ')
         encoding.append(encoding_array)

    all_known_persons_encodings = encoding
    print("Ucitavanje encodinga u array  {}", (time.time() - ucitavanje_encodinga))


    if request.method == "GET": 
        url = request.GET.get('image')
        print(url)

        image_url = "https://" + url
        spremanje_load_slike = time.time()
        urllib.request.urlretrieve(image_url, "backend/static/unknown_people/unknown.jpg")

        # Load the uploaded image file
        
        img = face_recognition.load_image_file("backend/static/unknown_people/unknown.jpg")
        print("Spremanje i load slike  {}", (time.time() - ucitavanje_encodinga))

        # Get face encodings for any faces in the uploaded image
        encoding_slike = time.time()
        unknown_face_encodings = face_recognition.face_encodings(img)[0]
        print("Encoding time {}", (time.time() - encoding_slike))

        # See how far apart the test image is from the known faces
        face_distances = face_recognition.face_distance(all_known_persons_encodings, unknown_face_encodings)
        data['recognized'] = False
        base64image = base64.b64encode(open("backend/static/unknown_people/unknown.jpg","rb").read())
        data['image'] = str.encode('data:image/jpeg;base64, ') + base64image
        for i, face_distance in enumerate(face_distances):
              if(face_distance < 0.63):
                data['recognized'] = True
                data['name'] = known_persons['data'][i]['name']

        print("Image scanned for {}, face recognition done", (time.time() - start))

    return Response(data)

