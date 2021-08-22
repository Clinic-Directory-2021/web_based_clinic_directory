from django.shortcuts import render, redirect
from firebase_admin import credentials
from firebase_admin import firestore
from django.contrib import messages

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

    fname = request.POST.get('fname')
    lname = request.POST.get('lname')
    email = request.POST.get('email')
    password = request.POST.get('password')
    confirm_password = request.POST.get('confirm_password')

    if password == confirm_password:
        data = {"fname": fname,
        "lname": lname,
        "email": email,
        "password": password}
        try:
            #register email and password to firebase auth
            user = auth.create_user_with_email_and_password(email, password)
            doc_ref = firestoreDB.collection('users').document(user['localId'])
            doc_ref.set({
                'first_name': fname,
                'last_name': lname,
                'email': email,
                'password': password,
            })
            messages.success(request, "New User Registered Successfully!")
            return render(request,'register.html')
        except requests.HTTPError as e:
            error_json = e.args[1]
            error = json.loads(error_json)['error']['message']
            if error == "EMAIL_EXISTS":
                messages.success(request, "Email Already Exists!")
            return render(request,'register.html')

    else:
        messages.success(request, "Password Do not Match!")
        return render(request,'register.html')

def login_validation(request):
    email = request.POST.get('login_email')
    password = request.POST.get('login_password')
    
    try:
        user_signin = auth.sign_in_with_email_and_password(email,password)
        request.session['user_id'] = user_signin['localId']
        return redirect('/homepage')
    except:
        messages.success(request, "Invalid Email or Password!")
        return render(request,'login.html')

def logout(request):
    try:
        del request.session['user_id']
    except:
        return redirect('/index')
    return redirect('/index')