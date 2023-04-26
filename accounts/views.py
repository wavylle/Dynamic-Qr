from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import time
from django.contrib.auth.models import User, auth
from django.contrib import messages
import hashlib
from .models import userData
from django.views.decorators.csrf import csrf_exempt
import requests
from django.contrib.auth import get_user_model
import json

def index(request):
    if request.user.is_authenticated:
        user_upi_id = userData.objects.get(username = request.user.username).upiid
        return render(request, "index.html", {'user_upi_id': user_upi_id})
    else:
        return redirect("/accounts/login")

###Register###
@csrf_exempt
def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password = request.POST.get("password")
        # password1 = request.POST['password1']
        # password2 = request.POST['password2']
        # email = request.POST['email']
        phone = request.POST.get('phone')
        upiid = request.POST.get('upiid')

        if User.objects.filter(username=username).exists():
            messages.info(request, 'Username already exists')
            err_data = {
            'status': False
            }
            return redirect('register')
        elif userData.objects.filter(phone = phone).exists():
            messages.info(request, 'Phone number already in use')
            return redirect('register')
        elif userData.objects.filter(upiid = upiid).exists():
            messages.info(request, 'UPI Id already registered')
            return redirect('register')
        else:
            user = User.objects.create_user(username=username, password = password, first_name=first_name, last_name=last_name)
            user.save()
            userData.objects.create(username = username, first_name = first_name, last_name = last_name, phone = phone, upiid = upiid)
            timestamp = time.time()
            name = str(first_name) + str(last_name)
            hashCombination = str(username) + str(name) + str(int(timestamp))
            # print(int(timestamp))
            hashUserToken = hashlib.sha256(hashCombination.encode()).hexdigest()
            user = User.objects.get(username = username)
            auth.login(request, user)
            # print(int(timestamp))
            #
            # api_key = '8921678e-2868-11ed-9c12-0200cd936042'
            #
            # url = f"https://2factor.in/API/V1/{api_key}/SMS/+91{phone}/AUTOGEN2/OTP1"
            #
            # payload={}
            # headers = {}
            #
            # response = requests.request("GET", url, headers=headers, data=payload)
            #
            # if 'OTP' in response.json():
            #     return render(request, 'otp.html', {'otp': response.json()['OTP'], 'username': username})
            #
            # else:
            #     messages.info(request, 'Invalid phone number')
            # return redirect('register')
            return redirect('login')
    else:
        return render(request, 'register.html')


###Login###
@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password = password)

        if user is not None:
            if userData.objects.get(username = username):
                auth.login(request, user)
                return redirect('/')
            else:
                messages.info(request, 'Invalid credentials')
                return redirect('login')
        else:
            messages.info(request, 'Invalid credentials')
            return redirect('login')
    else:
        return render(request, 'login.html')


###Logout###
def logout(request):
    auth.logout(request)
    return redirect('/accounts/login')


### OTP Verification ###
@csrf_exempt
def otpverification(request):
    if request.method == 'POST':
        otpinp = request.POST.get('otpinp')
        username = request.POST.get('username')
        print(username)

        verificationUpdate = userData.objects.get(username = username)
        verificationUpdate.phone_verification_status = True
        verificationUpdate.save()

        return redirect('/accounts/login')

#### Image Post Req Test Func ###
# import io
# import json
# import base64
# import logging
# import numpy as np
# import face_recognition
# from PIL import Image
# from flask import Flask, request, jsonify, abort
#
# @csrf_exempt
# def imagePost(request):
#     if request.method == 'POST':
#         known_images = request.POST.get('known_images')
#         unknown_image = request.POST.get('unknown_image')
#         api_key = request.POST.get('api_key')
#         known_images_files = []
#         files_dict = {}
#
#         # Known images saving
#         for e, x in enumerate(json.loads(known_images)):
#             img_bytes = base64.b64decode(x.encode('utf-8'))
#
#             # convert bytes data to PIL Image object
#             img = Image.open(io.BytesIO(img_bytes))
#             img.save(f'static/images/{api_key}-known-{e}.png', 'png')
#             known_images_files.append(f'static/images/{api_key}-known-{e}.png')
#
#         # Unknown image saving
#         img_bytes = base64.b64decode(unknown_image.encode('utf-8'))
#
#         # convert bytes data to PIL Image object
#         img = Image.open(io.BytesIO(img_bytes))
#         img.save(f'static/images/{api_key}-unknown.png', 'png')
#
#         files_dict['unknown_image'] = f'static/images/{api_key}-unknown.png'
#         files_dict['known_images'] = known_images_files
#
#         match_faces(json.dumps(files_dict['known_images']), files_dict['unknown_image'])
#
#         # PIL image object to numpy array
#         # img_arr = np.asarray(img)
#         # print('img shape', img_arr.shape)
#         # print(img)
#
#         result_dict = {'output': 'output_key'}
#         return JsonResponse(result_dict)


# def match_faces(known_faces, unknown_face):
#     knownEncodeList = []
#     for img in json.loads(known_faces):
#         knownImg = face_recognition.load_image_file('static/images/1234-known-0.png')
#         encodeImg = face_recognition.face_encodings(knownImg)
#         if encodeImg:
#             encodeImg = face_recognition.face_encodings(knownImg)[0]
#             knownEncodeList.append(encodeImg)
#
#     unknown_img = cv2.imread(unknown_face)
#     unknown_img = cv2.cvtColor(unknown_img, cv2.COLOR_BGR2RGB)
#     unknown_encodings = face_recognition.face_encodings(unknown_img)
#     if unknown_encodings:
#         unknown_encodings = face_recognition.face_encodings(unknown_img)[0]
#
#     results = face_recognition.compare_faces(knownEncodeList, unknown_encodings)
#     print(results)
