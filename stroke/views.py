from django.shortcuts import render
from django.template import RequestContext
from django.urls import reverse
from .forms import UploadImageForm, ImageUploadForm
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from .train import training
from .results import result_main
import os
from django.views.generic import View
from django.http import JsonResponse, HttpResponse
from .models import ImageUploadModel
from .serializers import ImageUploadSerializer
from rest_framework.response import Response
from rest_framework import viewsets
import base64
import json

class ReactAppView(View):
    def get(self, request):
        try:
            with open(os.path.join(str(settings.BASE_DIR),
                                    'frontend',
                                    'build',
                                    'index.html')) as file:
                return HttpResponse(file.read())

        except:
            
            return HttpResponse(status=501,)
        
    def post(self, request):
        print("결과가 왜 이래")
        data = json.loads(request.body)
        ide = data['description']
        doc = data['document']

        new_doc = doc[23:]

        ide = settings.MEDIA_ROOT_URL + settings.MEDIA_URL + ide + "_new.jpg"

        result_str, cropped_img, eye_rate, lip_rate, nose_rate = result_main(new_doc, True, ide)

        #result_str, cropped_img, LEFT_EYE_X, LEFT_LIP_X, RIGHT_EYE_X, RIGHT_LIP_X, LEFT_EYE_Y, LEFT_LIP_Y, RIGHT_EYE_Y, RIGHT_LIP_Y = result_main(new_doc, True, ide)
        context = {"result":result_str, "image":cropped_img, "eye_rate":eye_rate, "lip_rate":lip_rate, "nose_rate":nose_rate}
        #context = {'result':result_str, 'image':cropped_img, 'left_eye':LEFT_EYE,'left_lip':LEFT_LIP, 'right_eye':RIGHT_EYE, 'right_lip':RIGHT_LIP}

        return JsonResponse(context, safe=False)