from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from get_best_words.get_word import suggest_word
import base64

import json
import cv2
import numpy as np
import requests

# Create your views here.
def index(request):
    context = {
        "message": "Hello World",
        'canvas': '',
        'fresh': True
    }
    return render(request, "scrabble/index.html", context)

#API to get words
@csrf_exempt
def getwords(request):
        # print(f'request.body: {type(request.body.decode("utf-8") )}')
        # print(f'request.body: {JsonResponse(request.body.decode("utf-8"),safe=False )}')
        # print(f'request.get: {request.FILES.get("choice")}')
        jsonFile = json.loads((request.body.decode("utf-8")))
        print(f'jsonFile: {jsonFile}, type: {type(jsonFile)}')
        characters = jsonFile['characters']
        # TODO: Use radix sort
        characters = sorted(characters)
        best_word, points = suggest_word(characters)
        print(f'returning: {best_word}, {points}')
        return JsonResponse(json.dumps(({'suggested_word': best_word, 'points': points})), safe=False)
