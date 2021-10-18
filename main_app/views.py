from django.shortcuts import render, redirect
from firebase_admin import credentials
from firebase_admin import firestore
from django.contrib import messages
from django.http import HttpResponse
from pyasn1.type.univ import Null

import pyrebase
import firebase_admin
import requests
import json

import folium

import datetime

from django.template.loader import render_to_string
from django.template import loader

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

storage = firebase.storage()

# Create your views here.

def index(request):
    #map Size
    #f = folium.Figure(width=1200, height=1000)

    #create Map and zoom on Malolos, Bulacan Philippines
    map = folium.Map(location =[14.8527, 120.8160], zoom_start = 13, min_zoom=13)

    timeNow = datetime.datetime.now().time()
    date_time = timeNow.strftime('%I:%M %p')
    currentTime = datetime.datetime.strptime(date_time, '%I:%M %p').time()

    users = firestoreDB.collection('users').get()

    user_data = []

    for user in users:
        value = user.to_dict()

        opening_time = datetime.datetime.strptime(value['opening_time'], '%I:%M %p').time()

        closing_time = datetime.datetime.strptime(value['closing_time'], '%I:%M %p').time()

        # opening_time = value['opening_time'].strftime('%I:%M %p')

        # closing_time = value['closing_time'].strftime('%I:%M %p')

        if opening_time < currentTime and currentTime < closing_time:
            user_data.append(value)
            
        latitude = value['latitude']
        longitude = value['longitude']

        folium.Marker([latitude, longitude], 
        popup= "<img style=\"width:200px;\" src=\""+value['clinic_img_url']+"\">"+"<b>Clinic Name:</b><br>" + value['clinic_name'] +"<br><br><img src='../static/images/rate.png' alt='' class='rate'><img src='../static/images/rate.png' alt='' class='rate'><img src='../static/images/rate.png' alt='' class='rate'><img src='../static/images/rate.png' alt='' class='rate'><img src='../static/images/rate.png' alt='' class='rate'><br>5.0" + "<br><br><b>Clinic Address:</b><br>" + value['clinic_address']  + "<br><br><b>Open and Closing time:</b><br>" + "<br><br><em>Description:</em><br>"+ value['clinic_description']  +"<br><br><b>Contact number:</b><br>", 
        icon=folium.Icon(color="red", icon="fa-paw", prefix='fa'),
        tooltip= value['clinic_name']).add_to(map)
        
    # Get html representation of the map
    map = map._repr_html_()

    if request.method == 'POST':
        userId = request.POST.get('user_id_post')
        items = firestoreDB.collection('items').document(userId).get()
        data = {
            'map': map,
            'user_data': user_data,
            'item_data': items.to_dict(),
         }
        return render(request, 'item_data.html', {'item_data':items.to_dict()})
        #return HttpResponse(json.dumps(items.to_dict()))
    else:
        data = {
            'map': map,
            'user_data': user_data,
        }
    

    if 'user_id' not in request.session:
        return render(request,'index.html', data)
    else:
        return redirect('/homepage')


def getSearchData(request):
    if request.method == 'POST':
        search_item = request.POST.get('search_item')

    users = firestoreDB.collection('users').get()

    items = firestoreDB.collection('items').get()

    user_data = []

    item_data = []

    for user in users:
        value = user.to_dict()
        user_data.append(value)

    for item in items:
        item_value = item.to_dict()
        item_data.append(item_value)

    return render(request, 'search_suggest.html', {
        'user_data': user_data,
        'search_item': search_item,
        'item_data': item_data,
        })

def login(request):
    #meaning if user_id session variable is not set then execute this code
    if 'user_id' not in request.session:
        return render(request,'login.html')
    else:
        return redirect('/homepage')

def homepage(request):
    if 'user_id' in request.session:
        user_data = firestoreDB.collection('users').document(request.session['user_id']).get()

        item_data = firestoreDB.collection('items').document(request.session['user_id']).get()

        return render(request,'homepage.html', {
        'user_data': user_data.to_dict(),
        'item_data': item_data.to_dict(),
        })
    else:
        return redirect('/login')

def register(request):
    #create Map and zoom on Malolos, Bulacan Philippines
    map = folium.Map(location =[14.8527, 120.8160], zoom_start = 13, min_zoom=13)

    map.add_child(folium.LatLngPopup())

    #map.add_child(folium.ClickForMarker())

    # Get html representation of the map
    map = map._repr_html_()

    

    #Store the html representation of the map to data variable
    data = {
        'map': map,
    }

    return render(request,'register.html', data)

def register_user_firebase(request):
    clinicImage =  request.FILES['clinicImage']
    fileName = request.POST.get('fileName')
    

    clinicName = request.POST.get('clinicName')
    clinicAddress = request.POST.get('clinicAddress')
    clinicContact = request.POST.get('clinicContact')
    latitude = request.POST.get('latitude')
    longitude = request.POST.get('longitude')
    email = request.POST.get('email')
    password = request.POST.get('password')
    confirm_password = request.POST.get('confirm_password')
    opening_time = request.POST.get('opening_time')
    closing_time = request.POST.get('closing_time')
    clinicDescription = request.POST.get('clinicDescription')

    if password == confirm_password:
        try:
            #register email and password to firebase auth
            user = auth.create_user_with_email_and_password(email, password)

            img_file_directory = user['localId']+"/clinic_images/"+ fileName

            #upload product image
            storage.child(img_file_directory).put(clinicImage, user['localId'])


            
            doc_ref = firestoreDB.collection('queue').document(user['localId'])
            doc_ref.set({
                'user_id': user['localId'],
                'clinic_img_url' : storage.child(img_file_directory).get_url(user['localId']),
                'clinic_img_directory' : img_file_directory,
                'clinic_name': clinicName,
                'clinic_address': clinicAddress,
                'clinic_contact_number': clinicContact,
                'latitude': latitude,
                'longitude': longitude,
                'email': email,
                'opening_time': opening_time,
                'closing_time': closing_time,
                'clinic_description': clinicDescription,
                'total_items': 0,
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
    
    users = firestoreDB.collection('users').get()

    try:
        user_signin = auth.sign_in_with_email_and_password(email,password)
        
        for user in users:
            value = user.to_dict()
            if value['email'] == email:
              request.session['user_id'] = user_signin['localId']
              return HttpResponse('Success!')

        return HttpResponse('Invalid Email or Password!')
    except:
        return HttpResponse('Invalid Email or Password!')

def logout(request):
    try:
        del request.session['user_id']
    except:
        return redirect('/')
    return redirect('/')

def settings(request):


    if 'user_id' in request.session:
        #map Size
        f = folium.Figure(width=800, height=500)

        #create Map and zoom on Malolos, Bulacan Philippines
        map = folium.Map(location =[14.8527, 120.8160], zoom_start = 13, min_zoom=13).add_to(f)

        map.add_child(folium.LatLngPopup())

        #map.add_child(folium.ClickForMarker())

        # Get html representation of the map
        map = map._repr_html_()

        result = firestoreDB.collection('users').document(request.session['user_id']).get()
        result.to_dict()
        return render(request,'settings.html', {
            'user_data': result.to_dict(),
            'map': map,
            })
    else:
        return redirect('/login')

def save_clinic_info(request):
    clinicImage =  request.FILES['clinicImage']
    fileName = request.POST.get('fileName')
    img_file_directory = request.session['user_id']+"/clinic_images/"+ fileName
    old_img_file_directory = request.POST.get('old_image_directory')

    editClinicName = request.POST.get('editClinicName')
    editClinicAddress = request.POST.get('editClinicAddress')
    clinicContact = request.POST.get('clinicContact')
    editLatitude = request.POST.get('editLatitude')
    editLongitude = request.POST.get('editLongitude')
    opening_time = request.POST.get('opening_time')
    closing_time = request.POST.get('closing_time')
    editClinicDescription = request.POST.get('editClinicDescription')

    doc_ref = firestoreDB.collection('users').document(request.session['user_id'])

    #delete the old picture
    storage.delete(old_img_file_directory, request.session['user_id'])
    
    #upload product image
    storage.child(img_file_directory).put(clinicImage, request.session['user_id'])

    doc_ref.update({
        'clinic_img_url' : storage.child(img_file_directory).get_url(request.session['user_id']),
        'clinic_img_directory' : img_file_directory,
        'clinic_address': editClinicAddress,
        'clinic_contact_number': clinicContact,
        'clinic_name': editClinicName,
        'latitude': editLatitude,
        'longitude': editLongitude,
        'clinic_description': editClinicDescription,
        'opening_time': opening_time,
        'closing_time': closing_time,
        })
    return HttpResponse('Information Updated Successfully!')

def add_item(request):
    user_data = firestoreDB.collection('users').document(request.session['user_id']).get()
    return render(request,'add_item.html', {
        'user_data': user_data.to_dict(),
    })

def add_item_firebase(request):
    items_doc_ref = firestoreDB.collection('items').document(request.session['user_id'])

    try:
        product_name = request.POST.get('product_name')
        product_price = request.POST.get('product_price')
        field_name = request.POST.get('field_name')
        product_image = request.FILES['selected_product_image']
        img_fileName = product_image.name
        img_file_directory = request.session['user_id']+"/product_images/"+ img_fileName
        
        #if fields are not null then try to update the document on items,
        #if that document is not yet existing then create one
        if product_name != "" and product_price != "" and field_name != "" and product_image != "" and img_fileName != "" and img_file_directory != "":
            
            #upload product image
            storage.child(img_file_directory).put(product_image, request.session['user_id'])
            
            try:
                items_doc_ref.update({
                field_name: {
                    'belong_to': request.session['user_id'],
                    'product_img_url' : storage.child(img_file_directory).get_url(request.session['user_id']),
                    'product_img_directory' : img_file_directory,
                    'product_name': product_name,
                    'product_price': product_price,
                    'availability': "available",
                    }
                })
            except:
                items_doc_ref.set({
                field_name: {
                        'belong_to': request.session['user_id'],
                        'product_img_url' : storage.child(img_file_directory).get_url(request.session['user_id']),
                        'product_img_directory' : img_file_directory,
                        'product_name': product_name,
                        'product_price': product_price,
                        'availability': "available",
                        }
                    })
            #increment the total number of items in a specific user
            users_doc_ref = firestoreDB.collection('users').document(request.session['user_id'])
            users_doc_ref.update({"total_items": firestore.Increment(1)})
            return redirect('/')
        else:
            messages.success(request, "Please Fill up all the forms")
            return render(request,'add_item.html')
    except:
        messages.success(request, "Please upload product image first")
        return render(request,'add_item.html')
   
def edit_item_firebase(request):
    items_doc_ref = firestoreDB.collection('items').document(request.session['user_id'])

    try:
        product_name = request.POST.get('edit_prod_name')
        product_price = request.POST.get('edit_prod_price')
        field_name = request.POST.get('edit_field_name')
        product_image = request.FILES['selected_edit_product_image']
        img_fileName = product_image.name
        img_file_directory = request.session['user_id']+"/product_images/"+ img_fileName
        old_img_file_directory = request.POST.get('old_image_directory')
        
        #if fields are not null then try to update the document on items,
        #if that document is not yet existing then create one
        if product_name != "" and product_price != "" and field_name != "" and product_image != "" and img_fileName != "" and img_file_directory != "" and old_img_file_directory != "":
            
            #delete the old picture
            storage.delete(old_img_file_directory, request.session['user_id'])

            #upload product image
            storage.child(img_file_directory).put(product_image, request.session['user_id'])

            items_doc_ref.update({
            field_name: {
                'belong_to': request.session['user_id'],
                'product_img_url' : storage.child(img_file_directory).get_url(request.session['user_id']),
                'product_img_directory' : img_file_directory,
                'product_name': product_name,
                'product_price': product_price,
                'availability': "available",
                }
            })

            return redirect('/')
        else:
            messages.success(request, "Please Fill up all the forms")
            return render(request,'homepage.html')
    except:
        messages.success(request, "Please upload product image first")
        return render(request,'homepage.html')   
    
def product_item_availability(request):
    items_doc_ref = firestoreDB.collection('items').document(request.session['user_id'])
    if request.method == 'POST':
        availability = request.POST.get('availability')
        field_name = request.POST.get('product_key')

        product_name = request.POST.get('prod_name')
        product_price = request.POST.get('prod_price')
        product_image_url = request.POST.get('prod_img_url')
        img_file_directory = request.POST.get('prod_img_directory')

        if availability == 'available':
            items_doc_ref.update({
            field_name: {
                'belong_to': request.session['user_id'],
                'product_img_url' : product_image_url,
                'product_img_directory' : img_file_directory,
                'product_name': product_name,
                'product_price': product_price,
                'availability': "available",
                }
            })
        if availability == 'not available':
            items_doc_ref.update({
            field_name: {
                'belong_to': request.session['user_id'],
                'product_img_url' : storage.child(img_file_directory).get_url(request.session['user_id']),
                'product_img_directory' : img_file_directory,
                'product_name': product_name,
                'product_price': product_price,
                'availability': "not available",
                }
            })

    return HttpResponse('')

def search_item(request):
    searchField = request.POST.get('searchField')

    if 'user_id' in request.session:
        user_data = firestoreDB.collection('users').document(request.session['user_id']).get()

        item_data = firestoreDB.collection('items').document(request.session['user_id']).get()

        return render(request,'homepage_search.html', {
        'user_data': user_data.to_dict(),
        'item_data': item_data.to_dict(),
        'searchField': searchField,
        })
    else:
        return redirect('/login')

def search_clinic(request):
    users = firestoreDB.collection('users').get()

    items = firestoreDB.collection('items').get()

    search_item = request.POST.get('search_item')

    user_data = []

    item_data = []

    for user in users:
        value = user.to_dict()
        user_data.append(value)

    for item in items:
        item_value = item.to_dict()
        item_data.append(item_value)

        
    return render(request,'index_search.html', {
        'user_data': user_data,
        'search_item': search_item,
        'item_data': item_data,
    })

def forgot_password(request):
    try:
        if request.method == 'POST':
            forgot_pass_email = request.POST.get('forgot_pass_email')
            auth.send_password_reset_email(forgot_pass_email)
            data = {
                'success': "Successfully Sent To Your Email",
            }
        else:
            data = {
                'success': "",
            }
    except:
        data = {
                'success': "Email Not Found!",
            }

    return render(request,'forgot_password.html', data)


def about(request):
    return render(request,'about.html')
