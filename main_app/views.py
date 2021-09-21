from django.shortcuts import render, redirect
from firebase_admin import credentials
from firebase_admin import firestore
from django.contrib import messages
from django.http import HttpResponse

import pyrebase
import firebase_admin
import requests
import json


config={
    "apiKey": "AIzaSyDwWsW--ZHaZIOE4OXu5VhMIclZad8zDYw",
    "authDomain": "animal-clinic-directory-2021.firebaseapp.com",
    "databaseURL": "https://animal-clinic-directory-2021-default-rtdb.firebaseio.com/",
    "projectId": "animal-clinic-directory-2021",
    "storageBucket": "animal-clinic-directory-2021.appspot.com",
    "messagingSenderId": "165228810397",
    "appId": "1:165228810397:web:8378bcc8cb06dd52520474",
    "measurementId": "G-D4BEP96KMK"
}

firebase = pyrebase.initialize_app(config)
cred = credentials.Certificate("main_app\serviceAccountKey.json")
firebase_admin.initialize_app(cred)

auth = firebase.auth()
db = firebase.database()
firestoreDB = firestore.client()

# Create your views here.
def index(request):
    if 'user_id' not in request.session:
        return render(request,'index.html')
    else:
        return redirect('/homepage')

def login(request):
    #meaning if user_id session variable is not set then execute this code
    if 'user_id' not in request.session:
        return render(request,'login.html')
    else:
        return redirect('/homepage')

def homepage(request):
    if 'user_id' in request.session:
        result = firestoreDB.collection('users').document(request.session['user_id']).get()
        result.to_dict()
        return render(request,'homepage.html', {
        'user_data': result.to_dict(),
        })
    else:
        return redirect('/login')

def register(request):
    return render(request,'register.html')

def register_user_firebase(request):
    clinicName = request.POST.get('clinicName')
    clinicAddress = request.POST.get('clinicAddress')
    email = request.POST.get('email')
    password = request.POST.get('password')
    confirm_password = request.POST.get('confirm_password')
    clinicDescription = request.POST.get('clinicDescription')

    if password == confirm_password:
        try:
            #register email and password to firebase auth
            user = auth.create_user_with_email_and_password(email, password)
            doc_ref = firestoreDB.collection('users').document(user['localId'])
            doc_ref.set({
                'clinic_name': clinicName,
                'clinic_address': clinicAddress,
                'email': email,
                'password': password,
                'clinic_description': clinicDescription,
            })
            #messages.success(request, "New User Registered Successfully!")
            return HttpResponse('New User Registered Successfully!')
        except requests.HTTPError as e:
            error_json = e.args[1]
            error = json.loads(error_json)['error']['message']
            if error == "EMAIL_EXISTS":
                #messages.success(request, "Email Already Exists!")
                return HttpResponse('Email Already Exists!')

    else:
        #messages.success(request, "Password Do not Match!")
        return HttpResponse('Password Do not Match!')

def login_validation(request):
    email = request.POST.get('login_email')
    password = request.POST.get('login_password')
    
    try:
        user_signin = auth.sign_in_with_email_and_password(email,password)
        request.session['user_id'] = user_signin['localId']
        return redirect('/homepage')
    except:
        return HttpResponse('Invalid Email or Password!')

def logout(request):
    try:
        del request.session['user_id']
    except:
        return redirect('/')
    return redirect('/')

def settings(request):
    result = firestoreDB.collection('users').document(request.session['user_id']).get()
    result.to_dict()
    return render(request,'settings.html', {
        'user_data': result.to_dict(),
        })

def save_clinic_info(request):
    editClinicName = request.POST.get('editClinicName')
    editClinicAddress = request.POST.get('editClinicAddress')
    editClinicDescription = request.POST.get('editClinicDescription')

    doc_ref = firestoreDB.collection('users').document(request.session['user_id'])
    doc_ref.update({
        'clinic_address': editClinicAddress,
        'clinic_name': editClinicName,
        'clinic_description': editClinicDescription,
        })
    return HttpResponse('Information Updated Successfully!')

def add_item(request):
    return render(request,'add_item.html')